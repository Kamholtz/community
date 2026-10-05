os: windows
-

# Fluent Search provides equivalents to my common uses of
# LaunchBar, Contexts, Homerow and menu search on Mac.

# If you have different keyboard shortcuts configured, you will need
# to replace them here.

# -- Homerow
# Search in-app using Screen hotkey (displays labels; frontmost app)
# ^ax$: key(alt-;)

# Search using Screen hotkey (displays labels; screen 1 only)
^fluent screen$: key(shift-alt)
# Search using Screen hotkey (displays labels; screen 1 only), then activate a gesture.
^fluent screen (click | left click)$:
    key(shift-alt)
    sleep(500ms)
    key(1)
^fluent screen double click$:
    key(shift-alt)
    sleep(500ms)
    key(2)
^fluent screen select click$:
    key(shift-alt)
    sleep(500ms)
    key(3)
^fluent screen right click$:
    key(shift-alt)
    sleep(500ms)
    key(4)
^fluent screen move mouse$:
    key(shift-alt)
    sleep(500ms)
    key(5)
# Search using Screen hotkey scoped to the focused app/window.
^fluent (click | left click)$:
    key(shift-super)
    sleep(500ms)
    key(1)
^fluent double click$:
    key(shift-super)
    sleep(500ms)
    key(2)
^fluent select click$:
    key(shift-super)
    sleep(500ms)
    key(3)
^fluent right click$:
    key(shift-super)
    sleep(500ms)
    key(4)
^fluent move mouse$:
    key(shift-super)
    sleep(500ms)
    key(5)

# -- LaunchBar
# Search hotkey (in fluent_search.py)
^fluent launch <user.text>$: user.fluent_search("apps\t{text}")
^fluent launch brief {user.abbreviation}$: user.fluent_search("apps\t{abbreviation}")
^fluent launch bar$: user.fluent_search("")
# Search using Processes hotkey
# No hotkey is configured for this source in hotkeys.md (Kill process /
# Windows are both "None"); disabled until one is assigned.
# ^launch running$: key(ctrl-alt-shift-space)

# -- Contexts
^fluent kill [<user.text>]: user.fluent_search("kill\t{text or ''}")
# TODO: confirm the gesture/hotkey Fluent Search uses for "kill all"
# matching results before enabling.
# ^fluent kill all$: user.fluent_search("kill\t")

# -- Contexts
^fluent walk [<user.text>]: user.fluent_search("windows\t{text or ''}")

# -- Clipboard
^fluent clip [<user.text>]: user.fluent_search("clipboard\t{text or ''}")

# -- Files
^fluent files [<user.text>]: user.fluent_search("files\t{text or ''}")

# -- Menu search / Homerow
# In-app search hotkey
^fluent (ax | menu | app): user.fluent_search_in_app(text or "", false)

# -- Result gestures (Ctrl+/Ctrl+C/etc. shared across most sources; see
# apps/fluent_search/hotkeys.md)
^fluent preview$: key(alt-p)
^fluent preview window$: key(shift-enter)
^fluent pin$: key(alt-ctrl-p)
^fluent open$: key(ctrl-1)
^fluent copy$: key(ctrl-c)
^fluent delete$: key(delete)
^fluent clear$: key(shift-delete)
^fluent rename$: key(f2)
^fluent admin$: key(ctrl-shift-enter)

# -- Clipboard result gestures
^fluent paste$: key(ctrl-v)
^fluent keep$: key(ctrl-s)

# -- Files result gestures
^fluent open folder$: key(ctrl-2)
^fluent search folder$: key(ctrl-r)
^fluent open terminal$: key(ctrl-3)
^fluent open with$: key(ctrl-4)
^fluent copy file$: key(ctrl-5)
