os: windows
-

# WORK AROUND: For some reason on windows it is necessary to have a key binding to the key without the up event in order to trigger the up event keybinding, except for the mouse keys

# F13 — L
key(f13):
    user.gamepad_debug("key(f13):")

# F14 — L2
key(f14):
    user.gamepad_debug("key(f14):")

# F15 — R2
key(f15):
    user.gamepad_debug("key(f15):")

# F16 — R
key(f16):
    user.gamepad_debug("key(f16):")

# F17 — - (minus)
key(f17):
    user.gamepad_debug("key(f17):")

# F18 — + (plus)
key(f18):
    user.gamepad_debug("key(f18):")

# F19 — * (star)
key(f19):
    user.gamepad_debug("key(f19):")

# F20 — M-shaped symbol (go flag)
key(f20):
    user.gamepad_debug("key(f20):")
# Relacon mouse
key(shift-f2):
    user.gamepad_debug("key(f2):")

# F21 —
key(f21):
    user.gamepad_debug("key(f21):")

# the mouse key bindings do not require the work around

# # F22 — X
# key(f22):
#     print("key(f22):")

# # F23 — A
# key(f23):
#     print("key(f23):")

# # F24 — B
# key(f24):
#     print("key(f24):")
