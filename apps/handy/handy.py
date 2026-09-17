from talon import Module, actions

mod = Module()

_transcribing = False


@mod.action_class
class Actions:
    def handy_toggle() -> None:
        """Toggle Handy transcription: hold ctrl-space to start recording, release it to stop."""
        global _transcribing

        if _transcribing:
            actions.key("ctrl-space:up")
            _transcribing = False
            actions.speech.enable()
        else:
            actions.key("ctrl-space:down")
            _transcribing = True
            actions.speech.disable()
