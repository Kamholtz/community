# Talon Whisper Mode

A focused Talon mode that integrates with the Scribe transcription daemon for hands-free dictation. When enabled, it minimizes normal command recognition and only listens for the single exit phrase.

- Mode name: `user.whisper`
- Start action: `user.whisper_start()`
- Exit phrase (only command while active): `talon whisper done`
- Exit action (called by the phrase): `user.whisper_done()`

## What It Does

- On start: calls the daemon `POST /unmute` to begin live transcription, disables Talon `command` mode, and enables `user.whisper` mode.
- While active: other commands are minimized; only the phrase `talon whisper done` is recognized (see `whisper_mode.talon`).
- On exit: calls the daemon `POST /mute`, disables `user.whisper` mode, and re-enables `command` mode.

## Files

- `whisper_mode.py` — Implements Talon actions and mode switching, talks to the daemon at `http://localhost:8080`.
- `whisper_mode.talon` — Declares the exit phrase for `user.whisper` mode.

## Requirements

- Run the transcription daemon first (zero startup delay):
  - `nvim-container/scribe/scribe-wsl/run_transcription_daemon.sh --daemon` (or run foreground without `--daemon`)
  - The daemon exposes: `/status`, `/toggle`, `/mute`, `/unmute`, `/mode`, `/mode/toggle` (see `nvim-container/scribe/scribe-wsl/README_DAEMON.md`).

## Usage

- Trigger whisper mode programmatically (keyboard, UI, or another Talon command) by calling:
  - `actions.user.whisper_start()`
- Dictate freely (daemon will type/print based on its configured mode).
- Say: `talon whisper done` to end dictation, mute the daemon, and return to normal command mode.

Optional: If you want a voice command to start whisper mode, add this to any `mode: command` context in your Talon user files:

```
# example (not included by default):
# mode: command
# talon whisper: user.whisper_start()
```

## Notes

- Base URL is `http://localhost:8080` by default; change `BASE_URL` in `whisper_mode.py` if needed.
- Notifications use `actions.user.notify(...)` if available; failures won’t crash the flow.
- If the daemon is unreachable, you’ll get a brief notification and the mode won’t switch.

