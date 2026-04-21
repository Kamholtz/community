# AGENTS - Talon Config Maintenance & Updates

## Purpose

This workspace contains a comprehensive Talon voice control configuration for Linux systems. It provides voice commands and customizations across multiple application domains, development environments, and system utilities. The configuration is continuously updated and maintained to support new tools, refine command recognition, and improve user experience.

## Overview of Key Components

### Configuration Categories

- **apps/**: Voice commands for specific applications (editors, browsers, terminals, etc.)
- **core/**: Core voice commands and foundational functionality
- **lang/**: Language-specific voice commands (Python, JavaScript, etc.)
- **settings/**: Global settings, themes, and preferences
- **tags/**: Context-based tags for conditional command activation
- **plugin/**: Plugin-based extensions and integrations
- **my-config/**: Personal customizations and overrides

### File Organization

```
community/
├── apps/              # Application-specific commands
├── core/              # Core Talon framework
├── lang/              # Language/framework commands
├── my-config/         # User customizations (local changes)
├── settings/          # Global configuration
├── tags/              # Context tags
├── test/              # Tests and validation
├── my-changes.md      # Tracking of local changes
└── settings.talon     # Global Talon settings
```

## Starting a Talon Development Session

Use the **talon-dev-workflow** skill to manage development sessions:

1. Start a tmuxinator session with integrated Talon environment:
   ```bash
   tmuxinator start talon
   ```
   This launches:
   - Talon running instance
   - Event monitor for real-time debugging
   - Config editor and file monitor
   - Git tracking for changes

2. Monitor Talon events and behavior:
   - Use event monitoring tools to debug why commands aren't firing
   - Check context conditions and tag activation
   - Trace voice recognition events

3. Make incremental changes in `my-config/` directory
4. Verify changes with live testing
5. Commit changes with clear commit messages

## Updating and Maintaining the Config

### Common Update Tasks

#### Adding a New Voice Command

1. Identify the appropriate location:
   - App-specific: `apps/[appname]/`
   - Language-specific: `lang/[language]/`
   - Core functionality: `core/`

2. Edit or create a `.talon` file with your command:
   ```talon
   <voice_phrase>:
       action()
   ```

3. Test via live reload or Talon REPL
4. Move to permanent location if working in `my-config/`

#### Customizing Lists and Vocabulary

Use the **talon-list-management** skill to:
- Override existing Talon lists
- Create custom `.talon-list` files
- Manage CSV-based vocabularies
- Configure homophones for improved recognition

Example locations:
- `settings/` for global lists
- App-specific directories for app-scoped customization

#### Creating Global Hotkeys

Use the **talon-hotkeys** skill to:
- Bind function keys to Talon actions
- Create keyboard shortcuts that work globally
- Map complex key combinations to commands

#### Debugging Issues

Use the **talon-event-monitoring** skill to:
- Monitor which events are firing
- Check if context/tags are activating correctly
- Trace voice recognition pipeline
- Inspect command execution hooks

### Validation & Testing

- Run test suite: `python -m pytest test/`
- Use Talon REPL to execute and test actions interactively
- Leverage **talon-repl** skill for programmatic testing
- Check recent startup errors with error troubleshooter task

### Tracking Changes

- Local changes should be documented in [my-changes.md](my-changes.md)
- Use git to track modifications across config updates
- When pulling upstream changes, merge carefully into your `my-config/` overrides

## Key Customization Points

### Settings & Preferences

- [settings.talon](settings.talon): Global Talon settings
- [settings/](settings/): Configuration organization
- Modify recognition parameters, behavior, and integrations here

### Context & Tags

- [tags/](tags/): Define context-specific behaviors
- Use tags to activate commands in specific applications or modes
- Example: `tag: user.git` activates git-specific commands

### Application Commands

- Browse [apps/](apps/) for application-specific customizations
- Copy commands from community into [my-config/apps/](my-config/) to override
- Customize recognition for frequently-used tools

### Language Commands

- [lang/](lang/): Programming language-specific voice commands
- Customize snippets and syntax for your languages
- Override in [my-config/lang/](my-config/lang/) for personal preferences

## Development Workflow with VS Code

1. **Open workspace**: `user.code-workspace`
2. **Install community settings**: Python environment configured in workspace
3. **Live editing**: Changes in `my-config/` take effect immediately
4. **Terminal integration**: Use built-in terminals for git and testing
5. **File monitoring**: Watch for conflicts between community and custom versions

## Troubleshooting

### Commands Not Firing

1. Check context activation with event monitor
2. Verify tags are correctly matched
3. Confirm voice recognition detected the phrase
4. Use REPL to test action execution directly

### Startup Errors

Use **talon-startup-error-troubleshooter** task to:
- Extract recent startup failures
- View stack traces and exceptions
- Debug initialization issues

### Recognition Issues

- Use homophones and list customization to improve recognition
- Test with REPL to isolate voice recognition vs command execution
- Check microphone input levels and noise

## References & Resources

- **Talon Official**: https://talon.wiki/
- **Community Config**: Check upstream for new features
- **Skill Resources**:
  - `talon-basic-customization`: Config fundamentals
  - `talon-talon-file-syntax`: .talon file syntax reference
  - `talon-dev-workflow`: Complete development session management

## Integration with Other Workspaces

This workspace integrates with:
- **acp-wrapper**: AI code assistant agent (via `user.model_acp_agent_command`)
- **talon-ai-tools**: AI-powered voice commands
- **phony-generated-rules**: Dynamically generated Talon rules
- **talon_hud**: HUD display system

## Notes

- Always test voice commands in a controlled environment
- Use dry-run modes when available for potentially destructive commands
- Keep `my-config/` in git for personal backup and version history
- Document significant changes in [my-changes.md](my-changes.md)
- Pull upstream updates periodically and merge carefully into local overrides
