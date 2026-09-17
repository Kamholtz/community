mode: command
mode: dictation
mode: sleep
not speech.engine: dragon
-

# Handy transcribes while ctrl-space is held down. Saying "wombat" starts the
# hold and puts speech to sleep (like `porcupine`) so nothing else can fire;
# saying it again releases the keys and wakes speech back up.
^wombat$:
    user.handy_toggle()
