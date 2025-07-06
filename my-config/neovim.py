from talon import Context, Module, actions, app, settings, ui, clip

mod = Module()


@mod.action_class
class Actions:
    def vim_search_commands(search_text: str):
        """Open commands picker"""
        cmd = ":PickCommands " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_commands_clipboard(search_text: str):
        """Open commands picker"""
        cmd = ":PickCommands " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_files(search_text: str):
        """Open files picker"""
        cmd = ":PickFiles " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_files_clipboard():
        """Open command picker"""
        cmd = ":PickFiles " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_recent(search_text: str):
        """Open recent picker"""
        cmd = ":PickRecent " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_recent_clipboard():
        """Open recent picker"""
        cmd = ":PickRecent " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_buffers(search_text: str):
        """Open buffers picker"""
        cmd = ":PickBuffers " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_buffers_clipboard():
        """Open buffers picker"""
        cmd = ":PickBuffers " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_undo(search_text: str):
        """Open undo picker"""
        cmd = ":PickUndo " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_undo_clipboard():
        """Open undo picker"""
        cmd = ":PickUndo " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_marks(search_text: str):
        """Open marks picker"""
        cmd = ":PickMarks " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_marks_clipboard():
        """Open marks picker"""
        cmd = ":PickMarks " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_command_history(search_text: str):
        """Open command history picker"""
        cmd = ":PickCommandHistory " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_command_history_clipboard():
        """Open command history picker"""
        cmd = ":PickCommandHistory " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_search_history(search_text: str):
        """Open search history picker"""
        cmd = ":PickSearchHistory " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_search_history_clipboard():
        """Open search history picker"""
        cmd = ":PickSearchHistory " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_grep(search_text: str):
        """Open grep picker"""
        cmd = ":PickGrep " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_grep_clipboard():
        """Open grep picker"""
        cmd = ":PickGrep " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_grep_word(search_text: str):
        """Open grep word picker"""
        cmd = ":PickGrepWord " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_grep_word_clipboard():
        """Open grep word picker"""
        cmd = ":PickGrepWord " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lines(search_text: str):
        """Open lines picker"""
        cmd = ":PickLines " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lines_clipboard():
        """Open lines picker"""
        cmd = ":PickLines " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_diagnostics(search_text: str):
        """Open diagnostics picker"""
        cmd = ":PickDiagnostics " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_diagnostics_clipboard():
        """Open diagnostics picker"""
        cmd = ":PickDiagnostics " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_help(search_text: str):
        """Open help picker"""
        cmd = ":PickHelp " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_help_clipboard():
        """Open help picker"""
        cmd = ":PickHelp " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_jumps(search_text: str):
        """Open jumps picker"""
        cmd = ":PickJumps " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_jumps_clipboard():
        """Open jumps picker"""
        cmd = ":PickJumps " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_loclist(search_text: str):
        """Open loclist picker"""
        cmd = ":PickLoclist " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_loclist_clipboard():
        """Open loclist picker"""
        cmd = ":PickLoclist " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_resume(search_text: str):
        """Open resume picker"""
        cmd = ":PickResume " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_resume_clipboard():
        """Open resume picker"""
        cmd = ":PickResume " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_qf_list(search_text: str):
        """Open quickfix list picker"""
        cmd = ":PickQfList " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_qf_list_clipboard():
        """Open quickfix list picker"""
        cmd = ":PickQfList " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_definitions(search_text: str):
        """Open LSP definitions picker"""
        cmd = ":PickLspDefinitions " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_definitions_clipboard():
        """Open LSP definitions picker"""
        cmd = ":PickLspDefinitions " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_references(search_text: str):
        """Open LSP references picker"""
        cmd = ":PickLspReferences " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_references_clipboard():
        """Open LSP references picker"""
        cmd = ":PickLspReferences " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_implementations(search_text: str):
        """Open LSP implementations picker"""
        cmd = ":PickLspImplementations " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_implementations_clipboard():
        """Open LSP implementations picker"""
        cmd = ":PickLspImplementations " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_type_definitions(search_text: str):
        """Open LSP type definitions picker"""
        cmd = ":PickLspTypeDefinitions " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_type_definitions_clipboard():
        """Open LSP type definitions picker"""
        cmd = ":PickLspTypeDefinitions " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_symbols(search_text: str):
        """Open LSP symbols picker"""
        cmd = ":PickLspSymbols " + search_text + "\n"
        actions.user.vim_run_normal_np(cmd)

    def vim_search_lsp_symbols_clipboard():
        """Open LSP symbols picker"""
        cmd = ":PickLspSymbols " + clip.text() + "\n"
        actions.user.vim_run_normal_np(cmd)


# "PickRecent"
# "PickBuffers"
# "PickUndo"
# "PickMarks"
# "PickCommandHistory"
# "PickSearchHistory"
# "PickGrep"
# "PickGrepWord"
# "PickLines"
# "PickDiagnostics"
# "PickHelp"
# "PickJumps"
# "PickLoclist"
# "PickResume"
# "PickQfList"
# "PickLspDefinitions"
# "PickLspReferences"
# "PickLspImplementations"
# "PickLspTypeDefinitions"
# "PickLspSymbols"
