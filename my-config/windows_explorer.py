from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: windows_explorer
app: windows_file_browser
"""


@ctx.action_class("user")
class UserActions:
    def file_manager_open_directory(path: str):
        """opens the directory that's already visible in the view"""
        # Typing immediately after ctrl-l can race the address bar taking
        # focus, dropping the first couple characters (e.g. "%AppData%"
        # becomes "ppData%"). A short sleep avoids that.
        actions.key("ctrl-l")
        actions.sleep("100ms")
        actions.insert(path)
        actions.key("enter")
