from talon import Module, actions, scope

mod = Module()


@mod.action_class
class Actions:
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