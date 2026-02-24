from pathlib import Path

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
os: linux
app: nautilus
"""


@ctx.action_class("user")
class UserActions:
    def file_manager_open_file(path: str):
        """Open a file in VSCode instead of the OS default app."""
        current_dir = actions.user.file_manager_current_path()
        full_path = Path(path).expanduser()
        if current_dir and not full_path.is_absolute():
            full_path = Path(current_dir) / path
        ui.launch(path="code", args=["--reuse-window", str(full_path)])
