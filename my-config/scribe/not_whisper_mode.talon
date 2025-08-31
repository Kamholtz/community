# Whisper transcription daemon control commands

# Commands to START whisper mode (available when NOT in whisper mode)
mode: command
mode: dictation
mode: sleep
not mode: user.whisper
not speech.engine: dragon
-

# Start whisper mode commands
# ^talon whisper start$: user.whisper_start()
# ^whisper start$: user.whisper_start()
