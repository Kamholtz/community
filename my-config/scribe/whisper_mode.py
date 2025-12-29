"""
Talon integration for Whisper transcription daemon.

Provides a dedicated `user.whisper` mode that minimizes command listening
while transcription is active. While in this mode, only the phrase
"talon whisper done" is recognized (see whisper_mode.talon) to exit.

On entry: unmute the transcription daemon and disable `command` mode.
On exit: mute the daemon and re-enable `command` mode.
"""

from talon import actions, Context, Module, cron
from pathlib import Path
import json
import queue
import subprocess
import threading

mod = Module()
mod.mode("whisper", desc="Transcription mode for Whisper daemon")

ctx = Context()

REALITIME_DIR = Path("~/repos/realtimestt-cli").expanduser()
REALITIME_CMD = ["./venv/bin/python3", "./webserver/client.py", "--json-lines"]
_whisper_proc = None
_whisper_reader_thread = None
_whisper_stop_event = None
_whisper_queue_job = None
_whisper_event_queue = queue.Queue()
_whisper_enabled = False
_whisper_last_realtime = None
_whisper_last_full = None
_whisper_prev_theme = None
_whisper_theme_map = {
    "dark": "dark_whisper",
    "light": "light_whisper",
}
_WHISPER_VAD_SUBTITLE = "Listening..."


def _notify(msg: str) -> None:
    try:
        actions.user.notify(msg)
    except Exception:
        # In case notify isn't available in this Talon build
        pass


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


def _queue_ui_action(action) -> None:
    _whisper_event_queue.put(action)


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
    global _whisper_last_realtime, _whisper_last_full
    event_type = event.get("type")
    if not event_type or not _whisper_enabled:
        return

    if event_type == "vad_start":
        _whisper_last_realtime = None
        _queue_ui_action(lambda: _show_subtitle(_WHISPER_VAD_SUBTITLE))
        return

    if event_type == "realtime":
        content = event.get("content")
        if not content or content == _whisper_last_realtime:
            return

        _whisper_last_realtime = content
        _queue_ui_action(lambda text=content: _show_subtitle(text))
        return

    if event_type == "full":
        content = event.get("content")
        if not content or content == _whisper_last_full:
            return

        _whisper_last_full = content
        text_to_insert = f"{content} "
        _queue_ui_action(lambda text=text_to_insert: actions.insert(text))
        _queue_ui_action(lambda text=content: _show_subtitle(text))


def _read_proc_output(proc: subprocess.Popen, stop_event: threading.Event) -> None:
    if proc.stdout is None:
        return

    for raw_line in proc.stdout:
        if stop_event.is_set():
            break

        line = raw_line.strip()
        if not line:
            continue

        try:
            event = json.loads(line)
        except Exception:
            continue

        if isinstance(event, dict):
            _handle_ws_event(event)


def _start_reader() -> None:
    global _whisper_reader_thread, _whisper_stop_event, _whisper_queue_job
    if _whisper_proc is None or _whisper_proc.stdout is None:
        return

    if _whisper_reader_thread is not None and _whisper_reader_thread.is_alive():
        return

    _whisper_stop_event = threading.Event()
    _whisper_reader_thread = threading.Thread(
        target=_read_proc_output,
        args=(_whisper_proc, _whisper_stop_event),
        daemon=True,
    )
    _whisper_reader_thread.start()

    if _whisper_queue_job is None:
        _whisper_queue_job = cron.interval("100ms", _drain_event_queue)


def _stop_reader() -> None:
    global _whisper_reader_thread, _whisper_stop_event, _whisper_queue_job
    if _whisper_stop_event is not None:
        _whisper_stop_event.set()

    if _whisper_reader_thread is not None:
        _whisper_reader_thread.join(timeout=1.0)
    _whisper_reader_thread = None
    _whisper_stop_event = None

    if _whisper_queue_job is not None:
        cron.cancel(_whisper_queue_job)
        _whisper_queue_job = None

    _drain_event_queue()


def _start_proc() -> bool:
    global _whisper_proc
    if _proc_is_running():
        _start_reader()
        return True

    if not REALITIME_DIR.exists():
        _notify(f"Whisper: missing dir {REALITIME_DIR}")
        return False

    try:
        _whisper_proc = subprocess.Popen(
            REALITIME_CMD,
            cwd=str(REALITIME_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        _start_reader()
        return True
    except Exception:
        _notify("Whisper: failed to start subprocess")
        _whisper_proc = None
        return False


def _stop_proc() -> None:
    global _whisper_proc
    if not _proc_is_running():
        _whisper_proc = None
        _stop_reader()
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
        _whisper_proc = None
        _stop_reader()


def _switch_hud_theme(theme_name: str) -> None:
    try:
        actions.user.hud_switch_theme(theme_name)
    except Exception:
        # HUD theme setting not available or failed
        pass


@mod.action_class
class Actions:
    def whisper_start():
        """Enter whisper mode: enable transcription and minimize commands."""
        global _whisper_enabled
        if not _start_proc():
            return

        # Enable whisper mode alongside command mode
        # Whisper mode commands will override conflicting command mode commands
        _whisper_enabled = True
        actions.mode.enable("user.whisper")

        # Switch to a whisper-capable theme if we have one registered.
        global _whisper_prev_theme
        if _whisper_prev_theme is None:
            try:
                current_theme = actions.user.hud_get_theme()
                _whisper_prev_theme = getattr(current_theme, "name", None)
            except Exception:
                _whisper_prev_theme = None

        if _whisper_prev_theme:
            whisper_theme = _whisper_theme_map.get(_whisper_prev_theme)
            if whisper_theme:
                _switch_hud_theme(whisper_theme)

        _notify("Whisper mode: ON - typing enabled (say 'talon whisper done' to exit)")

    def whisper_done():
        """Exit whisper mode: mute transcription and restore command mode."""
        global _whisper_enabled, _whisper_last_realtime, _whisper_last_full
        _stop_proc()
        _whisper_enabled = False
        _whisper_last_realtime = None
        _whisper_last_full = None

        # Simply disable whisper mode - command mode stays active
        actions.mode.disable("user.whisper")

        # Restore the previous HUD theme if we switched it.
        global _whisper_prev_theme
        if _whisper_prev_theme:
            _switch_hud_theme(_whisper_prev_theme)
        _whisper_prev_theme = None

        _notify("Whisper mode: OFF - console output restored")
