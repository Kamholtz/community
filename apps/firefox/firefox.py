from talon import Context, Module, actions, app, ui

ctx = Context()
mod = Module()


mod.tag("firefox_chatgpt", desc="Tag for Firefox windows with ChatGPT open")


apps = mod.apps
apps.firefox = "app.name: Firefox"
apps.firefox = "app.name: Firefox Developer Edition"
apps.firefox = "app.name: firefox"
apps.firefox = "app.name: org.mozilla.firefox"
apps.firefox = "app.name: Firefox-esr"
apps.firefox = "app.name: firefox-esr"
apps.firefox = "app.name: LibreWolf"
apps.firefox = "app.name: waterfox"
apps.firefox = r"""
os: windows
and app.name: Firefox
os: windows
and app.exe: /^firefox\.exe$/i
"""
apps.firefox = """
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


def update_firefox_tag(app_obj, window):
    print(window.title())
    if window and "ChatGPT" in window.title():
        ctx.tags = ["firefox_chatgpt"]
    else:
        ctx.tags = []


def win_event_handler(window):
    global cached_path

    print("win_event_handler: window.title=" + window.title)
    if window and "ChatGPT" in window.title:
        print("adding tag firefox_chatgpt")
        ctx.tags = ["firefox_chatgpt"]
    else:
        print("removing tag firefox_chatgpt")
        ctx.tags = []

    # on windows, we get events from the clock
    # and such, so this check is important
    if not window.app.exe or window != ui.active_window():
        return


def register_events():
    print("register_events")
    ui.register("win_title", win_event_handler)
    ui.register("win_focus", win_event_handler)


print("refresh...")

# Register app and window focus hooks
app.register("ready", register_events)
# app.register("win_focus", update_firefox_tag)
