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
    user.model_endpoint = "llm"
    user.model_default = "gpt-4o-mini"
    user.model_shell_default = "zsh"
    user.cursorless_settings_directory = "community/my-config/cursorless-settings"
    # Enable evil-mode support in Emacs (uses C-r " for paste in insert mode)
    user.emacs_evil_mode = true

# Custom voice commands for undo and redo
nope: edit.undo()
yep: edit.redo()

# clap: key(enter)

# list phrase: on_phrase.analyze_phrase
# (phrase view): user.analyze_phrase()

scrape: key(escape)

# Command to open Talon user directory in VSCode
open talon config:
    user.open_talon_config_vscode()

# key(ctrl-f12):
#     core.repeat_command(1)

# key(f12): "hello"
# key(F20): "hello"
# key(ctrl-F3): "hello"
# key(f3): "hello"

# key(ctrl-1): "hello"
# key(ctrl-shift-1): "hello"
# key(ctrl-shift-alt-1): "hello"
# key(ctrl-alt-w): "hello"
# key(alt-1): "hello"
# key(ctrl-1): "hello"
# key(ctrl-w): insert("hello")

# key(f20):
#     # close zoom if open
#     tracking.zoom_cancel()
#     mouse_click(1)
#     # close the mouse grid if open
#     user.grid_close()

key(f13):
    mouse_click(1)

# key(f14):
#     core.repeat_command(1)

# key(f14):
#     core.repeat_partial_phrase()

# key(f14):
#     core.repeat_partial_phrase(1)

# key(f14):
#     print("pressed F14")

# key(f14):
#     mimic("again")

key(f14:up):
    print("start")
    core.repeat_phrase()
    print("end")

key(f15:up):
    mouse_click(0)

key(f20:up):
    mouse_click(1)

# (repeat phrase | again) [<number_small> times]:
#     core.repeat_partial_phrase(number_small or 1)

toggle hiss scroll:
    user.toggle_hiss_scroll()

# (vest one|word term|weston|western): "wezterm"
