from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()


apps = mod.apps
apps.firefox_chatgpt = "app.name: Firefox"
apps.firefox_chatgpt = "app.name: Firefox Developer Edition"
apps.firefox_chatgpt = "app.name: firefox"
apps.firefox_chatgpt = "app.name: org.mozilla.firefox"
apps.firefox_chatgpt = "app.name: Firefox-esr"
apps.firefox_chatgpt = "app.name: firefox-esr"
apps.firefox_chatgpt = "app.name: LibreWolf"
apps.firefox_chatgpt = "app.name: waterfox"
apps.firefox_chatgpt = r"""
os: windows
and app.name: Firefox
os: windows
and app.exe: /^firefox\.exe$/i
"""
apps.firefox_chatgpt = """
os: mac
and app.bundle: org.mozilla.firefox
"""

# Make the context match more specifically than anything else. This is important, eg. to
# override the browser.go_home() implementation in tags/browser/browser_mac.py.
ctx.matches = r"""
os: windows
os: linux
os: mac
tag: browser
app: firefox
win.title: /ChatGPT/
"""


@mod.action_class
class Actions:
    def firefox_bookmarks_sidebar():
        """Toggles the Firefox bookmark sidebar"""

    def firefox_history_sidebar():
        """Toggles the Firefox history sidebar"""


@ctx.action_class("user")
class UserActions:
    def tab_close_wrapper():
        actions.sleep("180ms")
        actions.app.tab_close()


@ctx.action_class("browser")
class BrowserActions:
    def focus_page():
        actions.browser.focus_address()
        actions.edit.find()
        actions.sleep("180ms")
        actions.key("escape")

    def go_home():
        actions.key("alt-home")
