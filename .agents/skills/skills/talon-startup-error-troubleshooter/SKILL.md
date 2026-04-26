---
name: talon-startup-error-troubleshooter
description: Run Talon startup error extraction and troubleshoot failures from the most recent startup using stack traces and exception messages. Use when Talon reports startup failures, when the user asks for recent Talon errors, or when debugging problems that started after the latest Talon launch.
---

# Talon Startup Error Troubleshooter

## Quick Run

Run the helper from the repository root:

```bash
python3 skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py
```

Use `--show-raw` when you need the full error blocks:

```bash
python3 skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py --show-raw
```

Use a custom log path only when needed:

```bash
python3 skills/talon-startup-error-troubleshooter/scripts/scan_and_triage.py --log-path /path/to/talon.log
```

The helper wraps `my-config/scripts/talon_errors_since_startup.py` and keeps that script as the source of truth for "recent" errors (`ERROR` blocks after the latest `Talon Version:` marker).

## Troubleshooting Workflow

1. Run the helper and inspect each triage item (`Exception`, `Stack frame`, `First checks`).
2. For each error block, extract:
- exception type and message
- first user-code file/line if present
- full traceback frames that point to Talon user scripts
3. Prioritize frames in `~/.talon/user/` over Talon internals.
4. Open the implicated file and surrounding lines, then inspect related symbols with `rg`.
5. Form a concrete hypothesis from the exception text and traceback path, then apply the smallest safe fix.
6. Re-run the script to verify the error is gone and check whether a new downstream error appears.
7. Repeat until no startup errors remain or only external/dependency issues remain.

## Error-Type Playbook

Use the traceback and exception message to choose the first check:

- `ModuleNotFoundError` or `ImportError`: verify package availability in Talon's Python environment and verify import paths.
- `AttributeError`: confirm API names and object types at the failing line; check recent refactors and renamed members.
- `KeyError` or `ValueError`: validate command names, settings keys, CSV/list entries, and assumptions about input shape.
- `SyntaxError` or `IndentationError`: fix syntax/indentation at the reported file and line first before any deeper analysis.
- `RuntimeError`: inspect the raising condition and required runtime prerequisites (app state, context activation, external process availability).

## Output Expectations

When reporting progress:

- quote the exact exception line and the decisive traceback frame
- name the file and line being changed
- state the hypothesis before editing
- confirm verification results after re-running the startup error script

If no recent startup errors are found, state that clearly and stop troubleshooting unless the user asks for deeper historical log analysis.
