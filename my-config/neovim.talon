tag: user.vim_mode_insert
tag: user.vim_mode_normal
-


(dup | duplicate) line:
    user.vim_run_normal_np("yy")
    user.vim_run_normal_np("p")

change word:
    user.vim_run_normal_np("ciw")

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

G commit feature:
    user.vim_run_normal_np(":GitCommitFeat\n")

G commit wip:
    user.vim_run_normal_np(":GitCommitWip\n")

G commit fix:
    user.vim_run_normal_np(":GitCommitFix\n")

G commit refactor:
    user.vim_run_normal_np(":GitCommitRefactor\n")

G commit format:
    user.vim_run_normal_np(":GitCommitFormat\n")

fugitive (close|hide|kill):
    user.vim_run_normal_np(":CloseFugitive\n")

tab close:
    user.vim_run_normal_np(":tabclose\n")

tab new:
    user.vim_run_normal_np(":tabnew\n")

copy git branch:
    user.vim_run_normal_np(" cgb")

# TODO: Figure out how to show the command picker synchronously
# ^please [<user.text>]$: user.command_search(user.text or "")
    # user.vim_run_normal_np(":lua Snacks.picker.commands({pattern='hi'})\n")

go to def:
    user.vim_run_normal_np("gd")

find (refs|references):
    user.vim_run_normal_np(" lr")

find file:
    user.vim_run_normal_np(" ff")

niff:
    user.vim_run_normal_np("]c")

next change:
    user.vim_run_normal_np("]c")

piff:
    user.vim_run_normal_np("[c")

prev change:
    user.vim_run_normal_np("[c")

show sig:
    user.vim_run_normal_np(" lh")

# G status:
#     user.vim_run_normal_np(":G\n")

# "drink <TARGET>": Inserts a new line above the target line, and moves the cursor to the newly created line
drink line:
    user.vim_run_normal_np("O")
    key("escape")
# "pour <TARGET>": Inserts a new line below the target line, and moves the cursor to the newly created line
pour line:
    user.vim_run_normal_np("s")
    key("escape")
# "drop <TARGET>": Inserts an empty line above the target line (without moving the cursor)
drop line:
    user.vim_run_normal_np("[ ")
# "float <TARGET>": Inserts an empty line below the target line (without moving the cursor)
float line:
    user.vim_run_normal_np("] ")
# "puff <TARGET>": Inserts empty lines/spaces around the target (without moving the cursor)
puff line:
    user.vim_run_normal_np("[ ] ")

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
