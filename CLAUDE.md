# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Talon voice control configuration for Windows/Mac/Linux. `.talon` files define voice commands; `.py` files define actions and modules. Talon hot-reloads all files in `~/.talon/user/` automatically when they change.

## Validation & Testing

```bash
# Full gate suite — run before any commit or handoff
python3 .agents/scripts/check_talon_config.py

# Syntax/metadata only — fast iteration during edits
python3 .agents/scripts/check_talon_config.py --skip-tests

# Historical text lint — only when auditing existing files
python3 .agents/scripts/check_talon_config.py --scope all --skip-tests

# Check for Talon reload/startup errors after changing .talon, .talon-list, or Talon Python files
python3 .agents/scripts/check_talon_config.py --talon-errors

# Unit tests (run outside Talon, requires pytest in a non-Talon Python env)
pytest

# Pre-commit linting on changed files
pre-commit run

# Pre-commit linting on all files
pre-commit run --all-files
```

If a gate fails, fix the first actionable error, rerun the same gate, then broaden to the full suite.

## Git Hooks

Pre-commit hooks live in `.githooks/` and run `python3 .agents/scripts/check_talon_config.py`. Enable with:

```bash
git config core.hooksPath .githooks
```

Do not bypass hooks unless the user explicitly approves; if bypassing is necessary, document the failing gate and follow-up fix.

## Architecture

### File Organisation

```text
community/
├── apps/              # App-specific commands (one subdir per app)
├── core/              # Foundational commands (edit, keys, formatters, help, modes)
├── lang/              # Programming language commands + shared tag interfaces
├── tags/              # Context-based tags for conditional command activation
├── plugin/            # Plugin extensions (mouse, symbols, repeater, etc.)
├── settings/          # Global settings/preferences
├── my-config/         # Personal overrides — make local changes here
├── test/              # Unit tests and stubs
├── .agents/           # Agent skills and validation scripts
├── settings.talon     # Global Talon settings
└── my-changes.md      # Track local changes here
```

### .talon File Structure

```talon
# Context header (blank = global)
app.name: Visual Studio Code
-
# Commands below the dash
go to line <number>:
    edit.jump_line(number)
```

### .py File Structure

Python files declare `Module()` objects with `@mod.action_class` to define action signatures, and `Context()` objects with `@ctx.action_class` to implement them. Tags are activated on a context with `ctx.tags = ["user.some_tag"]`.

### Language Tag System

`lang/tags/` contains pairs of `.talon` + `.py` files for shared language features (e.g., `functions.talon`, `comment_line.talon`). Each language in `lang/{language}/` activates the relevant tags and implements the corresponding actions.

### Override Pattern

Override community files by creating new files in `my-config/` or a more-specific `.talon-list` file elsewhere in the user directory (Talon picks the most-specific context header). Never edit community files directly — this minimises merge conflicts when pulling upstream.

### Stored State

Use the actions in [core/stored_state_management/stored_state.py](core/stored_state_management/stored_state.py) to persist state to disk; this keeps state in `stored_state/` where it can be git-ignored.

## Contributing Principles (from CONTRIBUTING.md)

- **P01** — Prefer `[object][verb]` ordering: `file save` not `save file`.
- **P03** — Use `app.bundle` matcher on macOS (most unambiguous).
- **P04** — Use both `app.name` and `app.exe` on Windows (MUICache can break one).
- **P05** — Prefer `.talon-list` files over Python for Talon lists (easier for non-programmers to edit).
- **P08** — Use stored state management actions, not ad-hoc files.
- **P09** — If an action has no valid implementation in a context, raise an exception rather than silently doing nothing.

## Skills Available

Use these agent skills for common development tasks:

| Skill | Use for |
|---|---|
| `talon-dev-workflow` | Start/stop tmuxinator-based Talon dev session |
| `talon-event-monitoring` | Debug missing commands via live event/context/tag monitoring |
| `talon-debug-sim` | Test if a spoken phrase matches a command (no execution) |
| `talon-debug-mimic` | Replay commands through Talon to test execution behaviour |
| `talon-repl` | Inspect live Talon state, call actions, validate contracts |
| `talon-startup-error-troubleshooter` | Triage recent reload/startup exceptions |
| `talon-list-management` | Maintain vocabulary, homophones, `.talon-list` files |
| `talon-hotkeys` | Add keyboard-triggered Talon actions or global shortcuts |

### Startup Error Triage

After editing Talon files, check for errors:

```bash
# Preferred: shows the DEBUG [~] line that triggered the reload
python3 .agents/skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py --since-last-file-change

# Full startup failure investigation
python3 .agents/skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py

# Raw log output / VS Code problem matcher format
python3 my-config/scripts/talon_errors_since_startup.py --since-last-file-change
```

## Troubleshooting Commands Not Firing

1. Check context activation with `talon-event-monitoring`
2. Verify tags are matching (`tag: user.git` in header, `ctx.tags` in Python)
3. Confirm voice recognition detected the phrase (`talon-debug-sim`)
4. Test action execution directly (`talon-repl`)

## Integrations

- **acp-wrapper**: AI code assistant agent (`user.model_acp_agent_command`)
- **talon-ai-tools**: AI-powered voice commands (sibling workspace)
- **talon_hud**: HUD display system (sibling workspace)
- **Cursorless**: Programming/text editing enhancement
- **Rango**: Browser navigation enhancement
