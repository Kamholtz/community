app: vscode
# Looks for special string in window title.
# NOTE: This requires you to add a special setting to your VSCode settings.json
# See [our vscode docs](./README.md#terminal)
win.title: /focus:\[Terminal\]/
-
tag(): terminal

# Use VS Code terminal paste binding.
(pace | paste) (that | it): key(ctrl-shift-v)
key(control v): key(ctrl-shift-v)
