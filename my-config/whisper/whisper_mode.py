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
from typing import Optional

import json
import queue
import subprocess
import sys
import threading

mod = Module()
mod.mode("whisper", desc="Transcription mode for Whisper daemon")

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
_whisper_last_full = None
_whisper_prev_theme = None
_whisper_theme_switched = False
_whisper_theme_map = {
    "dark": "dark_whisper",
    "light": "light_whisper",
}
_WHISPER_VAD_SUBTITLE = "Listening..."


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
        _apply_whisper_theme()
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
    global _whisper_enabled, _whisper_last_realtime, _whisper_last_full
    if _whisper_enabled:
        return True

    _whisper_last_realtime = None
    _whisper_last_full = None
    _whisper_enabled = True
    _enter_whisper_mode()
    _apply_whisper_theme()

    started = _start_proc()
    if not started:
        _whisper_enabled = False
        _exit_whisper_mode()
        _restore_hud_theme()

    return started


def _disable_whisper() -> None:
    """Ensure the Whisper process is stopped and reset the tracked state."""
    global _whisper_enabled
    if not _whisper_enabled and not _proc_is_running():
        _exit_whisper_mode()
        _restore_hud_theme()
        return

    _whisper_enabled = False
    _exit_whisper_mode()
    _restore_hud_theme()
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
