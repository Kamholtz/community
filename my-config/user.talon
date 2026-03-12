tag(): user.git
tag(): user.zoxide
tag(): user.docker
# tag(): user.gamepad_tester

tag(): user.gamepad
tag(): user.glazewm

# Example Talon file
settings():
    imgui.scale = 3
    speech.timeout = 0.6
    # subtitles_show = true
    user.subtitles_color = "ffffaa"
    user.model_endpoint = "acp"
    # user.model_default = "gpt-4o-mini"
    user.model_shell_default = "zsh"
    user.cursorless_settings_directory = "community/my-config/cursorless-settings"
    user.model_acp_agent_command = "/home/carl/repos/acp-wrapper/run-acp-agent"
    # Enable evil-mode support in Emacs (uses C-r " for paste in insert mode)
    user.emacs_evil_mode = true

# Custom voice commands for undo and redo
nope: edit.undo()
yep: edit.redo()

# clap: key(enter)

# list phrase: on_phrase.analyze_phrase
# (phrase view): user.analyze_phrase()

scrape: key(escape)

# quick pick: user.quick_pick_show()

# Command to open Talon user directory in VSCode
open talon config:
    user.open_talon_config_vscode()

# F13 — L
key(f13:up):
    user.mouse_scroll_down(2)

# F14 — L2
key(f14:up):
    key(home)

# F15 — R2
key(f15:up):
    user.mouse_scroll_up(2)

# F16 — R
key(f16:up):
    key(end)

# F17 — - (minus)
key(f17:up):
    key(ctrl-backspace)

# F18 — + (plus)
key(f18:up):
    key(space)

# F19 — * (star)
key(f19:up):
    key(tab)

# F20 — M-shaped symbol (go flag)
key(f20:up):
    key(super-~)
    # user.quick_pick_show()

# F21 —
key(f21:up):
    print("repeat start")
    core.repeat_phrase()
    print("end")

# F22 — X
key(f22:down):
    user.mouse_drag(0)
key(f22:up):
    user.mouse_drag_end()

# F23 — A
key(f23:down):
    user.mouse_drag(2)
key(f23:up):
    user.mouse_drag_end()

# F24 — B
key(f24:down):
    user.mouse_drag(1)
key(f24:up):
    user.mouse_drag_end()

toggle hiss scroll:
    user.toggle_hiss_scroll()
