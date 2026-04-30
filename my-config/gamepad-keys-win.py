from talon import Module

DEBUG = False

mod = Module()


@mod.action_class
class Actions:
    def gamepad_debug(text: str):
        """Print debug text when gamepad debug mode is enabled."""
        if DEBUG:
            print(text)
