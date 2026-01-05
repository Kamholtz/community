mode: user.whisper
-

key(alt-m:down):
    user.whisper_done()
    speech.enable()
    mode.disable("user.whisper")
