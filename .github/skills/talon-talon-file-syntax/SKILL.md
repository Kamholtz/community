---
name: talon-talon-file-syntax
description: Learn .talon file syntax including context headers, voice command definition, and built-in actions.
---

# .talon File Syntax

## File Structure

A `.talon` file has two parts: a context header (optional) and a body.

```talon
title: /Gmail/
-

# Body starts here
find on page: key(ctrl-f)
```

## Context Header

The context header (lines before the `-` divider) defines when the file is active. It's **optional**—without it, the file is always active.

### Context Matchers

Common matchers include:

- `title: /Gmail/` - Active when "Gmail" is in the window title
- `os: mac` - Active on macOS
- `app.exe: my_game.exe` - Active when the app filename matches
- `mode: command` - Active in command mode

### No Context Header

If you omit the context header, the file is always active:

```talon
# No context header—these commands are always available
select all: key(ctrl-a)
save: key(ctrl-s)
```

## Body

The body defines voice commands and settings. It can include:
- Voice command definitions
- Settings blocks
- Comments (lines starting with `#`)

## Voice Commands

### Basic Syntax

Commands start with the spoken phrase followed by a colon:

```talon
spoken phrase here: action()
```

### Single Action

Define on one line:

```talon
find on page: key(ctrl-f)
```

### Multiple Actions

Put each action on its own indented line:

```talon
insert bold text:
    key(ctrl-b)
    insert("type in this text (it will be bolded)")
    key(ctrl-b)
```

### Separating Commands

Use one or more blank lines between commands.

## Built-in Actions

Here are commonly used actions:

| Action | Description |
|--------|-------------|
| `key(ctrl-a)` | Presses the specified keys (see key names below) |
| `insert("text")` | Types the specified text |
| `sleep(100ms)` | Waits for specified duration (e.g., 100ms) |
| `mouse_move(100, 200)` | Moves mouse to screen coordinates (x=100, y=200) |
| `mouse_scroll(0, -10)` | Scrolls; note: args are (y, x), not (x, y) |
| `mouse_click(0)` | Clicks mouse button; 0=left, 1=right |
| `speech.toggle()` | Toggles speech listening |

### More Actions

To see all available actions:
1. Open the Talon REPL (right-click Talon icon → Scripting → Console)
2. Type `actions.list()` and press enter

## Common Key Names

| Key | Name |
|-----|------|
| Enter | `enter` |
| Escape | `escape` |
| Tab | `tab` |
| Space | `space` |
| Backspace | `backspace` |
| Delete | `delete` |
| Home | `home` |
| End | `end` |
| Page Up | `pageup` |
| Page Down | `pagedown` |
| Arrow keys | `left`, `right`, `up`, `down` |

### Modifier Keys

Combine with modifiers: `ctrl`, `shift`, `alt`, `cmd` (macOS) or `super` (Linux)

```talon
key(ctrl-a)       # Ctrl+A
key(cmd-a)        # Cmd+A (macOS)
key(ctrl-shift-s) # Ctrl+Shift+S
```

## Settings Block

Change Talon settings within a context:

```talon
title: /my_game.exe/
-
settings():
    key_hold = 32
```

Multiple settings:

```talon
settings():
    key_hold = 32
    speech.timeout = 0.5
```

Use `settings.list()` in the REPL to see all available settings.

## Comments

Lines starting with `#` are comments and ignored by Talon:

```talon
# This is a comment
touch:
    mouse_click(0)
    # This comment explains the next line
    user.grid_close()
```

## Error Messages

Talon provides helpful error feedback. Check the Talon log (right-click Talon icon → Scripting → View log) for errors.

Example error output shows:
- The file with the problem
- The approximate line number
- What Talon expected

If your file contains a syntax error and won't load, the log will tell you exactly where the problem is.
