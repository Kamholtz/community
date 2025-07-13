app: obsidian
-
tag(): user.tabs


please [<user.text>]:
    key('ctrl-P')
    insert(user.text or "")

tag(): user.markdown

file save: key(ctrl-s)
left side: key(ctrl-left)
new note: key(ctrl-n)
open quick: key(ctrl-o)
right side: key(ctrl-right)
search file: key(ctrl-f)
start editing: key(ctrl-e)
start reading: key(ctrl-e)
stop editing: key(ctrl-e)
stop reading: key(ctrl-e)
toggle: key(ctrl-enter)

open today: key(ctrl-shift-t)
search vault: key(ctrl-shift-f)
open daily: user.open_daily_note()