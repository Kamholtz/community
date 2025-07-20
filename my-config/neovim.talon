tag: user.vim_mode_insert
tag: user.vim_mode_normal
-

tag(): user.cursorless

(dup | duplicate) line:
    user.vim_run_normal_np("yy")
    user.vim_run_normal_np("p")

change word:
    user.vim_run_normal_np("ciw")

change (nibble|inner word):
    user.vim_run_normal_np("civ")

change para:
    user.vim_run_normal_np("cip")

toggle comment:
    user.vim_run_normal_np("gcc")

G status:
    user.vim_normal_mode(" gg")

G status:
    user.vim_run_normal_np(" gg")

G push:
    user.vim_run_normal_np(" gkk")

G pull:
    user.vim_run_normal_np(" gjj")

G stage:
    user.vim_run_normal_np(" hs")

G stage file:
    user.vim_run_normal_np(" hS")
#
# G commit feature:
    user.vim_run_normal_np(":GitCommitFeat\n")

G commit wip:
    user.vim_run_normal_np(":GitCommitWip\n")

G commit fix:
    user.vim_run_normal_np(":GitCommitFix\n")

G commit refactor:
    user.vim_run_normal_np(":GitCommitRefactor\n")

G commit format:
    user.vim_run_normal_np(":GitCommitFormat\n")

G verbose commit (feature|feat):
    user.vim_run_normal_np(":GitVerboseCommit feat\n")

G verbose commit fix:
    user.vim_run_normal_np(":GitVerboseCommit fix\n")

G verbose commit refactor:
    user.vim_run_normal_np(":GitVerboseCommit refactor\n")

G verbose commit wip:
    user.vim_run_normal_np(":GitVerboseCommit wip\n")

G verbose commit format:
    user.vim_run_normal_np(":GitVerboseCommit format\n")

fugitive (close|hide|kill):
    user.vim_run_normal_np(":CloseFugitive\n")

tab close:
    user.vim_run_normal_np(":tabclose\n")

tab new:
    user.vim_run_normal_np(":tabnew\n")

tab only:
    user.vim_run_normal_np(":tabonly\n")

(win|window) only:
    user.vim_run_normal_np(":only\n")

WriteReportTemp:
    user.vim_run_normal_np(":WriteReportTemp\n")

copy git branch:
    user.vim_run_normal_np(" cgb")

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
    key("enter")

hunt this [<user.text>]:
    user.vim_run_normal_np("/{user.text or ''}")
    key("enter")

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
check box tick: user.check_box_tick
check box untick: user.check_box_untick


# =====================================
# Mini files
# =====================================
mini files:
    user.vim_run_normal_np(':MyMiniFilesOpen\n')

mini files current:
    user.vim_run_normal_np(':lua MiniFiles.open()\n')
