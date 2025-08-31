# Whisper mode - minimal commands like dictation mode
mode: user.whisper
not speech.engine: dragon
-

# VERY specific exit commands - must match exactly like dictation mode
# ^talon whisper done$: user.whisper_done()
# ^whisper done$: user.whisper_done()

# Alternative exact-match exit commands
# ^command mode$: user.whisper_done()
# ^command marred$: user.whisper_done()

# Everything else should be handled by the transcription daemon
# No raw prose capture - let whisper daemon handle all speech