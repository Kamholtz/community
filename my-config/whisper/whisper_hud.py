"""Talon HUD glue for Whisper mode.

The single seam through which whisper_mode.py talks to the optional
talon_hud package: every function no-ops (returning False) when the HUD is
missing, and failures print one warning instead of dying silently.
"""

from typing import Callable, Optional

from talon import actions, scope

WHISPER_PANEL_TOPIC = "whisper_panel"
WHISPER_PANEL_TITLE = "Whisper"
_CHOICE_WIDGET_ID = "Choices"
_MIN_HUD_VERSION = 6

_warned_calls: set[str] = set()


def hud_available() -> bool:
    try:
        if "user.talon_hud_available" not in (scope.get("tag") or ()):
            return False
        version = scope.get("user.talon_hud_version") or 0
        return version >= _MIN_HUD_VERSION
    except Exception:
        return False


def _warn_once(name: str, error: Exception) -> None:
    if name not in _warned_calls:
        _warned_calls.add(name)
        print(f"whisper_hud: HUD call {name} failed: {error}")


def publish_panel(
    body: str,
    show: bool = False,
    buttons: Optional[list[tuple[str, Callable]]] = None,
) -> bool:
    """Publish the whisper panel; buttons are (text, callback) pairs that
    appear in the panel's right-click menu and as voice commands of the form
    "<panel name> <button text>"."""
    if not hud_available():
        return False
    try:
        hud_buttons = [
            actions.user.hud_create_button(text, callback)
            for text, callback in (buttons or [])
        ]
        actions.user.hud_publish_content(
            body, WHISPER_PANEL_TOPIC, WHISPER_PANEL_TITLE, show, hud_buttons
        )
        return True
    except Exception as error:
        _warn_once("hud_publish_content", error)
        return False


def clear_panel() -> None:
    if not hud_available():
        return
    try:
        # An empty replace releases the wildcard Text panel back to other
        # content; show=False avoids re-opening a panel the user closed.
        actions.user.hud_publish_content(
            "", WHISPER_PANEL_TOPIC, WHISPER_PANEL_TITLE, False
        )
    except Exception as error:
        _warn_once("hud_clear_panel", error)


def publish_history_choices(
    choice_items: list[dict], on_choice: Callable[[Optional[dict]], bool]
) -> bool:
    if not hud_available() or not choice_items:
        return False
    try:
        choices = actions.user.hud_create_choices(choice_items, on_choice, False)
        actions.user.hud_publish_choices(
            choices,
            "Whisper history",
            "Say <*option <number>/> or click to insert an entry",
        )
        return True
    except Exception as error:
        _warn_once("hud_publish_choices", error)
        return False


def hide_choices() -> None:
    if not hud_available():
        return
    try:
        # Same dismissal path the choice panel uses after a pick.
        actions.user.hud_disable_id(_CHOICE_WIDGET_ID)
    except Exception as error:
        _warn_once("hud_disable_id", error)


def add_log(level: str, message: str) -> bool:
    if not hud_available():
        return False
    try:
        actions.user.hud_add_log(level, message)
        return True
    except Exception as error:
        _warn_once("hud_add_log", error)
        return False
