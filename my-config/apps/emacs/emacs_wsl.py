from talon import Module

mod = Module()

# Match Emacs running in WSL displayed as a Windows RAIL (RemoteApp) window.
# win.class is RAIL_WINDOW and app.exe is msrdc.exe in this case, so the
# standard app.exe: /^emacs\.exe$/ rule never fires.
#
# Keystroke caveat: actions.key() sends keystrokes to the OS-focused RAIL
# window; the RAIL protocol forwards them into the WSL session, so Emacs
# receives them normally. The exception is keys Windows intercepts before RAIL
# (e.g. Win+key, Alt+F4) — those will never reach Emacs. Clipboard actions
# (actions.clip) use the Windows clipboard; whether it is shared with the WSL
# session depends on the WSL/RDP clipboard-integration setting.
mod.apps.emacs = """
os: windows
win.class: RAIL_WINDOW
win.title: /Emacs/
"""
