# NOTE: To use GlazeWM commands, enable the tag in your settings:
#   tag(): user.glazewm
os: windows
tag: user.glazewm
-

# Focus movement
(win | window) left: user.glazewm_focus("left")
(win | window) right: user.glazewm_focus("right")
(win | window) up: user.glazewm_focus("up")
(win | window) down: user.glazewm_focus("down")

# Move window
(shuffle | move (win | window) left): user.glazewm_move("left")
(shuffle | move (win | window) right): user.glazewm_move("right")
(shuffle | move (win | window) up): user.glazewm_move("up")
(shuffle | move (win | window) down): user.glazewm_move("down")

# Resize
resize narrower: user.glazewm_resize("narrower")
resize wider: user.glazewm_resize("wider")
resize taller: user.glazewm_resize("taller")
resize shorter: user.glazewm_resize("shorter")

resize mode: user.glazewm_resize_mode()
resize done: user.glazewm_resize_mode_exit()

# WM toggles and actions
tiling pause: user.glazewm_toggle_pause()
tiling direction: user.glazewm_toggle_tiling_direction()
focus cycle: user.glazewm_cycle_focus()
toggle floating: user.glazewm_toggle_floating()
toggle tiling: user.glazewm_toggle_tiling()
(full screen | (win | window) scuba): user.glazewm_toggle_fullscreen()
minimize (win | window): user.glazewm_toggle_minimized()
(win | window) kill: user.glazewm_close()
glaze exit: user.glazewm_exit()
glaze reload: user.glazewm_reload_config()
glaze redraw: user.glazewm_redraw()

# Launch shell/terminal
(launch shell | koopa): user.glazewm_launch_shell()

# Workspaces
port <number_small>: user.glazewm_workspace_focus(number_small)
workspace <number_small>: user.glazewm_workspace_focus(number_small)
port right: user.glazewm_workspace_next()
port left: user.glazewm_workspace_prev()
port recent: user.glazewm_workspace_recent()
workspace next: user.glazewm_workspace_next()
workspace previous: user.glazewm_workspace_prev()
workspace recent: user.glazewm_workspace_recent()

(shuffle | move (win | window) [to] port) <number_small>: user.glazewm_move_to_workspace(number_small)
(shuffle | move (win | window) [to] workspace) <number_small>: user.glazewm_move_to_workspace(number_small)

# Move parent workspace between monitors
move workspace left: user.glazewm_move_workspace("left")
move workspace right: user.glazewm_move_workspace("right")
move workspace up: user.glazewm_move_workspace("up")
move workspace down: user.glazewm_move_workspace("down")
