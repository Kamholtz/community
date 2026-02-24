
import os
from talon import actions, app, Module, settings

mod = Module()

@mod.action_class
class Actions:
    def open_talon_config_vscode():
        """Opens the Talon user configuration directory in VSCode."""
        config_path = actions.path.talon_home()  # Automatically gets your Talon user directory
        vscode_command = f'code "{config_path}/user.code-workspace"'  # VSCode command

        # Using os.system for compatibility
        result = os.system(vscode_command)
        if result == 0:
            app.notify("Opened Talon config in VSCode")
        else:
            app.notify(f"Failed to open Talon config in VSCode {config_path}")

    def toggle_hiss_scroll():
        """Toggle hiss scrolling on/off."""
        setting_name = "user.mouse_enable_hiss_scroll"
        enabled = bool(settings.get(setting_name))
        settings.set(setting_name, not enabled)
        app.notify(f"Hiss scroll {'enabled' if not enabled else 'disabled'}")
