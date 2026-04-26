---
name: talon-repl
description: Execute Python code in Talon's REPL to interact with the Talon API, test actions, inspect variables, debug commands, and run scripts. Use for testing Talon actions, querying state, debugging voice commands, or programmatically controlling Talon.
---

# Talon REPL Skill

## Overview
The Talon REPL provides an interactive Python shell with full access to Talon's API. It can be used to:
- Execute Talon actions and test voice commands programmatically
- Inspect Talon's state, settings, and registered actions
- Debug voice command issues
- Run quick Python scripts with Talon context
- Prototype new Talon functionality

## Usage Methods

### Interactive REPL
Launch an interactive Python session:
```bash
~/.talon/bin/repl
```

This opens a Python REPL with the Talon API loaded and ready to use.

### Piping Commands
Execute single commands or scripts by piping them into the REPL:
```bash
echo "actions.speech.disable()" | ~/.talon/bin/repl
```

This is particularly useful for:
- Running one-off commands without entering interactive mode
- Executing Talon commands from shell scripts
- Automating Talon state changes
- Testing actions quickly from the terminal
- Binding Talon commands to terminal shortcuts or launcher menus

Common piped commands:
```bash
# Toggle speech recognition
echo "actions.speech.toggle()" | ~/.talon/bin/repl

# Monitor Talon events (useful for debugging)
echo "events.tail()" | ~/.talon/bin/repl
```

### Multiple Commands
Execute multiple statements by piping multi-line input:
```bash
echo -e "from talon import actions\nprint(actions.app.name())" | ~/.talon/bin/repl
```

For compound statements such as loops, `try`/`except`, or nested parsing logic, wrap the payload in `exec("""...""")` when piping it. This avoids REPL indentation and block-submission issues:
```bash
printf 'exec("""from talon import actions\nfor name in [\"one\", \"two\"]:\n    print(name)\n""")\n' | ~/.talon/bin/repl
```

Or using heredoc syntax:
```bash
~/.talon/bin/repl << EOF
from talon import actions, ctx
print(f"Current app: {actions.app.name()}")
print(f"Active modes: {ctx.modes}")
EOF
```

## Common Use Cases

### Testing Actions
```bash
# Toggle speech recognition on/off
echo "actions.speech.toggle()" | ~/.talon/bin/repl

# Disable speech recognition
echo "actions.speech.disable()" | ~/.talon/bin/repl

# Enable speech recognition
echo "actions.speech.enable()" | ~/.talon/bin/repl

# Watch Talon events in real-time (blocking, use Ctrl+C to stop)
echo "events.tail()" | ~/.talon/bin/repl

# Insert text
echo "actions.insert('Hello from Talon!')" | ~/.talon/bin/repl

# Simulate keypress
echo "actions.key('ctrl-s')" | ~/.talon/bin/repl
```

### Inspecting State
```python
# Check current application
actions.app.name()

# List available actions
dir(actions)

# Check active modes
from talon import ctx
print(ctx.modes)
```

### Debugging
```python
# Test if a specific action is available
hasattr(actions.user, "my_custom_action")

# Check registered commands
from talon import registry
list(registry.commands)
```

### Debugging Action Contracts
Use the REPL to validate the live contract between Talon modules when a stack trace shows one module calling another module's action. This is especially useful for callbacks, draw handlers, lists, captures, and other places where static code passes strings or structured values into registered actions.

1. Read the stack trace from the outer callback to the failing action.
2. Inspect the caller's input values and the callee's accepted values in code.
3. Reproduce the failing action call in the REPL with the smallest dummy input that exercises the same path.
4. After fixing one value, validate the entire local data structure that feeds the action, because repeated callbacks often reveal only the first invalid entry.
5. Trigger the user-facing action through the REPL and check the log tail for fresh errors. Startup-error scripts may continue to show old entries until Talon restarts.

Example: validate whether window snap labels used by a UI are accepted by the live snap action:
```bash
printf 'exec("""from talon import actions\nfrom talon.types import Rect\nfor name in [\"top center\", \"top center third\", \"middle\", \"center\"]:\n    try:\n        r = actions.user.snap_apply_position_to_rect(Rect(0, 0, 300, 200), name)\n        print(name, \"=>\", (r.x, r.y, r.width, r.height))\n    except Exception as e:\n        print(name, \"=>\", type(e).__name__, e)\n""")\n' | ~/.talon/bin/repl
```

Example: parse a Python file and validate every label from a list against a live Talon action:
```bash
printf 'exec("""import ast\nfrom pathlib import Path\nfrom talon import actions\nfrom talon.types import Rect\n\nmodule = ast.parse(Path(\"/home/carl/.talon/user/community/plugin/quick_pick/quick_pick.py\").read_text())\nsnap_positions = []\nfor node in module.body:\n    if isinstance(node, ast.Assign):\n        for target in node.targets:\n            if isinstance(target, ast.Name) and target.id == \"snap_positions\":\n                snap_positions = ast.literal_eval(node.value)\n\nfailures = []\nfor group in snap_positions:\n    for name in group:\n        try:\n            actions.user.snap_apply_position_to_rect(Rect(0, 0, 300, 200), name)\n        except Exception as e:\n            failures.append((name, type(e).__name__, str(e)))\nprint(\"failures\", failures)\nprint(\"checked\", sum(len(group) for group in snap_positions), \"labels\")\n""")\n' | ~/.talon/bin/repl
```

Example: trigger a UI action after patching, then inspect the log for new callback errors:
```bash
printf 'exec("""from talon import actions\nactions.user.quick_pick_show()\nactions.sleep(\"200ms\")\nactions.user.quick_pick_show()\nprint(\"quick pick show/hide invoked\")\n""")\n' | ~/.talon/bin/repl

tail -n 120 ~/.talon/talon.log
```

## When to Use This Skill
- User asks to test or execute Talon actions
- Need to inspect Talon's current state or configuration
- Debugging voice command issues
- Prototyping Talon functionality before writing full scripts
- Running automated Talon commands from shell scripts
- User mentions "REPL", "Talon Python", or "execute in Talon"
