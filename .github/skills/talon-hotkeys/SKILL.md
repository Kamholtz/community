---
name: talon-hotkeys
description: Create global hotkeys in Talon that bind keyboard keys to actions. Use for mapping function keys or key combinations to Talon actions, enabling quick access to frequently-used commands without voice.
---

# Talon Hotkeys

## Overview
Talon hotkeys allow you to bind keyboard keys and key combinations to Talon actions. They work globally across all applications and provide quick access to commands without using voice.

## Basic Hotkey Syntax

### Single Key Binding
Bind a single key to an action:
```talon
key(f1):
    user.whisper_toggle()
```

When you press **F1**, the `user.whisper_toggle()` action executes.

### Common Function Keys
```talon
key(f1):
    user.my_action_one()

key(f2):
    user.my_action_two()

key(f11):
    user.my_action_three()

key(f12):
    user.my_action_four()
```

## Key Combinations

### Modifier Keys
Combine keys with modifiers (`ctrl`, `alt`, `shift`, `cmd`/`super`):

```talon
# Ctrl + F1
key(ctrl-f1):
    user.whisper_toggle()

# Alt + F1
key(alt-f1):
    user.action_alpha()

# Shift + F1
key(shift-f1):
    user.action_beta()

# Cmd/Super + F1 (macOS/Linux)
key(cmd-f1):
    user.action_gamma()

# Multiple modifiers
key(ctrl-alt-f1):
    user.complex_action()

key(ctrl-shift-super-f1):
    user.advanced_action()
```

### Common Key Names
```talon
key(escape):
    user.on_escape()

key(enter):
    user.on_enter()

key(backspace):
    user.on_backspace()

key(tab):
    user.on_tab()

key(space):
    user.on_space()

key(delete):
    user.on_delete()

key(home):
    user.go_home()

key(end):
    user.go_end()

key(pageup):
    user.page_up()

key(pagedown):
    user.page_down()

key(left):
    user.move_left()

key(right):
    user.move_right()

key(up):
    user.move_up()

key(down):
    user.move_down()
```

## Context-Specific Hotkeys

### App-Specific Hotkeys
Only active in specific applications:
```talon
app: vscode
-
key(f8):
    user.vscode_run_tests()

app: vim
-
key(escape):
    key(escape)  # Send ESC to vim instead of handling in Talon
```

### Mode-Specific Hotkeys
Only active in certain modes:
```talon
mode: dictation
-
key(f1):
    user.dictation_help()

mode: command
-
key(f1):
    user.command_help()
```

### Tag-Specific Hotkeys
Only active when certain tags are active:
```talon
tag: user.vim_keys
-
key(ctrl-d):
    key(pagedown)  # vim-style page down

tag: user.test_mode
-
key(f1):
    user.run_current_test()
```

## Practical Examples

### Speech Control Hotkeys
```talon
# Toggle speech on/off
key(f1):
    actions.speech.toggle()

# Disable speech
key(f2):
    actions.speech.disable()

# Enable speech
key(f3):
    actions.speech.enable()
```

### Application Control
```talon
# Toggle application focus
key(alt-f1):
    user.toggle_app("Firefox")

# Quick screenshot
key(shift-f1):
    user.take_screenshot()

# Open terminal
key(ctrl-alt-t):
    user.open_terminal()
```

### Text Editing
```talon
# Quick copy/paste
key(alt-c):
    edit.copy()

key(alt-v):
    edit.paste()

# Quick undo/redo
key(alt-z):
    edit.undo()

key(alt-y):
    edit.redo()

# Insert common text
key(alt-;):
    actions.insert("# TODO: ")
```

### Navigation
```talon
# Quick window switching
key(alt-tab):
    user.next_window()

key(alt-shift-tab):
    user.prev_window()

# Workspace navigation
key(super-1):
    user.switch_workspace(1)

key(super-2):
    user.switch_workspace(2)
```

## Action Examples

### Built-in Actions
```talon
key(f1):
    edit.copy()          # Copy selection

key(f2):
    edit.paste()         # Paste

key(f3):
    edit.undo()          # Undo last action

key(f4):
    edit.redo()          # Redo last undone action

key(f5):
    edit.select_all()    # Select all

key(f6):
    actions.key("ctrl-s")  # Send Ctrl+S (save)

key(f7):
    actions.insert("Hello")  # Insert text

key(f8):
    actions.skip()       # Skip current command
```

### Custom Actions
```talon
# Call user-defined actions from your .py files
key(f1):
    user.my_custom_action()

key(f2):
    user.my_custom_action("param1", "param2")

key(f3):
    user.another_action_with_logic()
```

## File Organization

Create hotkey definitions in a dedicated `.talon` file:

```
~/.talon/user/community/my-config/my-hotkeys.talon
```

Example structure:
```talon
# ~/.talon/user/community/my-config/my-hotkeys.talon
# Global hotkeys for common actions

# Speech control
key(f1):
    actions.speech.toggle()

key(f2):
    actions.speech.disable()

key(f3):
    actions.speech.enable()

# Navigation
key(alt-tab):
    user.next_window()

# Clipboard
key(alt-c):
    edit.copy()

key(alt-v):
    edit.paste()

# App-specific
app: vscode
-
key(f8):
    user.vscode_run_tests()

app: vim
-
key(ctrl-h):
    key(left)
```

## Best Practices

### Avoid Conflicts
- Don't override hotkeys used by your OS or applications
- Test hotkeys in multiple contexts
- Use uncommon key combinations (e.g., `ctrl-alt-super-f12`)
- Document any hotkeys that override default behavior

### Use Consistent Patterns
```talon
# Good: Consistent patterns
key(f1):
    user.action_one()

key(f2):
    user.action_two()

key(f3):
    user.action_three()

# Better: Grouped by function
# Text editing
key(alt-c):
    edit.copy()

key(alt-v):
    edit.paste()

# Speech control
key(f1):
    actions.speech.toggle()
```

### Avoid Too Many Hotkeys
- Use sparingly for frequent actions only
- Too many hotkeys = hard to remember
- Consider using voice commands for most things
- Reserve hotkeys for emergency/critical functions

### Test in Context
```talon
# Test before using in production
mode: test_mode
-
key(f1):
    user.test_action()

# Once verified, move to global scope
```

## Debugging Hotkeys

### Check if Hotkey is Active
In REPL:
```python
from talon import registry

# List all hotkeys
for hotkey in registry.hotkeys:
    print(hotkey)

# Check current context
from talon import ctx
print(f"Current app: {actions.app.name()}")
print(f"Tags: {ctx.tags}")
print(f"Modes: {ctx.modes}")
```

### Test Hotkey Execution
```bash
echo "user.my_action()" | ~/.talon/bin/repl
```

### Monitor Hotkey Events
```bash
echo "events.tail()" | ~/.talon/bin/repl
# Press your hotkey and watch the event output
```

## Common Hotkey Use Cases

### Code Editor Hotkeys
```talon
app: vscode
-
key(f5):
    user.vscode("workbench.action.debug.start")

key(f6):
    user.vscode("editor.action.formatDocument")

key(f7):
    user.vscode("editor.action.goToDefinition")
```

### Terminal Hotkeys
```talon
app: terminal
-
key(alt-1):
    actions.insert("ls -la\n")

key(alt-2):
    actions.insert("git status\n")

key(ctrl-alt-t):
    # Open new terminal tab
    actions.key("ctrl-shift-t")
```

### Browser Hotkeys
```talon
app: firefox
-
key(alt-j):
    user.firefox_open_devtools()

key(alt-r):
    actions.key("f5")  # Reload
```

## When to Use This Skill
- User asks about creating hotkeys or keyboard shortcuts
- Need to bind function keys to Talon actions
- Want quick access to frequently-used commands
- Creating emergency hotkeys (e.g., disable speech)
- User mentions "hotkey", "keyboard shortcut", "function key", or `key()`
- Setting up global keyboard bindings outside of voice commands
- Context-specific key bindings for apps or modes
