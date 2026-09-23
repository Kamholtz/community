# Fluent Search — New Hotkey Integration Plan

Follow-up to the hotkeys.md alignment fix (commit `90d2c79a`). Goal: cover
the gap identified in that review — result gestures have no voice
equivalent today — with a focus on Clipboard and Files, plus a small
universal set that works across every source.

## 1. Universal result-gesture commands

Most sources in hotkeys.md share the same gesture chords (Ctrl+1 open,
Ctrl+C copy, Delete remove, Shift+Delete permanent-delete/clear, F2
rename, Ctrl+Shift+Return run-as-admin). Rather than one phrase per
source, add one phrase per chord that fires regardless of which source
is currently showing results:

| Phrase | Key | Covers |
|---|---|---|
| `fluent open` | `ctrl-1` | Files open, Apps open, Windows switch-to, Browser open, To Do complete |
| `fluent copy` | `ctrl-c` | Files copy path, Clipboard copy text, Browser copy URL, Calculator copy |
| `fluent delete` | `delete` | Files delete, Clipboard remove from history, Windows close, Kill process |
| `fluent clear` | `shift-delete` | Files permanently delete, Clipboard clear-all-except-saved, Kill process as admin |
| `fluent rename` | `f2` | Files rename, To Do rename |
| `fluent admin` | `ctrl-shift-enter` | Apps open as admin, Command run as admin |

These need `wait_for_fluent_search_window()` treatment only if Fluent
Search isn't already frontmost — in practice they'd be spoken while the
result list is already showing, so a plain `key()` binding is probably
enough (no need to route through `fluent_search.py`). Will confirm this
during implementation.

## 2. Clipboard integration

- **Launcher**: `^fluent clip [<user.text>]$: user.fluent_search("clipboard\t{text or ''}")`
  — same `plugin\t` pattern as the existing `^fluent con` / `^fluent walk`
  commands.
- **Source-specific gesture** not covered by the universal set:
  - `fluent paste` → `ctrl-v` (paste text)
  - `fluent keep` → `ctrl-s` (keep/save result, survives "clear")
- `fluent copy` / `fluent delete` / `fluent clear` from the universal set
  already cover Copy Text / Remove from history / Clear all-except-saved.

## 3. Files integration

- **Launcher**: `^fluent files [<user.text>]$: user.fluent_search("files\t{text or ''}")`
- **Source-specific gestures**:
  - `fluent open folder` → `ctrl-2` (open parent folder)
  - `fluent search folder` → `ctrl-r` (search in parent folder)
  - `fluent open terminal` → `ctrl-3` (open directory in command line)
  - `fluent open with` → `ctrl-4` (open with)
  - `fluent copy file` → `ctrl-5` (copy file itself, distinct from `fluent copy` = copy path)
- `fluent open` / `fluent copy` / `fluent delete` / `fluent clear` /
  `fluent rename` from the universal set cover Open / Copy File Path /
  Delete / Permanently Delete / Rename.

## Open questions to verify before implementing

1. **Plugin keyword spelling** — `apps`, `processes`, `windows` are
   confirmed working today. `clipboard` and `files` are my best guess at
   Fluent Search's internal plugin keyword; need to confirm the actual
   strings (test via `fluent_search.py`'s tab-completion path, or check
   Fluent Search's own docs/config) before wiring the launchers.
2. **Do gesture keys need the app-focus wait?** — if these are always
   spoken with a result list already on screen, a bare `key()` binding in
   the `.talon` file is simpler than adding new `fluent_search.py`
   actions. Only add Python-side wait logic if testing shows the window
   isn't reliably focused.
3. **Naming collisions** — `fluent open`, `fluent copy`, etc. need to be
   checked against other `^fluent ...` and global command patterns
   already in the config to avoid ambiguity.

## Rollout order

1. Verify plugin keywords for `clipboard` and `files` live in Fluent
   Search.
2. Add the two launcher commands (`^fluent clip`, `^fluent files`).
3. Add the universal gesture set (6 commands).
4. Add the Clipboard- and Files-specific gesture commands (2 + 5).
5. Run `check_talon_config.py --talon-errors` after reload, then manually
   speak each phrase against a live Fluent Search window to confirm.
6. Update `hotkeys.md` / `my-changes.md` to record the new commands.
