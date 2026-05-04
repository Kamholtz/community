tag(): user.git
tag(): user.zoxide
tag(): user.docker
# tag(): user.gamepad_tester

tag(): user.gamepad
tag(): user.glazewm

# Example Talon file
settings():
    imgui.scale = 4
    speech.timeout = 0.6
    # subtitles_show = true
    user.subtitles_color = "ffffaa"
    user.model_endpoint = "llm"
    # user.model_default = "gpt-4o-mini"
    user.model_shell_default = "zsh"
    user.cursorless_settings_directory = "community/my-config/cursorless-settings"
    # user.model_acp_agent_command = "/home/carl/repos/acp-wrapper/run-acp-agent"
    # Enable evil-mode support in Emacs (uses C-r " for paste in insert mode)
    user.emacs_evil_mode = true
    # user.subtitles_size = 500

# Custom voice commands for undo and redo
nope: edit.undo()
yep: edit.redo()

# clap: key(enter)

# list phrase: on_phrase.analyze_phrase
# (phrase view): user.analyze_phrase()

scrape: key(escape)

quick pick$: user.quick_pick_show()

# Command to open Talon user directory in VSCode
open talon config: user.open_talon_config_vscode()

toggle hiss scroll: user.toggle_hiss_scroll()
