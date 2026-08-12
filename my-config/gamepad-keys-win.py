from talon import Module

DEBUG = True

mod = Module()


@mod.action_class
class Actions:
    def gamepad_debug(text: str):
        """Print debug text when gamepad debug mode is enabled."""
        if DEBUG:
            print(text)

    def gamepad_toggle_control_mouse_or_quick_pick():
        """Enable eye tracking, or toggle quick pick when it is unavailable or enabled."""
        from talon import actions

        if actions.tracking.control_enabled():
            actions.user.quick_pick_show_or_app_show()
        else:
            actions.tracking.control_toggle(True)
            if not actions.tracking.control_enabled():
                actions.user.quick_pick_show_or_app_show()
