
import os
from talon import actions, app, Module

mod = Module()

@mod.action_class
class Actions:
    def open_talon_config_vscode():
        """Opens the Talon user configuration directory in VSCode."""
        config_path = actions.path.talon_user()  # Automatically gets your Talon user directory
        vscode_command = f'code "{config_path}"'  # VSCode command

        # Using os.system for compatibility
        result = os.system(vscode_command)
        if result == 0:
            app.notify("Opened Talon config in VSCode")
        else:
            app.notify("Failed to open Talon config in VSCode")
