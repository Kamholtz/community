from pathlib import Path

from talon import Context, actions, app, cron, scope

THEME_DIRS = {
    "dark_whisper": Path(__file__).resolve().parent / "talon_hud_themes" / "dark_whisper",
    "light_whisper": Path(__file__).resolve().parent / "talon_hud_themes" / "light_whisper",
}

ctx = Context()
ctx.matches = """
tag: user.talon_hud_available
"""


def _register_whisper_theme(attempt: int = 0) -> None:
    registered_all = True
    for theme_name, theme_dir in THEME_DIRS.items():
        if not theme_dir.is_dir():
            continue

        try:
            actions.user.hud_register_theme(theme_name, str(theme_dir))
        except Exception:
            registered_all = False

    # The HUD can finish loading after Talon's ready event. Retry briefly so a
    # full Talon restart behaves the same as a script reload.
    if not registered_all and attempt < 20:
        cron.after("500ms", lambda: _register_whisper_theme(attempt + 1))


app.register("ready", _register_whisper_theme)
_register_whisper_theme()


@ctx.action_class("user")
class Actions:
    def hud_get_status_modes() -> list[str]:
        """Include whisper mode so the HUD can theme it."""
        return ["user.whisper", "sleep", "dictation", "command"]

    def hud_determine_mode() -> str:
        """Prefer whisper mode for HUD theming even if sleep is also active."""
        active_modes = scope.get("mode")
        if active_modes and "user.whisper" in active_modes:
            return "user.whisper"

        current_mode = "command"
        for available_mode in actions.user.hud_get_status_modes():
            if active_modes and available_mode in active_modes:
                current_mode = available_mode
                break

        if active_modes and "command" in active_modes and current_mode == "dictation":
            current_mode = "mixed"

        return current_mode

    def hud_toggle_mode():
        """Allow the mode toggle to work while whisper mode is active."""
        current_mode = actions.user.hud_determine_mode()
        if current_mode in ["command", "dictation", "mixed", "user.whisper"]:
            actions.speech.disable()
        elif current_mode == "sleep":
            actions.speech.enable()
