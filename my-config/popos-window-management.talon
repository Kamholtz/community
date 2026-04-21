os: linux
hostname: pop-os
-

# Application switcher (fixes 'focus' command that doesn't work on Linux)
focus$: key(super-a)

# Cycle windows of the same application while keeping Alt held down.
window same next:
    key(alt:down)
    key(`)

window same stop: key(alt:up)

# Window state management
# Note: window minimize is not currently enabled in Pop!OS configuration
window minimize: key(super-h)
window maximize: key(super-up)
window (unmaximize | restore): key(super-down)

# Desktop/workspace switching (supplementary to existing desktops.talon)
# These use Pop!OS native shortcuts as alternatives to the generic commands
(desk | desktop | workspace) left: key(super-ctrl-alt-left)
(desk | desktop | workspace) right: key(super-ctrl-alt-right)

# Move window between desktops (supplementary to existing desktops.talon)
# These use Pop!OS native shortcuts as alternatives to the generic commands
window (desk | desktop | workspace) left: key(super-shift-ctrl-alt-left)
window (desk | desktop | workspace) right: key(super-shift-ctrl-alt-right)
