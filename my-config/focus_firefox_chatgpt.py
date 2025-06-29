from talon import Module, ui, actions

mod = Module()


@mod.action_class
class Actions:
    def focus_firefox_chatgpt():
        """Brings the ChatGPT Firefox window into focus"""
        for window in ui.windows():
            if (
                window.app
                and "firefox" in window.app.name.lower()
                and "ChatGPT" in window.title
            ):
                window.focus()
                return
        # Optional: Notify if window not found
        actions.app.notify("ChatGPT window not found")
