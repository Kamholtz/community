mode: command
mode: dictation
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
    user.code_clear_language_mode()
    user.gdb_disable()
^command (mode|marred|married|mud|merge)$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")
