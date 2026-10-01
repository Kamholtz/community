mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
-

# Handy toggles transcription with Ctrl+Space. Saying "wombat" sends that
# shortcut without changing Talon's speech state.
^wombat$:
    user.toggle_handy_transcription()

^wombat toggle$:
    user.toggle_f1_handy_mode()
