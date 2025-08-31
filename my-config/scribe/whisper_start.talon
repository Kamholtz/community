# Commands to START whisper mode (available globally)
mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
-

# Start whisper mode commands
^talon whisper start$: user.whisper_start()
^talon whisper$: user.whisper_start()
^whisper start$: user.whisper_start()