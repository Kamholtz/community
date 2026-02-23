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

## When to Use This Skill
- User asks to test or execute Talon actions
- Need to inspect Talon's current state or configuration
- Debugging voice command issues
- Prototyping Talon functionality before writing full scripts
- Running automated Talon commands from shell scripts
- User mentions "REPL", "Talon Python", or "execute in Talon"