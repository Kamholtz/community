# Only active while the dedicated whisper mode is enabled.
mode: user.whisper
-


^talon whisper$: user.whisper_start()

^talon whisper done$: user.whisper_done()