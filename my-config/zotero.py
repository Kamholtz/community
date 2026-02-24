from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def zotero_find_selection():
        """Search Zotero for the current selection and preserve the clipboard."""
        selection = actions.edit.selected_text()
        if not selection:
            actions.app.notify("No selection to search for")
            return
        try:
            actions.user.switcher_focus("Zotero")
        except Exception:
            actions.app.notify("Zotero not running")
            return
        actions.sleep("100ms")
        actions.key("ctrl-f")
        actions.sleep("50ms")
        actions.user.paste(selection)
