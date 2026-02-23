---
name: talon-dev-workflow
description: Manage a comprehensive Talon development environment with tmuxinator, including running Talon, monitoring events, editing configs, and managing git changes. Use when starting/stopping Talon development sessions or when the user mentions tmux/tmuxinator for Talon work.
---

# Talon Development Workflow

## Overview
A tmuxinator-based development environment for Talon that provides:
- Talon runtime with colorized output
- Interactive REPL session
- Live event monitoring
- Neovim editor for configs
- STT server integration
- Codex integration
- Git management with lazygit
- Automatic commit of `.talon-list` and `.csv` files on exit

## Quick Start

### Start Development Session
```bash
cd ~/.talon/user/community
tmuxinator start
```

This launches a tmux session with multiple windows:
1. **talon** - Three panes:
   - Talon runtime (`~/talon/run.sh`)
   - Interactive REPL
   - Live event tail (`events.tail()`)
2. **editor** - Neovim editing `user.talon`
3. **stt-server** - Speech-to-text server
4. **codex** - Codex integration
5. **git** - Lazygit for version control

### Restart Session (Reload Talon)
```bash
cd ~/.talon/user/community
tmuxinator stop && tmuxinator start --no-attach
```

From wezterm launcher: **"Talon tmux restart"**

### Stop Session
```bash
cd ~/.talon/user/community
tmuxinator stop
```

## Automatic Git Management

The workflow includes automatic git operations:

### On Session Start (`tx-start.sh`)
```bash
git pull  # Sync latest changes
```

### On Session Exit (`tx-exit.sh`)
```bash
git add *.talon-list *.csv
git commit -m "feat: update *.talon-list"
git push
```

This automatically commits and pushes changes to:
- `.talon-list` files (vocabulary, commands, etc.)
- `.csv` files (homophones, replacements, etc.)

## Configuration Location

- Tmuxinator config: `~/.talon/user/community/.tmuxinator.yml`
- Startup script: `~/.talon/user/community/tx-start.sh`
- Exit script: `~/.talon/user/community/tx-exit.sh`

## Common Operations

### Monitor Talon Events
Switch to the "talon" window, bottom pane to see live events:
```bash
tmux select-window -t talon:0
tmux select-pane -t 2
```

### Access REPL
Switch to the middle pane for interactive Python:
```bash
tmux select-window -t talon:0
tmux select-pane -t 1
```

### Edit Configs
Switch to the editor window:
```bash
tmux select-window -t editor
```

### Manage Git Changes
Switch to the git window for lazygit interface:
```bash
tmux select-window -t git
```

## Integration with WezTerm

Add to wezterm launcher menu:
```lua
{
    label = "Talon tmux restart",
    args = { "bash", "-c", "tmuxinator stop && tmuxinator start --no-attach" },
    cwd = "~/.talon/user/community/",
},
{
    label = "Talon tmux start",
    args = { "bash", "-c", "tmuxinator start" },
    cwd = "~/.talon/user/community/",
},
{
    label = "Talon tmux stop",
    args = { "bash", "-c", "tmuxinator stop" },
    cwd = "~/.talon/user/community/",
},
```

## When to Use This Skill
- User asks about Talon development setup or workflow
- Need to start/stop a comprehensive Talon development environment
- Want live monitoring of Talon events while developing
- Need automatic git management for Talon config files
- User mentions "tmux", "tmuxinator", or "Talon development session"
- Debugging Talon issues that require monitoring runtime + REPL + events simultaneously
