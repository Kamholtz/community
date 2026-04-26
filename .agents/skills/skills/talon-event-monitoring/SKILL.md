---
name: talon-event-monitoring
description: Monitor and troubleshoot Talon events in real-time, debug command execution, inspect hooks, and trace voice recognition events. Use when debugging why commands aren't firing, investigating Talon behavior, or analyzing event flow.
---

# Talon Event Monitoring & Debugging

## Overview
Talon routes events through hooks and handlers. This skill covers:
- Monitoring live Talon events
- Debugging command execution flow
- Inspecting event hooks
- Tracing voice recognition events
- Understanding event filtering

## Live Event Monitoring

### Watch All Talon Events (Blocking)
Launch REPL and run event tail:
```bash
echo "events.tail()" | ~/.talon/bin/repl
```

### Via WezTerm Launcher
**"Talon REPL events"** opens a live event stream showing:
- Voice recognition events (`phrase`, `ready`, etc.)
- Mode changes
- App focus changes
- Custom events
- Timing information

### In Development Session
Run the "talon" window from tmuxinator:
```bash
tmuxinator start talon
# Switch to third pane: tmux select-pane -t talon:0.2
# Shows: echo 'events.tail()' | bin/repl
```

Events display with timestamps and details:
```
event: phrase
time: 2026-02-22 14:23:45.123
phrase: "hello world"
homophones: []

event: ready
time: 2026-02-22 14:23:46.000

event: mode
name: dictation
enabled: true
```

## Event Types and Common Use Cases

### Voice Events
```python
# 'phrase' event - fired when voice command recognized
event_name: "phrase"
phrase: str          # The recognized text
homophones: List[str]  # Alternative pronunciations

# 'ready' event - fired when speech recognition is ready
event_name: "ready"

# 'trigger' event - custom trigger events
phrase: str
```

### Context Events
```python
# 'app_focus' event - window/app changed
event_name: "app_focus"
app: App object

# 'mode' event - mode enabled/disabled
event_name: "mode"
name: str           # mode name
enabled: bool
```

## Debugging Command Execution

### Check if Command is Firing

1. **Start event monitoring:**
```bash
echo "events.tail()" | ~/.talon/bin/repl
```

2. **Speak the command** and watch output
3. **Look for:**
   - `phrase` event with your command text
   - If no event appears: speech recognition issue
   - If event appears but command doesn't execute: matching issue

### Debug What Command Matched

Use REPL to test matching:
```python
# Check if action exists
hasattr(actions.user, "my_command")

# Check current mode
from talon import ctx
print(ctx.modes)

# Check app context
print(actions.app.name())

# Check window title
import talon.ui
front_app = talon.ui.active_app()
print(f"App: {front_app.name}, Window: {front_app.window.title}")
```

### Test Command Directly
```bash
# Execute action from shell
echo "actions.user.my_command()" | ~/.talon/bin/repl

# Or specific actions
echo "actions.insert('Hello')" | ~/.talon/bin/repl
echo "actions.key('ctrl-s')" | ~/.talon/bin/repl
```

## Event Filtering and Context

### Understand Talon's Event Flow

1. **Event fires** (e.g., `phrase`)
2. **Talon evaluates context**:
   - Current app
   - Active modes
   - Tag matches
   - File context
3. **Commands matched** based on context
4. **Best match executed**

### Context Requirements for Commands
```talon
# This command only runs in vim
app: vim
-
exit insert mode: key(escape)

# This command needs two tags
tag: user.vim_keys
tag: user.insert_mode
-
map leader: user.insert_map()

# Mode-specific command
mode: dictation
-
dictation mode command: actions.insert("text")
```

## Interactive Event Analysis

### Monitor Specific Event Type
In REPL:
```python
from talon import ui, app, ctx

# Get current app
print(f"Active app: {actions.app.name()}")

# Check if tag is active
print(f"Tags: {ctx.tags}")

# Check modes
print(f"Modes: {ctx.modes}")

# Check registered commands
from talon import registry
for cmd in registry.commands[:5]:
    print(cmd)
```

### Trace a Specific Command
```python
# Check if command is registered
from talon import registry
cmds = [c for c in registry.commands if "my_command" in str(c)]
print(f"Matching commands: {cmds}")

# Check scope requirements
for cmd in cmds:
    print(f"Scope: {cmd.scope}, requires: {cmd.ctx_requirements}")
```

## Event Monitoring Integration

### Start Monitoring from WezTerm
Use launcher: **"Talon REPL events"**
- Opens in new pane
- Live event stream
- Press `Ctrl+C` to stop

### Start from Tmuxinator
```bash
tmuxinator start talon
# Three panes in "talon" window:
# - Pane 1: Talon runtime
# - Pane 2: REPL
# - Pane 3: Event tail (events.tail())
```

### Script-Based Monitoring
Create a monitoring script:
```bash
#!/bin/bash
# watch_events.sh
echo "events.tail()" | ~/.talon/bin/repl | grep -E "phrase|mode|ready"
```

## Troubleshooting with Events

### Command Not Executing?
1. Start event monitoring
2. Speak command - verify `phrase` event appears
3. If no event: speech recognition isn't capturing
4. If event appears but no action: context mismatch
5. Check `ctx.modes`, `ctx.tags`, current app

### Too Many Events Printed?
Add filtering to your monitoring:
```bash
# Only show phrase events
echo "events.tail()" | ~/.talon/bin/repl 2>&1 | grep "phrase"

# Only show mode changes
echo "events.tail()" | ~/.talon/bin/repl 2>&1 | grep "mode"
```

### Events Stop After a While?
- REPL session may have timed out
- Restart with `echo "events.tail()" | ~/.talon/bin/repl`
- Or use tmuxinator window which handles restarts

## Advanced Event Usage

### Subscribe to Events Programmatically
In a Talon `.py` file:
```python
from talon import hooks

def on_phrase(phrase):
    print(f"Phrase detected: {phrase}")

hooks.register("phrase", on_phrase)
```

### Custom Events
Define and trigger:
```python
from talon import hooks

# Trigger custom event
hooks.trigger("my_custom_event", data={"key": "value"})

# Listen for it
def on_my_event(data):
    print(f"Custom event fired: {data}")

hooks.register("my_custom_event", on_my_event)
```

## When to Use This Skill
- User asks why a Talon command isn't executing
- Need to debug voice recognition issues
- Want to monitor Talon's event flow
- Troubleshooting context/mode matching
- Understanding why specific commands are/aren't available
- User mentions "events", "live monitoring", "debugging commands"
- Investigating timing or order of Talon events
