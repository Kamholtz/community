mode: command
mode: user.cursorless_spoken_form_test
tag: user.cursorless
-
# Override the cursorless change command to also enter insert mode.
change <user.cursorless_target>:
    user.cursorless_command("clearAndSetSelection", cursorless_target)
    user.run_rpc_command("vscode-neovim.lua", "vim.cmd('startinsert')")
