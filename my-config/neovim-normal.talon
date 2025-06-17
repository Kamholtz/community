tag: user.vim_mode_normal
-

(dup | duplicate) line:
    insert("yy")
    insert("p")

change word:
    insert("ciw")

G status:
    user.vim_normal_mode(" gg")

G status:
    insert(" gg")

G push:
    insert(" gkk")

G pull:
    insert(" gjj")

go to def:
    insert("gd")

find refs:
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