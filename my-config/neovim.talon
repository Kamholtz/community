tag: user.vim_mode_insert
tag: user.vim_mode_normal
-  

tag(): user.cursorless

# settings():
#     # Whether or not to always revert back to the previous mode. Example, if
#     # you are in insert mode and say 'delete word' it will delete one word and
#     # keep you in insert mode. Same as ctrl-o in VIM.
#     user.vim_preserve_insert_mode = 1

#     # Whether or not to automatically adjust modes when using commands. Example
#     # saying "go line 50" will first switch you out of INSERT into NORMAL and
#     # then jump to the line. Disabling this setting would put :50\n into your
#     # file if you say "row 50" while in INSERT mode.
#     user.vim_adjust_modes = 1

#     # Select whether or not talon should dispatch notifications on mode changes
#     # that are made. Not yet completed, as notifications are kind of wonky on
#     # Linux
#     user.vim_notify_mode_changes = 0

#     # Whether or not all commands that transfer out of insert mode should also
#     # automatically escape out of terminal mode. Turning this on is quite
#     # troublesome.
#     user.vim_escape_terminal_mode = 0

#     # When issuing counted actions in vim you can prefix a count that will
#     # dictate how many times the command is run, however some peoples talon
#     # grammar already allows you to utter a number without a prefix (ex: voice
#     # command "ten" will put 10 in your file) so we want to cancel any existing
#     # counts that might already by queued in vim in error.
#     #
#     # This also helps prevent accidental number queueing if talon
#     # mishears a command such as "delete line" as "delete" "nine". Without this
#     # setting, if you then said "undo" it would undo the last 9 changes, which
#     # is annoying.
#     #
#     # This setting only applies to commands run through the actual counted
#     # actions grammar itself
#     user.vim_cancel_queued_commands = 1

#     # When you are escaping queued commands, it seems vim needs time to recover
#     # before issuing the subsequent commands. This controls how long it waits,
#     # in seconds
#     user.vim_cancel_queued_commands_timeout = 0.20

#     # It how long to wait before issuing commands after a mode change. You
#     # want adjust this if when you say things like undo from INSERT mode, an
#     # "u" gets inserted into INSERT mode. It in theory that shouldn't be
#     # required if using pynvim.
#     user.vim_mode_change_timeout = 0.25

#     # When you preserve mode and switch into into insert mode it will often
#     # move your cursor, which can mess up the commands you're trying to run from
#     # insert. This setting controls the cursor move
#     user.vim_mode_switch_moves_cursor = 0

#     # Whether or not use pynvim rpc if it is available
#     user.vim_use_rpc = 1

#     # Adds debug output to the talon log
#     user.vim_debug = 0

(dup | duplicate) line:
    user.vim_run_normal_np("yy")
    user.vim_run_normal_np("p")

change quote:
    user.vim_run_normal_np("ciq")

change word:
    user.vim_run_normal_np("ciw")

change (nibble|inner word):
    user.vim_run_normal_np("civ")

change para:
    user.vim_run_normal_np("cip")

toggle comment:
    user.vim_run_normal_np("gcc")

# =====================================
# Git
# =====================================

(G | git) status:
    user.vim_normal_mode(" gg")

(G | git) status:
    user.vim_run_normal_np(" gg")

(G | git) push:
    user.vim_run_normal_np(" gkk")

(G | git) pull:
    user.vim_run_normal_np(" gjj")

(G | git) stage:
    user.vim_run_normal_np(" hs")

(G | git) stage file:
    user.vim_run_normal_np(" hS")

(G | git) ref log:
    user.vim_run_normal_np(":Flog\n")

(G | git) worktrees:
    user.vim_run_normal_np(":TelescopeGitWorkTrees\n")

(G | git) commit feature:
    user.vim_run_normal_np(":GitCommitFeat\n")

(G | git) commit wip:
    user.vim_run_normal_np(":GitCommitWip\n")

(G | git) commit fix:
    user.vim_run_normal_np(":GitCommitFix\n")

(G | git) commit refactor:
    user.vim_run_normal_np(":GitCommitRefactor\n")

(G | git) commit format:
    user.vim_run_normal_np(":GitCommitFormat\n")

(G | git) verbose commit (feature|feat):
    user.vim_run_normal_np(":GitVerboseCommit feat\n")

(G | git) verbose commit fix:
    user.vim_run_normal_np(":GitVerboseCommit fix\n")

(G | git) verbose commit refactor:
    user.vim_run_normal_np(":GitVerboseCommit refactor\n")

(G | git) verbose commit wip:
    user.vim_run_normal_np(":GitVerboseCommit wip\n")

(G | git) verbose commit format:
    user.vim_run_normal_np(":GitVerboseCommit format\n")

fugitive (close|hide|kill):
    user.vim_run_normal_np(":CloseFugitive\n")

copy git branch:
    user.vim_run_normal_np(" cgb")

# =====================================
# Tab
# =====================================

tab close:
    user.vim_run_normal_np(":tabclose\n")

tab new:
    user.vim_run_normal_np(":tabnew\n")

tab only:
    user.vim_run_normal_np(":tabonly\n")

# =====================================
# Window
# =====================================

(win|window) only:
    user.vim_run_normal_np(":only\n")

(win|window) split (h|horizontal):
    user.vim_run_normal_np(":split\n")

(win|window) split (v|vertical):
    user.vim_run_normal_np(":vsplit\n")

    
# =====================================
# Report
# =====================================

Write Report Temp:
    user.vim_run_normal_np(":WriteReportTemp\n")

# =====================================
# Highlight
# =====================================

highlight that:
    user.vim_run_normal_np(":Hi+\n")

unhighlight that:
    user.vim_run_normal_np(":Hi-\n")

# =====================================
# LSP
# =====================================

(definition|def) show:
    user.vim_run_normal_np("gd")

(quick|quick fix) show:
    user.vim_run_normal_np("xq")

(loc|loc fix) show:
    user.vim_run_normal_np("xl")

(definition|def) split:
    key("ctrl-w")
    key("]")

(ref|references|reference) find:
    user.vim_run_normal_np(" lr")

code action:
    user.vim_run_normal_np(" la")


# =====================================
# Please commands
# =====================================

^please (pace | paste)$:
    user.vim_search_commands_clipboard()

^please [<user.text>]$:
    user.vim_search_commands(user.text or "")

# =====================================
# Hunt commands
# =====================================

hunt this (pace | paste):
    key("/")
    edit.paste()

hunt this [<user.text>]:
    user.vim_run_normal_np("/{user.text or ''}")

file hunt (pace | paste):
    user.vim_search_files_clipboard()

file hunt [<user.text>]:
    user.vim_search_files(user.text or "")

recent hunt (pace | paste):
    user.vim_search_recent_clipboard()

recent hunt [<user.text>]:
    user.vim_search_recent(user.text or "")

buffers hunt (pace | paste):
    user.vim_search_buffers_clipboard()

buffers hunt [<user.text>]:
    user.vim_search_buffers(user.text or "")

undo hunt (pace | paste):
    user.vim_search_undo_clipboard()

undo hunt [<user.text>]:
    user.vim_search_undo(user.text or "")

marks hunt (pace | paste):
    user.vim_search_marks_clipboard()

marks hunt [<user.text>]:
    user.vim_search_marks(user.text or "")

command history hunt (pace | paste):
    user.vim_search_command_history_clipboard()

command history hunt [<user.text>]:
    user.vim_search_command_history(user.text or "")

search history hunt (pace | paste):
    user.vim_search_search_history_clipboard()

search history hunt [<user.text>]:
    user.vim_search_search_history(user.text or "")

grep hunt (pace | paste):
    user.vim_search_grep_clipboard()

grep hunt [<user.text>]:
    user.vim_search_grep(user.text or "")

grep word hunt (pace | paste):
    user.vim_search_grep_word_clipboard()

grep word hunt [<user.text>]:
    user.vim_search_grep_word(user.text or "")

lines hunt (pace | paste):
    user.vim_search_lines_clipboard()

lines hunt [<user.text>]:
    user.vim_search_lines(user.text or "")

diagnostics hunt (pace | paste):
    user.vim_search_diagnostics_clipboard()

diagnostics hunt [<user.text>]:
    user.vim_search_diagnostics(user.text or "")

help hunt (pace | paste):
    user.vim_search_help_clipboard()

help hunt [<user.text>]:
    user.vim_search_help(user.text or "")

jumps hunt (pace | paste):
    user.vim_search_jumps_clipboard()

jumps hunt [<user.text>]:
    user.vim_search_jumps(user.text or "")

loclist hunt (pace | paste):
    user.vim_search_loclist_clipboard()

loclist hunt [<user.text>]:
    user.vim_search_loclist(user.text or "")

resume hunt (pace | paste):
    user.vim_search_resume_clipboard()

resume hunt [<user.text>]:
    user.vim_search_resume(user.text or "")

quickfix hunt (pace | paste):
    user.vim_search_qf_list_clipboard()

quickfix hunt [<user.text>]:
    user.vim_search_qf_list(user.text or "")

(definitions|definition|def) hunt (pace | paste):
    user.vim_search_lsp_definitions_clipboard()

(definitions|definition|def) hunt [<user.text>]:
    user.vim_search_lsp_definitions(user.text or "")

(references|reference|ref) hunt (pace | paste):
    user.vim_search_lsp_references_clipboard()

(references|reference|ref) hunt [<user.text>]:
    user.vim_search_lsp_references(user.text or "")

implementations hunt (pace | paste):
    user.vim_search_lsp_implementations_clipboard()

implementations hunt [<user.text>]:
    user.vim_search_lsp_implementations(user.text or "")

type definitions hunt (pace | paste):
    user.vim_search_lsp_type_definitions_clipboard()

type definitions hunt [<user.text>]:
    user.vim_search_lsp_type_definitions(user.text or "")

symbols hunt (pace | paste):
    user.vim_search_lsp_symbols_clipboard()

symbols hunt [<user.text>]:
    user.vim_search_lsp_symbols(user.text or "")

(jump|jumps) hunt (pace | paste):
    user.vim_search_jumps_clipboard()

(jumps) hunt [<user.text>]:
    user.vim_search_jumps(user.text or "")

# =====================================
# Next/previous commands
# =====================================

(niff|next change):
    user.vim_run_normal_np("]c")

(piff|prev change):
    user.vim_run_normal_np("[c")

sig show:
    user.vim_run_normal_np(" lh")


# =====================================
# Cusorless line commands
# =====================================

# G status:
#     user.vim_run_normal_np(":G\n")

# # "drink <TARGET>": Inserts a new line above the target line, and moves the cursor to the newly created line
# drink line:
#     user.vim_run_normal_np("O")
#     key("escape")
# # "pour <TARGET>": Inserts a new line below the target line, and moves the cursor to the newly created line
# pour line:
#     user.vim_run_normal_np("s")
#     key("escape")
# # "drop <TARGET>": Inserts an empty line above the target line (without moving the cursor)
# drop line:
#     user.vim_run_normal_np("[ ")
# # "float <TARGET>": Inserts an empty line below the target line (without moving the cursor)
# float line:
#     user.vim_run_normal_np("] ")
# # "puff <TARGET>": Inserts empty lines/spaces around the target (without moving the cursor)
# puff line:
#     user.vim_run_normal_np("[ ] ")

(dup | duplicate) line:
    user.vim_run_normal_np("yyp")

yank line:
    user.vim_run_normal_np("yy")

push:
    key('end')

push <user.key_unmodified>:
    key('end')
    key('{key_unmodified}')

push it:
    key('end')
    edit.paste()

source file:
    user.vim_run_normal_np(":source %")

(disk|save file):
    user.vim_run_normal_np(":w\n")

nope:
    user.vim_run_normal_np("u")

yep:
    key("ctrl-r")

go back: 
    key("ctrl-o")

go forward: 
    key("ctrl-i")

take element block: 
    user.vim_run_normal_np("vatV")

chuck pair: 
    user.vim_run_normal_np("dab")

chuck inside pair: 
    user.vim_run_normal_np("dib")

void repack pair: 
    user.vim_run_normal_np("dsb")


north:
    user.vim_run_normal_np("S")

south:
    user.vim_run_normal_np("s")

copy remote word:
    user.vim_run_normal_np('yirw')

bring remote word:
    user.vim_run_normal_np('""yirw')

copy remote funk:
    user.vim_run_normal_np('yarf')

bring remote funk:
    user.vim_run_normal_np('""yarf')

copy remote arg:
    user.vim_run_normal_np("yara")

bring remote arg:
    user.vim_run_normal_np('""yara')

clone next arg:
    user.vim_run_normal_np('gmana')

clone (prev|previous) arg:
    user.vim_run_normal_np('gmala')

# Delete remote text objects
delete remote word:
    user.vim_run_normal_np('dirw')

delete remote funk:
    user.vim_run_normal_np('darf')

delete remote arg:
    user.vim_run_normal_np('dara')

# Change remote text objects
change remote word:
    user.vim_run_normal_np('cirw')

change remote funk:
    user.vim_run_normal_np('carf')

change remote arg:
    user.vim_run_normal_np('cara')

# Debug log
debug log remote word:
    user.vim_run_normal_np('g?rv')

debug log remote funk:
    user.vim_run_normal_np('carf')

debug log remote arg:
    user.vim_run_normal_np('cara')


# =====================================
# Markdown
# =====================================
check box tick: user.check_box_tick()
check box untick: user.check_box_untick()


# =====================================
# Mini files
# =====================================
mini files:
    user.vim_run_normal_np(':MyMiniFilesOpen\n')

mini files current:
    user.vim_run_normal_np(':lua MiniFiles.open()\n')


# =====================================
# Fold 
# =====================================
toggle fold [that]: user.vim_run_normal_np('za')
toggle (recursive | recur) fold [that]: user.vim_run_normal_np('zA')
fold [that]: user.vim_run_normal_np('zc')
(recursive | recur) fold [that]: user.vim_run_normal_np('zC')
unfold [that]: user.vim_run_normal_np('zo')
(recursive | recur) unfold [that]: user.vim_run_normal_np('zO')
