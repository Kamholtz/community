from talon import Module, actions, scope

mod = Module()

_f1_uses_handy = False
_handy_transcribing = False


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

    def toggle_handy_transcription() -> None:
        """Toggle Handy transcription and track its state."""
        global _handy_transcribing

        actions.user.handy_toggle()
        _handy_transcribing = not _handy_transcribing

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
