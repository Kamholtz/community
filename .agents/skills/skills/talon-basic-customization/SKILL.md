---
name: talon-basic-customization
description: Understand Talon customization fundamentals, including .talon vs .py files, the Talon user directory structure, and how to organize customizations.
---

# Basic Talon Customization

## Overview

All Talon customization consists of files with `.talon` or `.py` extensions placed in the Talon user directory (`~/.talon/user/` on macOS/Linux, `%APPDATA%\Talon\user` on Windows).

Talon doesn't care how you organize files within this directory—subdirectories and file names are there for your convenience and understanding.

## .talon Files vs .py Files

### .talon Files
- **Purpose**: Provide a succinct way of mapping spoken commands to behavior
- **Language**: Dedicated syntax designed specifically for Talon
- **Design goal**: Simple syntax with good error feedback
- **Use case**: Defining voice commands, context headers, and settings

### .py Files
- **Purpose**: Implement behavior and functionality used by `.talon` files
- **Language**: Python scripting
- **Note**: You do not need to know how to code to use Talon; this is for advanced users who want to extend functionality

## User Directory Organization

### Recommended Approach (Option B)
Instead of editing Talon Community files directly, maintain your own separate customization directory alongside the Community files:

```
~/.talon/user/
├── community/           # Talon Community (unchanged from GitHub)
├── my_talon/           # Your personal customizations
├── cursorless-talon/   # Third-party plugins
└── other-config/       # Additional configuration
```

**Benefits**:
- Easier to keep upstream in sync and track your changes
- Updates to Community files won't overwrite your customizations
- Cleanly separates your modifications from upstream

### Avoid Option A
Directly editing Community files makes it difficult to:
- Track what you've modified
- Keep up with upstream changes
- Reapply your changes after updates

## Auto-Loading and Reloading

Talon automatically picks up and applies changes to `.talon` and `.py` files in your user directory. You don't need to restart Talon when you modify files—changes are loaded immediately. Watch the Talon log to confirm files are loaded.

Log entries look like:
```
2021-09-02 17:33:36 DEBUG [+] /path/to/file.talon
```

The `[+]` indicates successful loading; `[-]` indicates unloading.
