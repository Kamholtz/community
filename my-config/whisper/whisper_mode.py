"""
Talon integration for Whisper transcription daemon.

Provides a dedicated `user.whisper` mode that minimizes command listening
while transcription is active. While in this mode, only the phrase
"talon whisper done" is recognized (see whisper_mode.talon) to exit.

On entry: unmute the transcription daemon and disable `command` mode.
On exit: mute the daemon and re-enable `command` mode.
"""

from talon import actions, app, Context, Module, cron, ctrl, imgui, settings, ui
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from pathlib import Path
from talon.types import Rect
from typing import Optional

from whisper_transcript_state import PendingTranscript, TranscriptState

import json
import queue
import subprocess
import sys
import threading

mod = Module()
mod.mode("whisper", desc="Transcription mode for Whisper daemon")
mod.setting(
    "whisper_insert_history_size",
    type=int,
    default=50,
    desc="Number of inserted Whisper dictation entries to keep in session history.",
)
mod.setting(
    "whisper_polish_segments",
    type=bool,
    default=True,
    desc="Wait briefly for polished Whisper segments before inserting final text.",
)
mod.setting(
    "whisper_polish_fallback_ms",
    type=int,
    default=700,
    desc="Milliseconds to wait for a polished transcript before inserting the original.",
)

ctx = Context()

REALITIME_DIR = Path("~/repos/realtimestt-cli").expanduser()
if sys.platform == "win32":
    REALITIME_CMD = [str(REALITIME_DIR / "venv" / "Scripts" / "python.exe"), "webserver/client.py", "--json-lines"]
else:
    REALITIME_CMD = ["./venv/bin/python3", "./webserver/client.py", "--json-lines"]
_whisper_proc = None
_whisper_poll_job = None
_whisper_line_queue: queue.Queue = queue.Queue()
_whisper_event_queue: queue.Queue = queue.Queue()
_whisper_enabled = False
_whisper_last_realtime = None
_whisper_transcripts = TranscriptState()
_whisper_last_event_signature = None
_whisper_ui_state = None
_whisper_connected_notified = False
_whisper_prev_theme = None
_whisper_theme_switched = False
_whisper_theme_map = {
    "dark": "dark_whisper",
    "light": "light_whisper",
}
_whisper_insert_history: list[str] = []
_whisper_subtitle_canvases: list[Canvas] = []
_WHISPER_VAD_SUBTITLE = "Listening..."
_WHISPER_STATUS_TOPIC = "whisper_status"
_WHISPER_STATUS_ICON = "user.whisper_icon"
_WHISPER_STATUS_TEXT = {
    "connecting": "Connecting",
    "connected": "Connected",
    "listening": "Listening",
    "voice_detected": "Voice",
    "realtime": "Live",
    "transcribing": "Transcribing",
    "final": "Final",
    "polishing": "Polishing",
    "polished": "Polished",
    "connection_failed": "Failed",
    "disconnected": "Disconnected",
}
_WHISPER_SUBTITLE_COLORS = {
    "connecting": "dddddd",
    "connected": "55dd77",
    "listening": "dddddd",
    "voice_detected": "55c7ff",
    "realtime": "55d6ff",
    "transcribing": "ffcc66",
    "final": "ffff99",
    "polishing": "ffcc66",
    "polished": "77ee99",
    "connection_failed": "ff6666",
    "disconnected": "ff9966",
}


def _notify(msg: str) -> None:
    try:
        actions.user.notify(msg)
    except Exception:
        print("ERROR: actions.user.notify(msg) " + msg)


def _proc_is_running() -> bool:
    return _whisper_proc is not None and _whisper_proc.poll() is None


def _show_subtitle(text: str) -> None:
    try:
        from plugin.subtitles.subtitles import show_subtitle
    except Exception:
        _notify(text)
        return

    try:
        show_subtitle(text)
    except Exception:
        _notify(text)


def _get_subtitle_screens() -> list[ui.Screen]:
    screen = settings.get("user.subtitles_screens")
    if screen == "all":
        return ui.screens()
    if screen == "cursor":
        x, y = ctrl.mouse_pos()
        return [ui.screen_containing(x, y)]
    if screen == "focus":
        return [ui.active_window().screen]
    return [ui.main_screen()]


def _calculate_subtitle_timeout(text: str) -> int:
    per_char = settings.get("user.subtitles_timeout_per_char")
    min_ms = settings.get("user.subtitles_timeout_min")
    max_ms = settings.get("user.subtitles_timeout_max")
    return min(max_ms, max(min_ms, len(text) * per_char))


def _measure_subtitle_rect(c: SkiaCanvas, size: int, text: str) -> Rect:
    while True:
        c.paint.textsize = size
        rect = c.paint.measure_text(text)[1]
        if rect.width < c.width * 0.8:
            return rect
        size *= 0.9


def _draw_whisper_subtitle(
    c: SkiaCanvas,
    screen: ui.Screen,
    text: str,
    color: str,
    outline: str,
) -> None:
    scale = screen.scale if app.platform != "mac" else 1
    size = settings.get("user.subtitles_size") * scale
    rect = _measure_subtitle_rect(c, size, text)
    x = c.rect.center.x - rect.center.x
    y_setting = settings.get("user.subtitles_y")
    y = max(
        min(
            c.rect.y + y_setting * c.rect.height + c.paint.textsize / 2,
            c.rect.bot - rect.bot,
        ),
        c.rect.top - rect.top,
    )

    c.paint.imagefilter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.style = c.paint.Style.FILL
    c.paint.color = color
    c.draw_text(text, x, y)

    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = outline
    c.draw_text(text, x, y)


def _clear_whisper_subtitles() -> None:
    for canvas in _whisper_subtitle_canvases:
        canvas.close()
    _whisper_subtitle_canvases.clear()


def _show_whisper_subtitle(
    text: str,
    state: str,
    outline: str = "222222",
) -> None:
    if not settings.get("user.subtitles_show"):
        _show_subtitle(text)
        return

    _clear_whisper_subtitles()
    color = _WHISPER_SUBTITLE_COLORS.get(state, settings.get("user.subtitles_color"))
    timeout = _calculate_subtitle_timeout(text)

    for screen in _get_subtitle_screens():
        canvas = Canvas.from_screen(screen)
        canvas.register(
            "draw",
            lambda c, screen=screen, text=text, color=color: _draw_whisper_subtitle(
                c,
                screen,
                text,
                color,
                outline,
            ),
        )
        canvas.freeze()
        cron.after(f"{timeout}ms", canvas.close)
        _whisper_subtitle_canvases.append(canvas)


def _queue_ui_action(action) -> None:
    _whisper_event_queue.put(action)


def _publish_whisper_status(state: str) -> None:
    text = _WHISPER_STATUS_TEXT.get(state, state.replace("_", " ").title())
    try:
        status_icon = actions.user.hud_create_status_icon(
            _WHISPER_STATUS_TOPIC,
            _WHISPER_STATUS_ICON,
            text,
            f"Whisper {text}",
        )
        actions.user.hud_publish_status_icon(_WHISPER_STATUS_TOPIC, status_icon)
    except Exception:
        pass


def _remove_whisper_status() -> None:
    try:
        actions.user.hud_remove_status_icon(_WHISPER_STATUS_TOPIC)
    except Exception:
        pass


def _set_whisper_ui_state(state: str) -> None:
    global _whisper_ui_state
    if _whisper_ui_state == state:
        return

    _whisper_ui_state = state
    _publish_whisper_status(state)


def _remember_inserted_text(text: str) -> None:
    global _whisper_insert_history
    history_size = max(0, settings.get("user.whisper_insert_history_size"))
    if history_size == 0:
        _whisper_insert_history = []
        return

    _whisper_insert_history.append(text)
    _whisper_insert_history = _whisper_insert_history[-history_size:]


def _insert_and_remember(text: str) -> None:
    actions.insert(text)
    _remember_inserted_text(text)


def _cancel_fallback(pending: PendingTranscript) -> None:
    if pending.fallback_job is not None:
        cron.cancel(pending.fallback_job)
        pending.fallback_job = None


def _resolve_pending_transcript(identity: int) -> None:
    pending = _whisper_transcripts.resolve(identity)
    if pending is None:
        return

    _cancel_fallback(pending)
    _insert_and_remember(f"{pending.insertion_text} ")


def _insert_displaced_transcript(pending: PendingTranscript) -> None:
    if pending.inserted:
        return
    pending.inserted = True
    _cancel_fallback(pending)
    _insert_and_remember(f"{pending.insertion_text} ")


def _flush_pending_transcript() -> None:
    pending = _whisper_transcripts.pending
    if pending is not None:
        _resolve_pending_transcript(pending.identity)


def _format_history_preview(text: str, max_length: int = 80) -> str:
    preview = " ".join(text.split())
    if len(preview) > max_length:
        return preview[: max_length - 3] + "..."
    return preview


def _get_whisper_history_entry(index: int) -> Optional[str]:
    if index < 1 or index > len(_whisper_insert_history):
        return None

    return list(reversed(_whisper_insert_history))[index - 1]


@imgui.open(y=0)
def _whisper_history_gui(gui: imgui.GUI):
    gui.text("Whisper History")
    gui.line()

    if not _whisper_insert_history:
        gui.text("No Whisper dictation history")
    else:
        for index, text in enumerate(reversed(_whisper_insert_history), 1):
            preview = _format_history_preview(text)
            if gui.button(f"whisper pick {index}: {preview}"):
                actions.user.whisper_insert_history(index)

    gui.spacer()
    if gui.button("Whisper history close"):
        actions.user.whisper_history_hide()


def _drain_event_queue() -> None:
    while True:
        try:
            action = _whisper_event_queue.get_nowait()
        except queue.Empty:
            break

        try:
            action()
        except Exception:
            _notify("Whisper: failed to handle event")


def _handle_ws_event(event: dict) -> None:
    global _whisper_connected_notified, _whisper_last_event_signature, _whisper_last_realtime
    event_type = event.get("type")
    if not event_type or not _whisper_enabled:
        return

    event_signature = json.dumps(event, sort_keys=True, default=str)
    if event_signature == _whisper_last_event_signature:
        return
    _whisper_last_event_signature = event_signature

    if event_type == "client_connecting":
        _set_whisper_ui_state("connecting")
        _queue_ui_action(
            lambda: _show_whisper_subtitle("Connecting to Whisper...", "connecting")
        )
        return

    if event_type == "client_connected":
        _set_whisper_ui_state("connected")
        if not _whisper_connected_notified:
            _whisper_connected_notified = True
            _queue_ui_action(lambda: _notify("Whisper: connected"))
        _queue_ui_action(
            lambda: _show_whisper_subtitle("Whisper connected", "connected")
        )
        return

    if event_type == "client_connection_failed":
        content = event.get("content") or "Unable to connect"
        retry_seconds = event.get("retry_seconds")
        message = f"Whisper connection failed: {content}"
        if retry_seconds is not None:
            message = f"{message}; retrying in {retry_seconds}s"

        _set_whisper_ui_state("connection_failed")
        _queue_ui_action(lambda text=message: _notify(text))
        _queue_ui_action(
            lambda text=message: _show_whisper_subtitle(text, "connection_failed")
        )
        return

    if event_type == "client_disconnected":
        content = event.get("content") or "Server disconnected"
        _set_whisper_ui_state("disconnected")
        _queue_ui_action(lambda text=content: _notify(f"Whisper: {text}"))
        _queue_ui_action(
            lambda text=content: _show_whisper_subtitle(
                f"Whisper disconnected: {text}",
                "disconnected",
            )
        )
        return

    if event_type == "client_reconnecting":
        retry_seconds = event.get("retry_seconds")
        message = "Reconnecting to Whisper..."
        if retry_seconds is not None:
            message = f"Reconnecting to Whisper in {retry_seconds}s..."

        _set_whisper_ui_state("connecting")
        _queue_ui_action(
            lambda text=message: _show_whisper_subtitle(text, "connecting")
        )
        return

    if event_type == "vad_start":
        _whisper_last_realtime = None
        _set_whisper_ui_state("voice_detected")
        _apply_whisper_theme()
        _queue_ui_action(
            lambda: _show_whisper_subtitle("Voice detected", "voice_detected")
        )
        return

    if event_type == "record_start":
        _set_whisper_ui_state("listening")
        _queue_ui_action(
            lambda: _show_whisper_subtitle(_WHISPER_VAD_SUBTITLE, "listening")
        )
        return

    if event_type == "transcript_start":
        _set_whisper_ui_state("transcribing")
        _queue_ui_action(
            lambda: _show_whisper_subtitle("Transcribing...", "transcribing")
        )
        return

    if event_type == "realtime":
        content = event.get("content")
        if not content or content == _whisper_last_realtime:
            return

        _whisper_last_realtime = content
        _set_whisper_ui_state("realtime")
        _queue_ui_action(
            lambda text=content: _show_whisper_subtitle(f"Live: {text}", "realtime")
        )
        return

    if event_type == "full":
        content = event.get("content")
        if not content:
            return

        displaced, pending = _whisper_transcripts.begin_full(content)
        if displaced is not None and not displaced.inserted:
            _queue_ui_action(
                lambda transcript=displaced: _insert_displaced_transcript(transcript)
            )

        if not settings.get("user.whisper_polish_segments"):
            _set_whisper_ui_state("final")
            _queue_ui_action(
                lambda identity=pending.identity: _resolve_pending_transcript(identity)
            )
        else:
            fallback_ms = max(0, settings.get("user.whisper_polish_fallback_ms"))
            pending.fallback_job = cron.after(
                f"{fallback_ms}ms",
                lambda identity=pending.identity: _resolve_pending_transcript(identity),
            )
            _set_whisper_ui_state("polishing")

        _queue_ui_action(
            lambda text=content: _show_whisper_subtitle(f"Final: {text}", "final")
        )
        return

    if event_type == "polished":
        content = event.get("content")
        if not content:
            return

        pending = _whisper_transcripts.apply_polished(content)
        if pending is None:
            return

        _cancel_fallback(pending)
        _set_whisper_ui_state("polished")
        _queue_ui_action(
            lambda identity=pending.identity: _resolve_pending_transcript(identity)
        )
        _queue_ui_action(
            lambda text=content: _show_whisper_subtitle(
                f"Polished: {text}",
                "polished",
            )
        )


def _stdout_reader(proc: subprocess.Popen) -> None:
    """Background thread: feed stdout lines into _whisper_line_queue; None signals EOF."""
    if proc.stdout is None:
        _whisper_line_queue.put(None)
        return
    try:
        for raw in proc.stdout:
            _whisper_line_queue.put(raw.rstrip("\n"))
    except Exception:
        pass
    finally:
        _whisper_line_queue.put(None)


def _read_proc_output() -> None:
    for _ in range(20):
        try:
            line = _whisper_line_queue.get_nowait()
        except queue.Empty:
            break

        if line is None:
            if _whisper_enabled:
                _set_whisper_ui_state("disconnected")
                _queue_ui_action(lambda: _notify("Whisper: client disconnected"))
                _queue_ui_action(
                    lambda: _show_whisper_subtitle(
                        "Whisper client disconnected",
                        "disconnected",
                    )
                )
            _stop_proc()
            return

        line = line.strip()
        if not line:
            continue

        try:
            event = json.loads(line)
        except Exception:
            continue

        if isinstance(event, dict):
            _handle_ws_event(event)


def _poll_proc_output() -> None:
    _read_proc_output()
    _drain_event_queue()


def _start_polling() -> None:
    global _whisper_poll_job
    if _whisper_proc is None or _whisper_proc.stdout is None:
        return

    if _whisper_poll_job is None:
        _whisper_poll_job = cron.interval("100ms", _poll_proc_output)


def _stop_polling() -> None:
    global _whisper_poll_job
    if _whisper_poll_job is not None:
        cron.cancel(_whisper_poll_job)
        _whisper_poll_job = None
    while not _whisper_line_queue.empty():
        try:
            _whisper_line_queue.get_nowait()
        except queue.Empty:
            break
    _drain_event_queue()


def _start_proc() -> bool:
    global _whisper_proc
    if _proc_is_running():
        _start_polling()
        return True

    if not REALITIME_DIR.exists():
        _notify(f"Whisper: missing dir {REALITIME_DIR}")
        return False

    try:
        if sys.platform == "win32":
            _whisper_proc = subprocess.Popen(
                REALITIME_CMD,
                cwd=str(REALITIME_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        else:
            _whisper_proc = subprocess.Popen(
                REALITIME_CMD,
                cwd=str(REALITIME_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
        if _whisper_proc.stdout is None:
            _notify("Whisper: missing stdout pipe")
            _stop_proc()
            return False

        threading.Thread(target=_stdout_reader, args=(_whisper_proc,), daemon=True).start()
        _start_polling()
        return True
    except Exception as e:
        _notify(f"Whisper: failed to start subprocess: {e}")
        _whisper_proc = None
        return False


def _stop_proc() -> None:
    global _whisper_proc
    if not _proc_is_running():
        if _whisper_proc is not None and _whisper_proc.stdout is not None:
            try:
                _whisper_proc.stdout.close()
            except Exception:
                pass
        _whisper_proc = None
        _stop_polling()
        return

    try:
        _whisper_proc.terminate()
        _whisper_proc.wait(timeout=2.0)
    except subprocess.TimeoutExpired:
        _whisper_proc.kill()
        _whisper_proc.wait(timeout=2.0)
    except Exception:
        _notify("Whisper: failed to stop subprocess")
    finally:
        if _whisper_proc is not None and _whisper_proc.stdout is not None:
            try:
                _whisper_proc.stdout.close()
            except Exception:
                pass
        _whisper_proc = None
        _stop_polling()


def _switch_hud_theme(theme_name: str) -> None:
    try:
        actions.user.hud_switch_theme(theme_name)
    except Exception:
        # HUD theme setting not available or failed
        pass


def _get_current_theme_name() -> Optional[str]:
    try:
        current_theme = actions.user.hud_get_theme()
    except Exception:
        return None

    return getattr(current_theme, "name", None)


def _apply_whisper_theme() -> None:
    global _whisper_prev_theme, _whisper_theme_switched

    if _whisper_theme_switched:
        return

    theme_name = _whisper_prev_theme or _get_current_theme_name()
    if not theme_name:
        return

    if _whisper_prev_theme is None:
        _whisper_prev_theme = theme_name

    whisper_theme = _whisper_theme_map.get(theme_name)
    if not whisper_theme:
        return

    _switch_hud_theme(whisper_theme)
    _whisper_theme_switched = True


def _restore_hud_theme() -> None:
    global _whisper_prev_theme, _whisper_theme_switched

    if _whisper_theme_switched and _whisper_prev_theme:
        _switch_hud_theme(_whisper_prev_theme)

    _whisper_prev_theme = None
    _whisper_theme_switched = False


def _enter_whisper_mode() -> None:
    """Activate whisper mode and suppress command mode while transcribing."""
    try:
        actions.mode.disable("command")
    except Exception:
        pass

    try:
        actions.mode.enable("user.whisper")
    except Exception:
        pass


def _exit_whisper_mode() -> None:
    """Reset mode state when whisper transcription stops."""
    try:
        actions.mode.disable("user.whisper")
    except Exception:
        pass

    try:
        actions.mode.enable("command")
    except Exception:
        pass


def _enable_whisper() -> bool:
    """Mark Whisper as enabled and start the real-time process."""
    global _whisper_connected_notified, _whisper_enabled, _whisper_last_event_signature, _whisper_last_realtime, _whisper_ui_state
    if _whisper_enabled:
        return True

    _whisper_ui_state = None
    _whisper_connected_notified = False
    _whisper_last_realtime = None
    _whisper_last_event_signature = None
    _whisper_transcripts.reset()
    _whisper_enabled = True
    _enter_whisper_mode()
    _apply_whisper_theme()
    _set_whisper_ui_state("connecting")
    _queue_ui_action(lambda: _show_whisper_subtitle("Connecting to Whisper...", "connecting"))

    started = _start_proc()
    if not started:
        _whisper_enabled = False
        _exit_whisper_mode()
        _restore_hud_theme()
        _remove_whisper_status()

    return started


def _disable_whisper() -> None:
    """Ensure the Whisper process is stopped and reset the tracked state."""
    global _whisper_connected_notified, _whisper_enabled, _whisper_last_event_signature, _whisper_last_realtime, _whisper_ui_state
    if not _whisper_enabled and not _proc_is_running():
        _exit_whisper_mode()
        _restore_hud_theme()
        _remove_whisper_status()
        _clear_whisper_subtitles()
        return

    _flush_pending_transcript()
    _whisper_enabled = False
    _whisper_connected_notified = False
    _whisper_last_realtime = None
    _whisper_last_event_signature = None
    _whisper_transcripts.reset()
    _whisper_ui_state = None
    _exit_whisper_mode()
    _restore_hud_theme()
    _remove_whisper_status()
    _clear_whisper_subtitles()
    _stop_proc()


@mod.action_class
class Actions:
    def whisper_start() -> bool:
        """Begin transcription by enabling Whisper and starting the daemon."""
        return _enable_whisper()

    def whisper_done() -> None:
        """Stop transcription by disabling Whisper and stopping the daemon."""
        _disable_whisper()

    def whisper_toggle() -> None:
        """Toggle the Whisper daemon on/off based on the current state."""
        if _whisper_enabled or _proc_is_running():
            _disable_whisper()
            actions.speech.enable()
        else:
            actions.speech.disable()
            _enable_whisper()

    def whisper_insert_latest() -> None:
        """Insert the most recent Whisper dictation history entry."""
        actions.user.whisper_insert_history(1)

    def whisper_insert_history(index: int) -> None:
        """Insert a Whisper dictation history entry by newest-first index."""
        text = _get_whisper_history_entry(index)
        if text is None:
            _notify("Whisper: no history entry at that number")
            return

        actions.insert(text)
        _whisper_history_gui.hide()

    def whisper_history_toggle() -> None:
        """Toggle the Whisper dictation history GUI."""
        if _whisper_history_gui.showing:
            _whisper_history_gui.hide()
        else:
            _whisper_history_gui.show()

    def whisper_history_hide() -> None:
        """Hide the Whisper dictation history GUI."""
        _whisper_history_gui.hide()

    def whisper_history_clear() -> None:
        """Clear the Whisper dictation history."""
        global _whisper_insert_history
        _whisper_insert_history = []
        _whisper_history_gui.hide()
