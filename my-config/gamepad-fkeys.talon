tag(): user.git
tag(): user.zoxide
tag(): user.docker
# tag(): user.gamepad_tester

tag(): user.gamepad
tag(): user.glazewm





# F1
# key(f1:up): user.toggle_command_dictation_mode()

# F13 — L
key(f13:up): user.mouse_scroll_down(2)

# F14 — L2
key(f14:up): key(home)

# F15 — R2
key(f15:up): user.mouse_scroll_up(2)

# F16 — R
key(f16:up): key(end)

# F17 — - (minus)
key(f17:up): key(ctrl-backspace)

# F18 — + (plus)
key(f18:up): key(space)

# F19 — * (star)
# key(f19:up): key(tab)

# F20 — M-shaped symbol (go flag)
key(f20:up):
    tracking.control_toggle()
    # key(super-~)
    # user.quick_pick_show()

# F21 —
key(f21:up):
    print("repeat start")
    core.repeat_phrase()
    print("end")

# F22 — X
key(f22:down): user.mouse_drag(0)
key(f22:up): user.mouse_drag_end()

# F23 — A
key(f23:down): user.mouse_drag(2)
key(f23:up): user.mouse_drag_end()

# F24 — B
key(f24:down): user.mouse_drag(1)
key(f24:up): user.mouse_drag_end()
