cd C:\Users\carlk\AppData\Roaming\talon\user

git clone https://github.com/chaosparrot/talon_hud.git

git clone https://github.com/Kamholtz/community.git

winget install --id BlastApps.FluentSearche

git clone https://github.com/cursorless-dev/cursorless-talon.git cursorless-talon

git clone https://github.com/wolfmanstout/talon-gaze-ocr.git

git clone https://github.com/C-Loftus/talon-ai-tools.git

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

prevent Microsoft store opening when running python
https://stackoverflow.com/questions/58754860/cmd-opens-windows-store-when-i-type-python


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression


# Add bucket
scoop bucket add nerd-fonts
# Maple Mono (ttf format)
scoop install Maple-Mono
# Maple Mono NF
scoop install Maple-Mono-NF
