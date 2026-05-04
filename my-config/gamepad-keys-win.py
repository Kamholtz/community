from talon import Module

DEBUG = False

mod = Module()


@mod.action_class
class Actions:
    def gamepad_debug(text: str):
        """Print debug text when gamepad debug mode is enabled."""
        if DEBUG:
            print(text)

    def gamepad_toggle_control_mouse_or_quick_pick():
        """Enable eye tracking or show quick pick when eye tracking is already enabled."""
        from talon import actions

        if actions.tracking.control_enabled():
            actions.user.quick_pick_show()
        else:
            actions.tracking.control_toggle(True)
