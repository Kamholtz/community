from talon import Module, actions

mod = Module()
mod.tag("glazewm", desc="Tag for enabling GlazeWM voice commands")


@mod.action_class
class Actions:
    def glazewm_focus(direction: str):
        """Focus window in a direction: left/right/up/down"""
        mapping = {
            "left": "alt-left",
            "right": "alt-right",
            "up": "alt-up",
            "down": "alt-down",
        }
        if direction in mapping:
            actions.key(mapping[direction])

    def glazewm_move(direction: str):
        """Move the focused window left/right/up/down"""
        mapping = {
            "left": "alt-shift-left",
            "right": "alt-shift-right",
            "up": "alt-shift-up",
            "down": "alt-shift-down",
        }
        if direction in mapping:
            actions.key(mapping[direction])

    def glazewm_resize(which: str):
        """Resize window: 'narrower'|'wider'|'taller'|'shorter'"""
        mapping = {
            "narrower": "alt-u",   # width -2%
            "wider": "alt-p",      # width +2%
            "taller": "alt-o",     # height +2%
            "shorter": "alt-i",    # height -2%
        }
        if which in mapping:
            actions.key(mapping[which])

    def glazewm_resize_mode():
        """Enter GlazeWM resize binding mode"""
        actions.key("alt-r")

    def glazewm_resize_mode_exit():
        """Exit GlazeWM resize binding mode"""
        actions.key("escape")

    def glazewm_toggle_pause():
        """Toggle GlazeWM pause (disable/enable bindings)"""
        actions.key("alt-shift-p")

    def glazewm_toggle_tiling_direction():
        """Toggle tiling insertion direction"""
        actions.key("alt-v")

    def glazewm_cycle_focus():
        """Cycle focus tiling→floating→fullscreen"""
        actions.key("alt-space")

    def glazewm_toggle_floating():
        """Toggle floating for focused window (centered)"""
        actions.key("alt-shift-space")

    def glazewm_toggle_tiling():
        """Toggle tiling for focused window"""
        actions.key("alt-t")

    def glazewm_toggle_fullscreen():
        """Toggle fullscreen for focused window"""
        actions.key("alt-f")

    def glazewm_toggle_minimized():
        """Toggle minimized state for focused window"""
        actions.key("alt-m")

    def glazewm_close():
        """Close focused window"""
        actions.key("alt-shift-q")

    def glazewm_exit():
        """Exit GlazeWM process"""
        actions.key("alt-shift-e")

    def glazewm_reload_config():
        """Reload GlazeWM configuration"""
        actions.key("alt-shift-r")

    def glazewm_redraw():
        """Redraw all windows"""
        actions.key("alt-shift-w")

    def glazewm_launch_shell():
        """Launch default shell (cmd)"""
        actions.key("alt-enter")

    def glazewm_workspace_next():
        """Focus next active workspace"""
        actions.key("alt-s")

    def glazewm_workspace_prev():
        """Focus previous active workspace"""
        actions.key("alt-a")

    def glazewm_workspace_recent():
        """Focus most recently focused workspace"""
        actions.key("alt-d")

    def glazewm_workspace_focus(number: int):
        """Focus workspace number 1-9"""
        actions.key(f"alt-{number}")

    def glazewm_move_to_workspace(number: int):
        """Move focused window to workspace number 1-9"""
        actions.key(f"alt-shift-{number}")

    def glazewm_move_workspace(direction: str):
        """Move current workspace between monitors: left/right/up/down"""
        mapping = {
            "left": "alt-shift-a",
            "right": "alt-shift-f",
            "up": "alt-shift-d",
            "down": "alt-shift-s",
        }
        if direction in mapping:
            actions.key(mapping[direction])
