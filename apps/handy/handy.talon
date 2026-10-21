mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
-

# Handy toggles transcription with Ctrl+Space. Saying "handy" sends that
# shortcut without changing Talon's speech state.
^handy$:
    user.toggle_handy_transcription()

^handy toggle$:
    user.toggle_f1_handy_mode()
