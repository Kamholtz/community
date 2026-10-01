from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def handy_toggle() -> None:
        """Toggle Handy transcription with Ctrl+Space."""
        actions.key("ctrl-space")
