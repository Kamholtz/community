# My Changes

## Whisper D-pad overlay

F1 now opens a four-direction Whisper control overlay. Up toggles Whisper and
keeps the overlay open; Left copies the last polished session; Right inserts
it; Down copies the current session transcript accumulated to that point.
The mapping is defined as data in `my-config/whisper/whisper_dpad.py`, including
each command and its post-command dismissal function. The overlay is green while
Whisper is active. Keyboard arrows and a gamepad D-pad dispatch through the
same mapping; the other mapped gamepad controls plus Escape, Enter, Space, Tab,
and F1 dismiss it. The Whisper integration now retains all finalised segments
and includes current realtime text when copying the active-session snapshot.

## (1) Edit

### (1.1) Replace Edit Action Cut With Carve

See header

## (2) Emacs in WSL (RAIL window)

### (2.1) Context match for WSL RemoteApp windows

`my-config/apps/emacs/emacs_wsl.py` extends `mod.apps.emacs` with a rule that
matches `win.class: RAIL_WINDOW` + `win.title: /Emacs/`. This fires when Emacs
runs inside WSL but is displayed as a Windows RemoteApp (RAIL) window via
`msrdc.exe`; the standard `app.exe: /^emacs\.exe$/` rule never matches in that
configuration.

**Caveat:** `actions.key()` keystrokes land in the RAIL window and are
forwarded by the RAIL protocol into the WSL session, so most Emacs keybindings
work as normal. Two exceptions:

- Keys Windows intercepts before RAIL (e.g. `Win+key`, `Alt+F4`) never reach
  Emacs.
- `actions.clip` uses the Windows clipboard; sharing with the WSL session
  depends on the WSL/RDP clipboard-integration setting.

## (3) Agent Skills

### (2.1) Flatten Community Skill Layout

Moved active Talon agent skills from `.agents/skills/skills/` to `.agents/skills/` and removed redundant or empty skill directories. General Talon syntax/customization guidance is now expected to come from the canonical `~/.agents/skills/talon-skill` skill, while this repository keeps local Talon workflow/debugging skills.

### (2.2) Add Agent Skill Gates

Added `.agents/scripts/check_talon_config.py` and `.githooks/pre-commit` to enforce skill metadata, changed/staged text linting, Python compilation, and pytest when available. Updated agent docs to explain when to use each Talon skill and how to run the validation workflow.

## (4) Fluent Search

### (4.1) Add Windows Fluent Search Commands

Imported `apps/fluent_search/` from `nriley/talon_community` commit `51bc9087a723af0c6b8587cccea14068280fafee`. Adds Windows commands for launching app/process searches, Fluent Search screen labels, and in-app/menu search hotkeys.

### (4.2) Fix Fluent Search Wait Detection

Updated `apps/fluent_search/fluent_search.py` to recognize Fluent Search when Talon reports the active app as `Fluent Search` on Windows, avoiding the timeout notification before query text is pasted.

## (5) Vocabulary

### (5.1) Move Misrecognitions to Words To Replace

Moved correction-style vocabulary mappings from `core/vocabulary/vocabulary.talon-list` into `settings/words_to_replace.csv`, leaving the vocabulary list focused on ordinary terms, proper nouns, and acronym pronunciations.
