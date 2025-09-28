app: obsidian
-
tag(): user.tabs


please [<user.text>]:
    key('ctrl-P')
    insert(user.text or "")

settings():
    user.snippet_raw_text_paste = true

tag(): user.markdown

file save: key(ctrl-s)
disk: key(ctrl-s)
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
open daily: user.obsidian("Open today's daily note")
open next daily: user.obsidian("Open next daily note")
open previous daily: user.obsidian("Open previous daily note")

# Override markdown code block for Obsidian to work with auto-completion
# {user.markdown_code_block_language} block (paste | pace):
#     user.insert_snippet("```{markdown_code_block_language}\n$0\n```")
#     key(ctrl-v)
