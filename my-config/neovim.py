from talon import Context, Module, actions, app, settings, ui, clip

mod = Module()


@mod.action_class
class Actions:
    def vim_search_commands(search_text: str):
        """Open commands picker"""
        cmd = ":PickCommands " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_files(search_text: str):
        """Open files picker"""
        cmd = ":PickFiles " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_files_clipboard():
        """Open command picker"""
        cmd = ":PickFiles " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)
