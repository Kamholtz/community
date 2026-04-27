# ACP Wrapper Integration - Quick Reference

## What is This?
This directory contains documentation for integrating Talon-AI-Tools with the ACP wrapper (`/home/carl/repos/acp-wrapper`) to query LLMs via the Agent Client Protocol.

## Current Status Summary
✅ **Integration Complete** | ⚠️ **Testing & Documentation In Progress**

| Component     | Status         | Notes                                                   |
| ------------- | -------------- | ------------------------------------------------------- |
| Architecture  | ✅ Complete     | Transport layer, settings, routing all in place         |
| ACP Transport | ✅ Complete     | `acp_client.py` fully implemented                       |
| Model Routing | ✅ Complete     | `send_request_to_acp()` and wrapper detection working   |
| Settings      | ✅ Complete     | All configuration options defined in `talonSettings.py` |
| Documentation | ⚠️ In Progress  | User guide and integration docs needed                  |
| Testing       | ⚠️ Minimal      | Only `strip_markdown()` tested; ACP tests needed        |
| Diagnostics   | ⚠️ Partial      | Error messages working; health check not implemented    |
| End-to-End    | ⚠️ Not Verified | Manual testing needed with real wrapper                 |

## Quick Links

### For Users
- [How to Install & Configure](talon-ai-tools-acp-plan.md#option-a---external-virtualenv-wrapper) - Setup guide for ACP wrapper
- [Talon-AI-Tools Readme](../../talon-ai-tools/readme.md) - Full feature documentation

### For Developers
- [Integration Plan](talon-ai-tools-acp-wrapper-integration.md) - Detailed work items and timeline
- [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md) - Architecture and implementation walkthrough
- [Agent Tracking](AGENT-acp-wrapper-integration.md) - Work items and progress tracking

### Reference Documents
- [ACP Wrapper Virtualenv Plan](acp-wrapper-venv-plan.md) - Original wrapper project plan
- [ACP Integration Alternatives](acp-alternatives-plan.md) - Why wrapper was chosen over vendoring

## Getting Started

### As a User
1. **Install the wrapper**:
   ```bash
   cd ~/repos/acp-wrapper
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Talon** (in your user.talon):
   ```talon
   user.model_endpoint = "acp"
   # Optional - these are the defaults:
   # user.model_acp_use_wrapper = 1
   # user.model_acp_agent_command = "codex-acp"
   ```

3. **Run a voice command**:
   - Use any GPT command like "ask what is python"
   - Response will route through ACP wrapper to your configured LLM

### As a Developer Working on Integration

1. **Read the architecture overview**:
   - See [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md#architecture-overview)

2. **Check current implementation status**:
   - Review [Agent Tracking](AGENT-acp-wrapper-integration.md) for what's done

3. **Key files to review**:
   ```
   ~/.talon/user/talon-ai-tools/
   ├── lib/acp_client.py          # Transport implementation
   ├── lib/modelHelpers.py        # Routing and wrapper detection
   ├── lib/talonSettings.py       # Settings definitions
   └── readme.md                  # User documentation
   ```

4. **Run tests** (when available):
   ```bash
   cd ~/.talon/user/talon-ai-tools
   python -m pytest .test/
   ```

## Configuration Examples

### Example 1: Default (Wrapper If Available, Fallback to codex-acp)
```talon
user.model_endpoint = "acp"
```

### Example 2: Always Use Wrapper
```talon
user.model_endpoint = "acp"
user.model_acp_use_wrapper = 1
```

### Example 3: Use Direct codex-acp (No Wrapper)
```talon
user.model_endpoint = "acp"
user.model_acp_use_wrapper = 0
user.model_acp_agent_command = "codex-acp"
```

### Example 4: Custom Agent Command
```talon
user.model_endpoint = "acp"
user.model_acp_agent_command = "/path/to/my-agent"
user.model_acp_agent_args = "--config my.toml"
user.model_acp_agent_cwd = "/project/root"
user.model_acp_agent_env = "OPENAI_API_KEY=sk-xxx CUSTOM_VAR=value"
```

### Example 5: Wrapper Override via Environment
```bash
export ACP_WRAPPER_COMMAND="/custom/path/to/wrapper"
# Then run Talon - it will use this wrapper instead of default
```

## Architecture at a Glance

```
User Voice Command
    ↓
send_request() routes based on user.model_endpoint
    ↓
send_request_to_acp() (called if endpoint == "acp")
    ↓
_get_acp_transport() - singleton factory
    ↓
_resolve_acp_agent_settings() - determines wrapper vs direct
    ↓
ACPTransport - manages subprocess and async
    ↓
run-acp-agent wrapper script (if available)
    ↓
codex-acp binary with proper environment
    ↓
LLM API (Claude, GPT, etc.)
    ↓
Response back through transport → Talon destination
```

## Key Settings

| Setting                        | Type | Default                      | Purpose                                  |
| ------------------------------ | ---- | ---------------------------- | ---------------------------------------- |
| `user.model_endpoint`          | str  | `https://api.openai.com/...` | Set to `"acp"` to use ACP                |
| `user.model_acp_use_wrapper`   | bool | `True`                       | Prefer wrapper if found                  |
| `user.model_acp_agent_command` | str  | `"codex-acp"`                | Agent binary path                        |
| `user.model_acp_agent_args`    | str  | `""`                         | Extra arguments                          |
| `user.model_acp_agent_cwd`     | str  | `""`                         | Working directory                        |
| `user.model_acp_agent_env`     | str  | `""`                         | Environment variables (KEY=VALUE format) |

## Error Handling

The integration includes automatic error recovery:

1. **Transport Initialization Fails**
   - Logged with full context (command, args, env)
   - Notification shown: "ACP Failure (context): error message"
   - User can retry or disable ACP

2. **Subprocess Dies**
   - Transport reset and reconnection attempted on next request
   - No manual intervention needed for transient failures

3. **SDK Missing**
   - Clear error: "ACP transport requires agent-client-protocol"
   - Suggestion: Run `pip install agent-client-protocol`

4. **Wrapper Not Found**
   - Falls back to direct `codex-acp` if wrapper unavailable
   - Logged: "Using ACP agent command instead of wrapper"

## Troubleshooting Checklist

- [ ] Verify wrapper path: `ls -l ~/.repos/acp-wrapper/run-acp-agent`
- [ ] Check wrapper is executable: `chmod +x ~/.repos/acp-wrapper/run-acp-agent`
- [ ] Check venv: `~/.repos/acp-wrapper/.venv/bin/python -m pip list | grep agent-client`
- [ ] Check codex-acp on PATH: `which codex-acp`
- [ ] Enable debug logging to see detailed flow
- [ ] Check Talon logs for error context: `~/.talon/logs/`

## Important Concepts

### Wrapper Pattern
The integration uses a wrapper script instead of directly importing `agent-client-protocol`. This keeps Talon's shared Python interpreter isolated from the ACP SDK's strict version requirements for `pydantic` and `typing_extensions`.

### Singleton Transport
A single `ACPTransport` instance is reused across requests to maintain agent session state. The transport is reset on errors and reconnects automatically on next use.

### Threading Model
The transport runs an independent asyncio event loop in a daemon thread to bridge Talon's synchronous calls with the ACP SDK's async interface.

### Settings Hierarchy
1. User explicit override: `user.model_acp_agent_command` (if not default)
2. Wrapper if available: `ACP_WRAPPER_COMMAND` env var or `~/.repos/acp-wrapper/run-acp-agent`
3. Default: `"codex-acp"` binary lookup on PATH

## Known Limitations

- [ ] No request timeout mechanism (can hang indefinitely)
- [ ] Single session reused (no multiple concurrent sessions)
- [ ] No wrapper hot-reload (requires Talon restart if wrapper changes)
- [ ] No built-in MCP server support (beyond basic ACP transport)
- [ ] Terminal/file access capabilities not implemented

## Performance Notes

- **Startup**: Wrapper/codex-acp startup delay on first request (~1-2 seconds)
- **Subsequent Requests**: Reuse cached transport (near-instant routing)
- **Memory**: Single transport object + subprocess in memory
- **Cleanup**: Daemon thread and subprocess cleaned up on Talon exit

## Next Steps for Integration Team

1. **Documentation** - Create comprehensive user guide
2. **Testing** - Implement full test suite for ACP integration
3. **Diagnostics** - Add health check and diagnostic commands
4. **Enhancement** - Consider timeout, multiple sessions, performance improvements

See [Integration Plan](talon-ai-tools-acp-wrapper-integration.md) for detailed work items.

## Support & Debugging

**For User Issues**:
- Check troubleshooting checklist above
- Review Talon logs: `~/.talon/logs/`
- Enable debug logging in modelHelpers.py

**For Developer Questions**:
- See [Technical Implementation Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md)
- Review [ACP Wrapper README](../../repos/acp-wrapper/README.md)
- Check [Codex ACP Repo](https://github.com/cola-io/codex-acp)

**Version Info to Provide**:
- Talon version: `talon --version`
- Wrapper version: Head commit in `/home/carl/repos/acp-wrapper`
- codex-acp version: `codex-acp --version`
- Python version in wrapper: `~/.repos/acp-wrapper/.venv/bin/python --version`
