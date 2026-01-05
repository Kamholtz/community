# Commands to START whisper mode (available globally)
# mode: command
# mode: dictation
not mode: whisper
-

# # Start whisper mode commands
# ^talon whisper start$: user.whisper_start()
# ^talon whisper$: user.whisper_start()
# ^whisper start$: user.whisper_start()

key(alt-m:down):
    mode.enable("user.whisper")
    speech.disable()
    user.whisper_start()
