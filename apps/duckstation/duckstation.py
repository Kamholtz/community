from talon import Module

mod = Module()

mod.apps.duckstation_ps1_emulator = r"""
os: windows
and app.name: DuckStation PS1 Emulator
os: windows
and app.exe: /^duckstation-qt-x64-ReleaseLTCG\.exe$/i
"""
