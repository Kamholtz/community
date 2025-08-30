"""
Talon integration for Whisper transcription daemon.

Provides a dedicated `user.whisper` mode that minimizes command listening
while transcription is active. While in this mode, only the phrase
"talon whisper done" is recognized (see whisper_mode.talon) to exit.

On entry: unmute the transcription daemon and disable `command` mode.
On exit: mute the daemon and re-enable `command` mode.
"""

from talon import actions, Context, Module
import requests

mod = Module()
mod.mode("whisper", desc="Transcription mode for Whisper daemon")

ctx = Context()

# Base URL for transcription daemon HTTP API
BASE_URL = "http://localhost:8080"


def _notify(msg: str) -> None:
    try:
        actions.user.notify(msg)
    except Exception:
        # In case notify isn't available in this Talon build
        pass


def _post(path: str):
    try:
        return requests.post(f"{BASE_URL}{path}", timeout=1.5)
    except Exception:
        return None


@mod.action_class
class Actions:
    def whisper_start():
        """Enter whisper mode: enable transcription and minimize commands."""
        # Unmute the transcription daemon first
        r = _post("/unmute")
        if r is None or getattr(r, "status_code", 500) != 200:
            _notify("Whisper: failed to contact daemon")
            return

        # Switch Talon modes: turn off command, enable whisper
        try:
            actions.mode.disable("command")
        except Exception:
            # Some configs auto-manage command mode; proceed regardless
            pass
        actions.mode.enable("user.whisper")
        _notify("Whisper mode: ON (say 'talon whisper done' to exit)")

    def whisper_done():
        """Exit whisper mode: mute transcription and restore command mode."""
        # Mute the transcription daemon
        r = _post("/mute")
        if r is None or getattr(r, "status_code", 500) != 200:
            _notify("Whisper: failed to contact daemon")
            # Still attempt to restore modes
        
        # Restore Talon modes
        actions.mode.disable("user.whisper")
        try:
            actions.mode.enable("command")
        except Exception:
            pass
        _notify("Whisper mode: OFF")

