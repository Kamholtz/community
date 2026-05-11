# Reusable App Quick Pick Menus

## Current State

Branch: `quick-pick-app-menus`

Checkpoint commit: `db87895d Add reusable app quick pick menus`

This feature refactors the original quick pick ring into a reusable menu engine and adds a first app-specific menu for VS Code. The checkpoint visual regressions have now been addressed:

- The contextual `APP` button now uses the open left-side ring slot at `165` degrees, between the global `TASK` and back/navigation buttons.
- The original global quick-pick icon labels have been restored when the configured font has glyph coverage, with readable text fallbacks for platforms/fonts that do not.

Current validation:

- `python3 .agents/scripts/check_talon_config.py --skip-tests` passes when run outside the sandbox so Python can write `__pycache__`.
- `python3 .agents/scripts/check_talon_config.py` passes when run outside the sandbox; `pytest` is skipped because it is not installed.
- `python3 .agents/skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py --since-last-file-change` reports no errors since the quick-pick reload.

## Architecture

The reusable quick pick model lives in `plugin/quick_pick/quick_pick.py`.

Core data structures:

- `QuickPickOption`: rectangular option with `text`, `callback`, and optional `move_mouse`.
- `QuickPickCircleOption`: circular/ring option with `text`, `degrees`, `callback`, and optional `move_mouse`.
- `QuickPickView`: one renderable view with circle options, optional left panel options, optional bottom row options, and optional snap-position panel.
- `QuickPickMenu`: menu identity plus a `view_provider`, so views can be generated dynamically each time the canvas draws.

Important actions:

- `user.quick_pick_show()`: toggles the global quick pick.
- `user.quick_pick_global_show()`: opens the global quick pick directly.
- `user.quick_pick_app_menu_get()`: default provider hook; returns `None` unless the active app context overrides it.
- `user.quick_pick_app_show()`: opens the active app menu when one exists.

The global quick pick keeps the previous behavior:

- Ring options for mouse/navigation/window/search actions.
- Left panel with running applications.
- Bottom row with media/tracking controls.
- Right snap-position panel.

The global ring adds an `APP` option only when `user.quick_pick_app_menu_get()` returns a `QuickPickMenu` for the active app.

## Current UI

Open the global menu with:

```talon
quick pick
```

The global quick-pick canvas shows:

- A central ring for high-frequency mouse, navigation, browser, tab, task-manager, window-switcher, and search actions.
- A contextual `APP` ring button when the focused application exposes an app quick-pick provider. This button opens the app-specific menu.
- A left vertical panel of running applications that focuses the selected app.
- A bottom horizontal row for media controls and eye-tracking toggle.
- A right snap-position panel for moving the active window into predefined screen regions.

The global ring labels use icon glyphs when the configured font supports them. If glyph coverage is unavailable, the same buttons fall back to plain labels such as `DRAG`, `CTRL`, `RIGHT`, `TASK`, `WIN`, and `SEARCH`. Media controls similarly prefer transport glyphs and fall back to `PREV`, `PLAY`, and `NEXT`.

The contextual `APP` button is currently text-labelled and positioned on the upper-left arc at `165` degrees. It no longer overlaps the existing `TASK` ring item at `140` degrees.

Clicking a button closes the canvas and runs its callback. Buttons with `move_mouse=True` first restore the mouse to the location where quick pick was opened.

The `EYE OFF` bottom-row button is handled specially: it turns eye tracking off, then restores the cursor to the position captured just before quick pick opened. This keeps the pointer hovering over the same target that was under the cursor before opening the menu.

## VS Code Provider

The first app provider is in `apps/vscode/vscode.py`.

It overrides `user.quick_pick_app_menu_get()` under the existing `app: vscode` context and returns a `QuickPickMenu("vscode", "VS Code", get_vscode_quick_pick_view)`.

Voice command:

```talon
code menu: user.quick_pick_app_show()
```

VS Code circle options currently map to:

- `TASK`: `workbench.action.tasks.runTask`
- `BUILD`: `workbench.action.tasks.build`
- `TERM`: `workbench.action.terminal.focus`
- `LAST`: `workbench.action.terminal.runRecentCommand`
- `TEST`: `testing.reRunLastRun`
- `FIX`: `editor.action.quickFix`
- `CMD`: `workbench.action.showCommands`
- `BACK`: `user.quick_pick_global_show()`

VS Code bottom row currently maps to:

- Explorer
- Search
- Source Control
- Problems
- Output
- Magit status in a new window
- VS Code reload

The VS Code left panel shows recent replayable commands recorded while VS Code was active.

When VS Code is focused, the UI exposes two paths into the app menu:

- Say `code menu` to open the VS Code menu directly.
- Say `quick pick`, then click the contextual `APP` ring button.

The VS Code app menu shows:

- A central ring of VS Code commands for tasks, build, terminal focus, recent terminal command, last test rerun, quick fixes, command palette, and returning to the global quick pick.
- A left vertical panel of recent replayable Talon commands that were spoken while VS Code was active.
- A bottom horizontal row of VS Code workbench views and utilities: Explorer, Search, Source Control, Problems, Output, Magit status in a new window, and VS Code reload.

The `BACK` ring button switches back to the global quick pick view by calling `user.quick_pick_global_show()`.

## Command History Replay

The command history extension is in `plugin/command_history/command_history.py`.

History now stores structured entries instead of only display strings:

- `id`
- display `text`
- raw mimic `words` when available
- active app name
- active app executable
- timestamp

Existing callers still work:

- `user.history_get(number)` still returns the display text string.

New actions:

- `user.history_get_recent_for_active_app(limit)` returns recent replayable entries for the active app.
- `user.history_replay_entry(entry_id)` replays an entry with `actions.mimic(words)`.

There is a small guard to avoid storing menu-opening commands such as `quick pick` and `code menu`, and to avoid immediately recording the replayed phrase.

## Next Work

Improve menu ergonomics:

- Consider titles/headings or section labels if the panel becomes visually ambiguous.
- Consider app-specific icon/short label instead of generic `APP`.
- Consider whether `BACK` should switch views in-place without closing/reopening the canvas.
- Consider reserving an explicit contextual slot in the base ring if more app-aware global actions are added later.

Make app providers easier to add:

- Add a short example provider template in this document after the VS Code implementation settles.
- Consider moving provider helpers into a separate quick-pick module if `quick_pick.py` grows too large.

## Validation Commands

Run these after changes:

```powershell
python3 .agents/scripts/check_talon_config.py --skip-tests
python3 .agents/scripts/check_talon_config.py
python3 .agents/scripts/check_talon_config.py --talon-errors
```

Notes from the checkpoint:

- The gates pass when run outside the sandbox so Python can write `__pycache__`.
- `pytest` was skipped because it was not installed.
- `apps/vscode/vscode.talon` decorative equals-sign separators were changed to dashes because the gate treats long equals runs as merge-conflict markers.
