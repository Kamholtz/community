tag: user.vim_mode_normal
-

(dup | duplicate) line:
    insert("yy")
    insert("p")

change word:
    insert("ciw")

change para:
    insert("cip")

toggle comment:
    insert("gcc")

G status:
    user.vim_normal_mode(" gg")

G status:
    insert(" gg")

G push:
    insert(" gkk")

G pull:
    insert(" gjj")

G stage:
    insert(" hs")

G stage file:
    insert(" hS")

G commit feature:
    insert(":GitCommitFeat\n")

G commit wip:
    insert(":GitCommitWip\n")

G commit fix:
    insert(":GitCommitFix\n")

G commit refactor:
    insert(":GitCommitRefactor\n")

G commit format:
    insert(":GitCommitFormat\n")

fugitive (close|hide|kill):
    insert(":CloseFugitive\n")

tab close:
    insert(":tabclose\n")

tab new:
    insert(":tabnew\n")

copy git branch:
    insert(" cgb")

# TODO: Figure out how to show the command picker synchronously
please:
    insert(" fc")

go to def:
    insert("gd")

find (refs|references):
    insert(" lr")

find file:
    insert(" ff")
    
niff:
    insert("]c")

next change:
    insert("]c")

piff:
    insert("[c")

prev change:
    insert("[c")

show sig:
    insert(" lh")

# G status:
#     insert(":G\n")

# "drink <TARGET>": Inserts a new line above the target line, and moves the cursor to the newly created line
drink line:
    insert("O")
    key("escape")
# "pour <TARGET>": Inserts a new line below the target line, and moves the cursor to the newly created line
pour line:
    insert("s")
    key("escape")
# "drop <TARGET>": Inserts an empty line above the target line (without moving the cursor)
drop line:
    insert("[ ")
# "float <TARGET>": Inserts an empty line below the target line (without moving the cursor)
float line:
    insert("] ")
# "puff <TARGET>": Inserts empty lines/spaces around the target (without moving the cursor)
puff line:
    insert("[ ] ")