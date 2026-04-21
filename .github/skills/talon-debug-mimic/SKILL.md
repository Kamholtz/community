---
name: talon-debug-mimic
description: Debug Talon command behavior using actions.mimic and speech_system.engine_mimic. Use when reproducing command chains, validating macro playback, or isolating recognition vs execution issues.
---

# Talon Debugging with mimic

## Overview
Use mimic to replay spoken commands without speaking.
This is useful for deterministic debugging of command execution, macro playback, and context-sensitive behavior.

This skill covers:
- Replaying parsed command words with `actions.mimic(...)`
- Replaying engine-level phrases with `speech_system.engine_mimic(...)`
- Building quick repeatable repro loops
- Avoiding common mimic debugging traps

## When to Use
Use this skill when:
- A command works sometimes and you need repeatable reproduction
- You are validating macro playback logic
- You want to separate recognition problems from action execution problems
- You need to test command behavior in specific app/mode/tag contexts

## Quick Start
1. Verify current context before replay:
```python
from talon import actions, scope
print(actions.app.name())
print(scope.get("mode"))
print(scope.get("tag"))
```
2. Replay a command as parsed words:
```python
from talon import actions
actions.mimic(["copy", "line"])
```
3. Replay a phrase at engine level (Dragon-style control commands):
```python
from talon import speech_system
speech_system.engine_mimic("go to sleep")
```

## Recommended Debug Workflow
1. Capture the exact target phrase or parsed words.
2. Confirm app, mode, and tags are what the command expects.
3. Run mimic once and observe behavior.
4. Run mimic in a small loop to detect flaky behavior:
```python
from talon import actions
for _ in range(5):
    actions.mimic(["next", "tab"])
```
5. Compare with a nearby known-good command to isolate context mismatch.

## Practical Patterns
### Macro Playback Pattern
```python
# Example pattern used by macro playback systems
for words in recorded_macro:
    actions.mimic(words)
```

### Single-Command Repro Helper
```python
from talon import Module, actions
mod = Module()

@mod.action_class
class Actions:
    def debug_mimic_once(words: list[str]):
        """Replay one command for deterministic debugging."""
        actions.mimic(words)
```

## Common Pitfalls
- `actions.mimic` expects parsed words (list form), not arbitrary free text.
- If nothing happens, context is usually wrong (app/mode/tag), not mimic itself.
- Mimic-based phrases may not include timing metadata expected by some hooks.
- Avoid recursive self-triggering (a mimic command that triggers itself repeatedly).

## Expected Output
- Command side effects in the active app (keypresses, inserts, actions).
- Logs from your own print/debug statements around replay.
- No speech recognition dependency during replay (useful for controlled tests).
