# My Changes

## Disable Whisper Windows notifications

Whisper messages, including "failed to handle event", now go to Talon's log
on Windows instead of desktop notifications. Existing HUD status and event-log
updates remain available.

## Whisper HUD panel, choice-panel history picker, and event-log routing

Whisper mode now drives a persistent Talon HUD panel (topic `whisper_panel`,
rendered on the HUD's wildcard Text panel — no talon_hud edits). The panel
shows the live state, polisher/context-extractor health, and a rolling session
transcript with the in-progress utterance colour-coded (blue realtime, orange
awaiting polish); during graceful shutdown it republishes a once-per-second
countdown instead of 120 s of dead air. `whisper history` now opens the HUD
Choice panel ("option N" by voice or click) with the old imgui picker as the
no-HUD fallback; `whisper pick <n>` is unchanged. Service degradation, probe
summaries, connection, context, and session events route to the HUD event log
(warning on degradation), and the modal force-open of the imgui status/context
windows after probes is gone — `whisper status` renders on the HUD panel when
available. Formatting lives in pure-Python
`my-config/whisper/whisper_hud_content.py` (tested by
`test/test_whisper_hud_content.py`); all HUD calls go through the guarded seam
`my-config/whisper/whisper_hud.py`, which checks `user.talon_hud_available`
(version >= 6) and warns once instead of failing silently. Panel text size is a
HUD per-widget preference (`Text panel_font_size` in
`talon_hud/preferences/monitor(...).csv`, set via
`hud_set_widget_preference`; context menu, Choices, and event log were
raised the same way), not `imgui.scale`.

The panel also carries a "Copy session" button (right-click menu, or say
"whisper copy session") wired to `whisper_session_copy_current`, and a
"Mic → WSL" line naming the Windows default capture device — the one WSLg
mirrors into WSL2 as RDPSource — resolved in the background at mode entry by
`my-config/whisper/get_default_mic.ps1`. Services are now also verified by
live use: a real `polished`/`session_polished` event marks the polisher
passed and `context_updated` marks the context extractor passed
(`ServiceState.verify_live()`), so labels no longer sit on "available, not
tested" while the service is demonstrably working.

## Whisper service diagnostics

Whisper now consumes the server's `service_status` events and exposes
`whisper status`, `whisper test polish`, `whisper test context`, and
`whisper test all`. Tests run in isolated one-shot clients so they cannot stop
the persistent dictation client. The polisher test retries once to accommodate
cold model startup, and a status window distinguishes availability from a
successful end-to-end test while preserving plain transcription as a fallback.

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

## (0) Hot Corners

Moving the pointer into either top corner now opens the desktop switcher. The
feature is enabled independently for Windows and Linux by
`my-config/hot_corners_windows.talon` and
`my-config/hot_corners_linux.talon`; set `user.hot_corners_enabled` to `false`
in either file to disable it on that operating system. Each screen has its own
8-by-8-pixel corner targets, and a corner triggers only once until the pointer
leaves it.

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
