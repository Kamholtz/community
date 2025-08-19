tag(): user.git
tag(): user.zoxide
# tag(): user.gamepad_tester

tag(): user.gamepad

# Example Talon file
settings():
    imgui.scale = 3
    speech.timeout = 0.6
    # subtitles_show = true
    user.subtitles_color = "ffffaa"


# Custom voice commands for undo and redo
nope:
    edit.undo()
yep:
    edit.redo()

# list phrase: on_phrase.analyze_phrase
# (phrase view): user.analyze_phrase()

(right|R) desk: key(ctrl-super-right)
desk (right|R): key(ctrl-super-right)
resk: key(ctrl-super-right)

(left|L) desk: key(ctrl-super-left)
desk (left|L): key(ctrl-super-left)
lesk: key(ctrl-super-left)

scrape: key(escape)

# Command to open Talon user directory in VSCode
open talon config:
    user.open_talon_config_vscode()

# (vest one|word term|weston|western): "wezterm"
