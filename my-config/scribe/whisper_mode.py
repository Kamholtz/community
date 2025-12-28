"""
Talon integration for Whisper transcription daemon.

Provides a dedicated `user.whisper` mode that minimizes command listening
while transcription is active. While in this mode, only the phrase
"talon whisper done" is recognized (see whisper_mode.talon) to exit.

On entry: unmute the transcription daemon and disable `command` mode.
On exit: mute the daemon and re-enable `command` mode.
"""

from talon import actions, Context, Module
from pathlib import Path
import subprocess

mod = Module()
mod.mode("whisper", desc="Transcription mode for Whisper daemon")

ctx = Context()

REALITIME_DIR = Path("~/repos/realtimestt-cli").expanduser()
REALITIME_CMD = ["./venv/bin/python3", "./realtime_test.py"]
_whisper_proc = None
_whisper_prev_theme = None
_whisper_theme_map = {
    "dark": "dark_whisper",
    "light": "light_whisper",
}


def _notify(msg: str) -> None:
    try:
        actions.user.notify(msg)
    except Exception:
        # In case notify isn't available in this Talon build
        pass


def _proc_is_running() -> bool:
    return _whisper_proc is not None and _whisper_proc.poll() is None


def _start_proc() -> bool:
    global _whisper_proc
    if _proc_is_running():
        return True

    if not REALITIME_DIR.exists():
        _notify(f"Whisper: missing dir {REALITIME_DIR}")
        return False

    try:
        _whisper_proc = subprocess.Popen(REALITIME_CMD, cwd=str(REALITIME_DIR))
        return True
    except Exception:
        _notify("Whisper: failed to start subprocess")
        _whisper_proc = None
        return False


def _stop_proc() -> None:
    global _whisper_proc
    if not _proc_is_running():
        _whisper_proc = None
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
        if not _start_proc():
            return

        # Enable whisper mode alongside command mode
        # Whisper mode commands will override conflicting command mode commands
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
        _stop_proc()

        # Simply disable whisper mode - command mode stays active
        actions.mode.disable("user.whisper")

        # Restore the previous HUD theme if we switched it.
        global _whisper_prev_theme
        if _whisper_prev_theme:
            _switch_hud_theme(_whisper_prev_theme)
        _whisper_prev_theme = None

        _notify("Whisper mode: OFF - console output restored")
