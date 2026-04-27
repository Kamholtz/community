# ACP Wrapper Integration Documentation - Map & Summary

## Overview
This directory now contains comprehensive documentation for integrating the ACP wrapper (`/home/carl/repos/acp-wrapper`) with `talon-ai-tools` to query LLMs via the Agent Client Protocol.

**Status**: ✅ Integration complete in code | ⚠️ Testing & user documentation in progress

## Document Map

### 1. Quick Reference (START HERE)
📄 **[ACP_WRAPPER_QUICK_REFERENCE.md](ACP_WRAPPER_QUICK_REFERENCE.md)**
- **Best for**: Users and developers getting oriented
- **Contents**:
  - What is this? (executive summary)
  - Current status at a glance
  - Quick links and quick start guide
  - Configuration examples
  - Troubleshooting checklist
  - Key concepts and limitations
- **Read time**: 10-15 minutes
- **Purpose**: One-stop reference for most common questions

### 2. Integration Planning
📄 **[talon-ai-tools-acp-wrapper-integration.md](talon-ai-tools-acp-wrapper-integration.md)**
- **Best for**: Project managers, integration leads, planning
- **Contents**:
  - Architecture overview with flow diagram
  - Detailed work breakdown by phase
  - Dependencies and prerequisites
  - Success criteria and verification checklist
  - Timeline estimates (total: 17-24 hours)
  - Risk assessment
- **Read time**: 20-30 minutes
- **Purpose**: Reference for planning, tracking, and understanding scope

### 3. Agent Work Tracking
📄 **[AGENT-acp-wrapper-integration.md](AGENT-acp-wrapper-integration.md)**
- **Best for**: Developers with assigned work, tracking progress
- **Contents**:
  - Current status and summary
  - Breakdown into 5 phases with effort estimates
  - Dependencies and success criteria
  - Next steps and notes
  - Key files involved
- **Read time**: 15-20 minutes
- **Purpose**: Actionable work tracking with clear next steps

### 4. Technical Deep-Dive
📄 **[ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md)**
- **Best for**: Developers implementing/modifying integration
- **Contents**:
  - Complete architecture diagram with all components
  - Implementation walkthrough with code snippets
  - Key design decisions and rationale
  - Testing considerations and scope
  - Common issues and solutions
  - Related standards and specifications
- **Read time**: 40-60 minutes
- **Purpose**: Complete technical understanding for implementation

### 5. Original Integration Plan
📄 **[talon-ai-tools-acp-plan.md](talon-ai-tools-acp-plan.md)** (EXISTING)
- **Best for**: Historical reference, context on design decisions
- **Contents**:
  - Original plan for integrating wrapper with talon-ai-tools
  - Two options: external wrapper vs vendored code
  - Work breakdown for both approaches
- **Read time**: 20 minutes
- **Purpose**: Context and historical record

### 6. Wrapper Project Plan
📄 **[acp-wrapper-venv-plan.md](acp-wrapper-venv-plan.md)** (EXISTING)
- **Best for**: Understanding why wrapper approach was chosen
- **Contents**:
  - Context around dependency isolation
  - Wrapper architecture goals
  - Step-by-step implementation plan
  - Completed checkmarks for what's done
- **Read time**: 20 minutes
- **Purpose**: Understand wrapper project itself

### 7. Design Alternatives
📄 **[acp-alternatives-plan.md](acp-alternatives-plan.md)** (EXISTING)
- **Best for**: Understanding trade-offs between approaches
- **Contents**:
  - Option A: External virtualenv (CHOSEN)
  - Option B: Vendored ACP helper
  - Comparison of effort and trade-offs
- **Read time**: 15 minutes
- **Purpose**: Justify design choices

## Reading Paths

### Path 1: "I want to use ACP with Talon"
1. Start: [Quick Reference](ACP_WRAPPER_QUICK_REFERENCE.md#getting-started) (5 min)
2. Read: [Getting Started](ACP_WRAPPER_QUICK_REFERENCE.md#getting-started) section (5 min)
3. Reference: Keep [Configuration Examples](ACP_WRAPPER_QUICK_REFERENCE.md#configuration-examples) handy

**Total**: 10 minutes to get started

### Path 2: "I'm managing this integration project"
1. Start: [Quick Reference](ACP_WRAPPER_QUICK_REFERENCE.md) (10 min)
2. Read: [Integration Planning](talon-ai-tools-acp-wrapper-integration.md) (20 min)
3. Review: [Agent Tracking](AGENT-acp-wrapper-integration.md) for current progress (10 min)

**Total**: 40 minutes to understand full scope and status

### Path 3: "I'm implementing/testing this integration"
1. Start: [Quick Reference](ACP_WRAPPER_QUICK_REFERENCE.md) (10 min)
2. Deep-dive: [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md) (45 min)
3. Reference: [Integration Planning](talon-ai-tools-acp-wrapper-integration.md#work-items) for test scope (15 min)
4. Implement: Use [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md#testing-considerations) for test design

**Total**: 70 minutes to understand implementation

### Path 4: "I need to understand why this design was chosen"
1. Start: [Alternatives Plan](acp-alternatives-plan.md) (15 min)
2. Read: [Wrapper Plan](acp-wrapper-venv-plan.md) (20 min)
3. Review: [Technical Rationale](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md#key-design-decisions) (10 min)

**Total**: 45 minutes for complete design justification

## Key Files in Codebase

### Source Files
```
~/.talon/user/talon-ai-tools/
├── lib/
│   ├── acp_client.py         ← ACPTransport & _TalonACPClient (239 lines)
│   ├── modelHelpers.py       ← send_request_to_acp() & utils (555 lines)
│   └── talonSettings.py      ← Settings definitions incl. ACP options
├── .test/
│   ├── unit_test.py          ← Current tests (minimal)
│   └── test_acp_integration.py ← TO BE CREATED
└── readme.md                 ← User docs (already mentions wrapper)
```

### Wrapper Project (Reference)
```
~/repos/acp-wrapper/
├── acp_wrapper/
│   ├── cli.py                ← Python launcher
│   └── launcher.py           ← Helper functions
├── run-acp-agent             ← Bash wrapper script
├── tests/                    ← Wrapper tests (reference for ACP tests)
├── requirements.txt          ← ACP SDK dependencies
└── README.md                 ← Wrapper setup docs
```

## Command Reference

### Check Current Configuration
```bash
# See if wrapper is available
ls -la ~/.repos/acp-wrapper/run-acp-agent

# Check wrapper's venv
~/.repos/acp-wrapper/.venv/bin/python -m pip list

# Check codex-acp
which codex-acp
codex-acp --version
```

### Test the Setup
```bash
# Current (minimal) tests
cd ~/.talon/user/talon-ai-tools
python -m pytest .test/unit_test.py -v

# When integration tests added
python -m pytest .test/test_acp_integration.py -v
```

### Debug Issues
```bash
# View Talon logs
tail -f ~/.talon/logs/*.log

# Check wrapper execution directly
~/.repos/acp-wrapper/run-acp-agent --help

# Test codex-acp directly
echo '{"jsonrpc":"2.0","id":1,"method":"session/new","params":{"cwd":".","mcpServers":[]}}' | \
  codex-acp
```

## Current Implementation Status

### What's Already Done ✅
- **Architecture**: Complete transport layer, routing, settings
- **Wrapper Detection**: Finds wrapper via env var or default path
- **Settings**: All configuration options defined and working
- **Routing**: `send_request()` properly routes to ACP endpoint
- **Transport**: `ACPTransport` manages subprocess and async/sync bridge
- **Response Capture**: `_TalonACPClient` captures agent responses

### What's In Progress ⚠️
- **Testing**: Need comprehensive test suite (estimated 6-8 hours)
- **Documentation**: User guide needed (estimated 3-4 hours)
- **Diagnostics**: Error scenarios need verification (estimated 2-3 hours)
- **Code Review**: Architecture review pending (estimated 2-3 hours)

### What's Not Yet Started 🔲
- **End-to-End Tests**: Real wrapper + codex-acp interaction tests
- **Health Check**: Diagnostic command for ACP status
- **Performance Monitoring**: Metrics collection (future enhancement)
- **Advanced Features**: Multiple sessions, custom MCP servers (future)

## Key Integration Points

### 1. Settings Flow
```
user.talon settings → talonSettings.py definitions
  → modelHelpers.py resolution
  → ACPTransport initialization
```

### 2. Request Flow
```
Talon voice command
  → modelHelpers.send_request()
  → modelHelpers.send_request_to_acp()
  → modelHelpers._get_acp_transport()
  → acp_client.ACPTransport.send_prompt()
  → wrapper script → codex-acp → LLM
  → Response captured → returned to Talon destination
```

### 3. Error Flow
```
Exception in any step
  → modelHelpers._reset_acp_transport()
  → modelHelpers._notify_acp_failure()
  → Error context logged to Talon log
  → Next request triggers reconnection attempt
```

## Testing Strategy

### Unit Tests (to create)
- Command resolution logic
- Settings parsing
- Block building
- Error path handling

### Integration Tests (to create)
- Mock agent responses
- Transport initialization
- Request/response proxying
- Model override behavior

### End-to-End Tests (manual for now)
- Real wrapper execution
- Real codex-acp interaction
- Full Talon voice command → result flow
- Performance and resource usage

## Work Prioritization

**Phase 1 - Critical (Do First)**:
- ✅ Architecture & integration (DONE)
- 🔲 Comprehensive unit tests
- 🔲 User documentation

**Phase 2 - Important (Do Second)**:
- 🔲 Integration tests with mocks
- 🔲 Error handling verification
- 🔲 Code review & cleanup

**Phase 3 - Nice-to-Have (Do Later)**:
- 🔲 Diagnostic tools
- 🔲 Performance monitoring
- 🔲 Advanced features

## Success Metrics

- [ ] All settings appear and work in Talon
- [ ] Voice commands route through ACP successfully
- [ ] Responses appear in selected destination (paste/snippet)
- [ ] Error messages are helpful and actionable
- [ ] Test coverage > 80% for acp_client.py
- [ ] Documentation covers setup and troubleshooting
- [ ] End-to-end flow verified with real wrapper

## Quick Links to Implementation

| Component | File                              | Lines   | Status      |
| --------- | --------------------------------- | ------- | ----------- |
| Transport | `acp_client.py`                   | 1-239   | ✅ Complete  |
| Routing   | `modelHelpers.py`                 | 450-555 | ✅ Complete  |
| Settings  | `talonSettings.py`                | 70-125  | ✅ Complete  |
| Tests     | `.test/test_acp_integration.py`   | N/A     | 🔲 To Create |
| Docs      | `docs/ACP_WRAPPER_INTEGRATION.md` | N/A     | 🔲 To Create |

## Next Immediate Steps

For developers assigned to this work:
1. Review [Quick Reference](ACP_WRAPPER_QUICK_REFERENCE.md)
2. Review [Agent Tracking](AGENT-acp-wrapper-integration.md)
3. Check your assigned phase in [Integration Planning](talon-ai-tools-acp-wrapper-integration.md#work-items)
4. Refer to [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md) as needed

## Questions & Support

**For Setup Questions**: See [Configuration Examples](ACP_WRAPPER_QUICK_REFERENCE.md#configuration-examples)

**For Technical Questions**: See [Technical Details](ACP_WRAPPER_IMPLEMENTATION_TECHNICAL.md)

**For Project Planning**: See [Integration Planning](talon-ai-tools-acp-wrapper-integration.md)

**For Detailed Work Items**: See [Agent Tracking](AGENT-acp-wrapper-integration.md)

---

**Created**: February 16, 2026
**Status**: Integration framework complete, testing and documentation in progress
**Maintained by**: ACP Wrapper Integration Team
