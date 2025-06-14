# Example Talon file
settings():
    imgui.scale = 3
    speech.timeout = 0.5
    subtitles_show = true
    user.subtitles_color = "ffffaa"

tag(): user.cursorless_use_community_snippets

# Custom voice commands for undo and redo
nope:
    edit.undo()
yep:
    edit.redo()

(fine|end|one|a  ad) list phrase: on_phrase.analyze_phrase
(phrase view): user.analyze_phrase()

right desk: key(ctrl-super-right)
left desk: key(ctrl-super-left)

# Command to open Talon user directory in VSCode
open talon config:
    user.open_talon_config_vscode()

# (vest one|word term|weston|western): "wezterm"