import os

from talon import Context, Module, actions, app, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: windows
"""

FLUENT_SEARCH_EXE = None
FLUENT_SEARCH_APP_NAMES = {"Fluent Search", "FluentSearch"}


def is_fluent_search_app(active_app):
    if active_app is None:
        return False
    if active_app.name in FLUENT_SEARCH_APP_NAMES:
        return True
    return os.path.basename(active_app.exe).lower() == "fluentsearch.exe"


def wait_for_fluent_search_window():
    for attempt in range(20):
        if is_fluent_search_app(ui.active_app()):
            return True
        actions.sleep("50ms")

    app.notify("Gave up while waiting for Fluent Search")
    return False


@mod.action_class
class Actions:
    def fluent_search(text: str):
        """Searches using Fluent Search"""

    def fluent_search_in_app(text: str, submit: bool):
        """Searches using Fluent Search's In-app Search"""


@ctx.action_class("user")
class UserActions:
    def fluent_search(text: str):
        global FLUENT_SEARCH_EXE

        apps = ui.apps(name="Fluent Search")
        if len(apps) == 0:
            if FLUENT_SEARCH_EXE is not None:
                app.notify("Fluent Search is not running; relaunching...")
                os.startfile(FLUENT_SEARCH_EXE)
            else:
                app.notify("Fluent Search is not running; please (re)launch it")
                return
        else:
            FLUENT_SEARCH_EXE = apps[0].exe
        # XXX can't use app.focus() and unaware of any other way to
        # automate the way we do with LaunchBar
        # If you have a different search keyboard shortcut configured,
        # replace ctrl-alt-space with it below.
        actions.key("ctrl-alt")
        if not wait_for_fluent_search_window():
            return
        actions.key("backspace")
        print("text=" + text)
        if "\t" in text:
            plugin, text = text.split("\t", 1)
            print("plugin=" + plugin)
            actions.insert(plugin)
            actions.sleep("100ms")
            actions.insert("\t")
        print("text=" + text)
        actions.user.paste(text)

    def fluent_search_in_app(text: str, submit: bool):
        actions.key("shift-super")
        if not wait_for_fluent_search_window():
            return
        actions.user.paste(text)
        if submit:
            actions.key("enter")
