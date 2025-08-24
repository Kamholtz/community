app: /WezTerm/i
os: windows

---

# Need to enable the terminal and git tags to make use of the talent community git application config
tag(): terminal

# Tabs
tab next:                 key(ctrl-tab)
tab last:                 key(ctrl-shift-tab)
tab new:                  key(ctrl-shift-t)
tab close:                key(ctrl-shift-w)
tab one:                  key(ctrl-1)
tab two:                  key(ctrl-2)
tab three:                key(ctrl-3)
tab four:                 key(ctrl-4)
tab five:                 key(ctrl-5)

# Panes (adjust these if you have custom bindings in wezterm.lua)
split right:              key(ctrl-shift-%)          # Often ctrl-shift-% is vertical split
split down:               key(ctrl-shift-quote)      # Horizontal split

pane left:                key(ctrl-shift-left)
pane right:               key(ctrl-shift-right)
pane up:                  key(ctrl-shift-up)
pane down:                key(ctrl-shift-down)
pane close:               key(ctrl-shift-w)

# Command palette or launcher (customize if needed)
command palette:          key(ctrl-shift-p)

# Clipboard operations
paste:                    key(ctrl-shift-v)
paste to all:             key(ctrl-u ctrl-shift-v)

# Reverse history search (FZF-style)
reverse search <user.text>:
    key(ctrl-r)
    insert(user.text or "")

# Git quick commands
git status:               insert("git status\n")
git commit:
    insert("git commit -m ''")
    key(left)
git pull:                 insert("git pull\n")
git push:                 insert("git push\n")
git clone:                insert("git clone ")

# Run command via dictation (requires user.text command below)
say command <user.text>:
    insert("{text}") key(enter)
