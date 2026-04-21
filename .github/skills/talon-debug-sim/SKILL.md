---
name: talon-debug-sim
description: Debug Talon command matching using speech_system._sim and sim(...) style REPL tests. Use when testing whether phrases match commands in the current context and inspecting simulated parse results.
---

# Talon Debugging with sim

## Overview
Use sim to test phrase matching and parsing without speaking.
This is ideal for understanding why a spoken phrase does or does not map to a command.

This skill covers:
- Running phrase simulation through Talon
- Inspecting simulation output for match details
- Reproducing matching issues in REPL-driven tests
- Comparing simulated behavior across contexts

## When to Use
Use this skill when:
- A spoken command is recognized but does not execute the expected rule
- You need to test many phrase variants quickly
- You are debugging list, capture, or grammar matching
- You want command-match evidence in logs for issue reports

## Quick Start
1. Simulate a phrase and print details:
```python
from talon import speech_system
result = speech_system._sim("open recent file")
print(result)
```
2. Use REPL-oriented `sim(...)` tests:
```python
sim('open recent file')
sim('test phrase')
```
3. Compare variants side-by-side:
```python
from talon import speech_system
for p in ["next tab", "go next tab", "tab next"]:
    print(p, speech_system._sim(p))
```

## Recommended Debug Workflow
1. Confirm active app/modes/tags before simulating.
2. Simulate the exact failing phrase.
3. Simulate nearby phrase variants to find the matching boundary.
4. If a variant matches, inspect lists/captures used by that command.
5. Save working/failing phrase pairs for regression tests.

## Practical Patterns
### Action Wrapper for Logging
```python
from typing import Union
from talon import Module, speech_system
from talon.grammar import Phrase

mod = Module()

@mod.action_class
class Actions:
    def debug_sim_phrase(phrase: Union[str, Phrase]):
        """Sim phrase and print structured debug output."""
        print("**** Simulated Phrase ****")
        print(speech_system._sim(str(phrase)))
        print("**************************")
```

### REPL Command Injection Pattern
```talon
# In talon_repl context
^test <phrase>$:
    insert("sim('{phrase}')")
    key(enter)
```

## Common Pitfalls
- `speech_system._sim(...)` is an internal-style API; behavior can change between Talon versions.
- A successful simulation in one context may fail in another due to app/mode/tag gating.
- Sim validates matching, but action side effects still depend on downstream action logic.
- Be careful with quotes when injecting `sim('...')` strings into REPL commands.

## Expected Output
- Simulation output showing parse/match information.
- Faster iteration on phrase variants than voice-only testing.
- Clear evidence to distinguish matching issues from action implementation bugs.
