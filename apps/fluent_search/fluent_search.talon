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

# -- LaunchBar
# Search hotkey (in fluent_search.py)
^launch <user.text>$: user.fluent_search("apps\t{text}")
^launch brief {user.abbreviation}$: user.fluent_search("apps\t{abbreviation}")
^launch bar$: user.fluent_search("")
# Search using Processes hotkey
# No hotkey is configured for this source in hotkeys.md (Kill process /
# Windows are both "None"); disabled until one is assigned.
# ^launch running$: key(ctrl-alt-shift-space)

# -- Contexts
^fluent con [<user.text>]: user.fluent_search("processes\t{text or ''}")

# -- Contexts
^fluent walk [<user.text>]: user.fluent_search("windows\t{text or ''}")

# -- Menu search / Homerow
# In-app search hotkey
^fluent (ax | menu | app): user.fluent_search_in_app(text or "", false)
