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


def _post(path: str, json_data=None):
    try:
        if json_data:
            return requests.post(f"{BASE_URL}{path}", json=json_data, timeout=1.5)
        else:
            return requests.post(f"{BASE_URL}{path}", timeout=1.5)
    except Exception:
        return None


@mod.action_class
class Actions:
    def whisper_start():
        """Enter whisper mode: enable transcription and minimize commands."""
        # Set transcription daemon to type mode
        mode_r = _post("/mode", {"mode": "type"})
        if mode_r is None or getattr(mode_r, "status_code", 500) != 200:
            _notify("Whisper: failed to set type mode")
            return

        # Unmute the transcription daemon
        r = _post("/unmute")
        if r is None or getattr(r, "status_code", 500) != 200:
            _notify("Whisper: failed to unmute daemon")
            return

        # Enable whisper mode alongside command mode
        # Whisper mode commands will override conflicting command mode commands
        actions.mode.enable("user.whisper")

        # Change HUD to green to indicate whisper mode is active
        try:
            actions.user.hud_set_theme("green")
        except Exception:
            # HUD theme setting not available or failed
            pass

        _notify("Whisper mode: ON - typing enabled (say 'talon whisper done' to exit)")

    def whisper_done():
        """Exit whisper mode: mute transcription and restore command mode."""
        # Set transcription daemon to print mode (console output)
        mode_r = _post("/mode", {"mode": "print"})
        if mode_r is None or getattr(mode_r, "status_code", 500) != 200:
            _notify("Whisper: failed to set print mode")
            # Continue anyway, try to mute

        # Mute the transcription daemon
        r = _post("/mute")
        if r is None or getattr(r, "status_code", 500) != 200:
            _notify("Whisper: failed to mute daemon")
            # Still attempt to restore modes

        # Simply disable whisper mode - command mode stays active
        actions.mode.disable("user.whisper")

        # Restore HUD to default theme
        try:
            actions.user.hud_set_theme("default")
        except Exception:
            # HUD theme setting not available or failed
            pass

        _notify("Whisper mode: OFF - console output restored")

