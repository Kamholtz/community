import json
from pathlib import Path

from talon import Module, actions, app, scope

mod = Module()

_f1_uses_handy = False
_handy_transcribing = False
_TRANSCRIPTION_HUD_TOPIC = "transcription_mode"


class TranscriptionHudButton:
    """Persist the visibility preference for the transcription HUD icon."""

    def __init__(self, path: Path, hud_actions, refresh, image):
        self.path = path
        self.actions = hud_actions
        self.refresh = refresh
        self.image = image
        self.hidden = False
        if path.exists():
            try:
                self.hidden = bool(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, ValueError) as error:
                print(f"transcription_hud: could not load button preference: {error}")

    def set_visible(self, visible: bool) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(not visible), encoding="utf-8")
        temporary.replace(self.path)
        self.hidden = not visible
        if not visible:
            self.actions.hud_remove_status_icon(_TRANSCRIPTION_HUD_TOPIC)
        self.refresh()

    def publish_icon(self, icon) -> None:
        if self.hidden:
            self.actions.hud_remove_status_icon(_TRANSCRIPTION_HUD_TOPIC)
        else:
            self.actions.hud_publish_status_icon(_TRANSCRIPTION_HUD_TOPIC, icon)

    def publish_option(self) -> None:
        visible = not self.hidden
        button = self.actions.hud_create_button(
            f"{'Remove' if visible else 'Add'} transcription mode",
            lambda *_args: self.set_visible(not visible),
            self.image(),
        )
        option = self.actions.hud_create_status_option(
            _TRANSCRIPTION_HUD_TOPIC, button, button
        )
        self.actions.hud_publish_status_option(
            f"{_TRANSCRIPTION_HUD_TOPIC}_option", option
        )


@mod.action_class
class Actions:
    def toggle_f1_input_mode() -> None:
        """Run F1's selected input-mode toggle."""

        if not _f1_uses_handy:
            actions.user.toggle_command_dictation_mode()
            return

        actions.user.toggle_handy_transcription()

    def toggle_f1_handy_mode() -> None:
        """Choose whether F1 toggles native dictation or Handy transcription."""
        global _f1_uses_handy, _handy_transcribing

        if _f1_uses_handy and _handy_transcribing:
            actions.user.toggle_handy_transcription()

        _f1_uses_handy = not _f1_uses_handy
        _publish_transcription_hud_button()

    def toggle_handy_transcription() -> None:
        """Toggle Handy transcription and track its state."""
        global _handy_transcribing

        actions.user.handy_toggle()
        _handy_transcribing = not _handy_transcribing
        if _handy_transcribing:
            actions.speech.disable()
        else:
            actions.speech.enable()
        _publish_transcription_hud_button()

    def transcription_hud_refresh_button() -> None:
        """Republish the transcription-mode HUD control."""
        _publish_transcription_hud_button()

    def toggle_command_dictation_mode() -> None:
        """Toggle between command and dictation modes."""
        active_modes = set(scope.get("mode") or [])

        # Keep the toggle focused on awake modes.
        try:
            actions.mode.disable("sleep")
        except Exception:
            pass

        if "dictation" in active_modes:
            actions.mode.disable("dictation")
            actions.mode.enable("command")
            _publish_transcription_hud_button()
            return

        actions.mode.disable("command")
        actions.mode.enable("dictation")

        try:
            actions.user.code_clear_language_mode()
        except Exception:
            pass

        try:
            actions.user.gdb_disable()
        except Exception:
            pass

        _publish_transcription_hud_button()


def _transcription_hud_details() -> tuple[str, str]:
    if _f1_uses_handy:
        if _handy_transcribing:
            return "microphone_on", "Stop Handy transcription"
        return "microphone_off", "Start Handy transcription"

    active_modes = set(scope.get("mode") or [])
    if "dictation" in active_modes:
        return "dictation_icon", "Switch to command mode (Talon dictation)"
    return "command_icon", "Switch to Talon dictation mode"


def _transcription_hud_image() -> str:
    return _transcription_hud_details()[0]


def _publish_transcription_hud_button(*_args) -> None:
    image, accessible_name = _transcription_hud_details()
    try:
        _transcription_hud_button.publish_option()
        icon = actions.user.hud_create_status_icon(
            _TRANSCRIPTION_HUD_TOPIC,
            image,
            None,
            accessible_name,
            actions.user.toggle_f1_input_mode,
        )
        _transcription_hud_button.publish_icon(icon)
    except Exception:
        # The HUD is optional and may not yet be ready during module reload.
        pass


_transcription_hud_button = TranscriptionHudButton(
    Path(__file__).resolve().parents[1]
    / "stored_state"
    / "transcription_hud_button.json",
    actions.user,
    _publish_transcription_hud_button,
    _transcription_hud_image,
)

app.register("ready", _publish_transcription_hud_button)
_publish_transcription_hud_button()
