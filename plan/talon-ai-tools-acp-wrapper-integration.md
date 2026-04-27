# Talon-AI-Tools ACP Wrapper Integration Plan

## Overview
This plan documents the work to fully integrate the ACP wrapper (from `/home/carl/repos/acp-wrapper`) into `talon-ai-tools` for using Codex ACP as an LLM query method.

## Current Status
Much of the integration is already in place:
- ✅ `acp_client.py` implemented with `ACPTransport` class for managing ACP connections
- ✅ `modelHelpers.py` has `_resolve_acp_agent_settings()` and wrapper detection logic
- ✅ Settings defined in `talonSettings.py` for ACP configuration
- ✅ Documentation in `readme.md` showing ACP setup with wrapper support
- ⚠️ Minimal test coverage exists; tests need expansion
- ⚠️ Diagnostics need verification for error cases
- ⚠️ End-to-end integration testing needs implementation

## Architecture Overview

### Key Components

**1. ACP Transport Layer** (`lib/acp_client.py`)
- `ACPTransport`: Manages persistent ACP agent connection
- `_TalonACPClient`: Client implementation that captures agent responses
- Threading-based event loop for async/sync compatibility with Talon

**2. Model Helpers** (`lib/modelHelpers.py`)
- `send_request_to_acp()`: Routes prompts to ACP agent
- `_get_acp_transport()`: Singleton transport factory with lazy initialization
- `_resolve_acp_agent_settings()`: Resolves wrapper vs direct command
- `_find_acp_wrapper_command()`: Locates wrapper at default or env-specified path

**3. Talon Settings** (`lib/talonSettings.py`)
- `user.model_acp_use_wrapper` (bool, default=True): Enable wrapper preference
- `user.model_acp_agent_command` (str): Direct agent command override
- `user.model_acp_agent_args` (str): Additional arguments for agent
- `user.model_acp_agent_cwd` (str): Working directory for agent
- `user.model_acp_agent_env` (str): Extra environment variables

### Flow Diagram
```
Talon voice command
    ↓
send_request() in modelHelpers.py checks user.model_endpoint
    ↓ (if "acp")
send_request_to_acp()
    ↓
_get_acp_transport() → _resolve_acp_agent_settings()
    ↓
Prefers ACP wrapper if:
  1. user.model_acp_use_wrapper = True (default)
  2. ACP_WRAPPER_COMMAND env var OR ~/.repos/acp-wrapper/run-acp-agent exists
    ↓
ACPTransport spawns wrapper/codex-acp
    ↓
Wrapper activates .venv and runs codex-acp with proper environment
    ↓
Response captured by _TalonACPClient → formatted and returned
```

## Work Items

### 1. Documentation & User Guide
**Status**: Partially Complete

**Tasks**:
- [ ] Create comprehensive integration guide: `docs/ACP_WRAPPER_INTEGRATION.md`
  - How to install and configure acp-wrapper
  - How to verify the wrapper is working
  - Troubleshooting common issues
  - Examples of custom configuration
- [ ] Update top-level README with ACP wrapper section
- [ ] Add configuration examples for common scenarios:
  - Using wrapper with default paths
  - Using wrapper with custom ACP agent
  - Disabling wrapper to use raw codex-acp

**Files to Update**:
- `readme.md` (already has basic info, enhance with examples)
- Create new: `docs/ACP_WRAPPER_INTEGRATION.md`

### 2. Testing & Verification
**Status**: Needs Work

**Current Tests**: Only `strip_markdown()` is tested in `.test/unit_test.py`

**Tests To Add**:

a. Unit Tests (`.test/test_acp_integration.py`):
   - [ ] Test `_find_acp_wrapper_command()`:
     - Returns None when wrapper not found
     - Returns env var override when set
     - Returns default path when exists
   - [ ] Test `_resolve_acp_agent_settings()`:
     - Wrapper selected when available and enabled
     - Direct command used when user specified
     - Codex-acp default when neither available
     - Args/env/cwd properly forwarded
   - [ ] Test `_format_acp_context()` generates correct context strings
   - [ ] Test `_build_acp_blocks()` correctly builds ACP message blocks

b. Integration Tests:
   - [ ] Create dummy ACP agent (similar to acp-wrapper test) to mock responses
   - [ ] Test `send_request_to_acp()` with mocked transport
   - [ ] Test error handling and `_notify_acp_failure()` paths
   - [ ] Test wrapper command execution and fallback to direct codex-acp
   - [ ] Verify content types handled: text, images, resources

c. End-to-End Tests:
   - [ ] Launch actual wrapper and verify JSON-RPC framing
   - [ ] Test with real codex-acp if available
   - [ ] Verify Talon voice command routing through ACP

**Implementation Notes**:
- Use pytest framework (already in place in acp-wrapper project)
- Mock subprocess and asyncio where appropriate
- Document expected environment for running tests

### 3. Diagnostics & Error Handling
**Status**: Partially Complete

**Current Implementation**:
- `_acp_command_context` tracks command details for error messages
- `_notify_acp_failure()` shows context in notification
- `_reset_acp_transport()` allows recovery after failure
- Exception logging to Talon log via `LOGGER.exception()`

**Verification Needed**:
- [ ] Test missing wrapper binary scenario
- [ ] Test missing agent-client-protocol SDK
- [ ] Test invalid JSON-RPC responses
- [ ] Test subprocess crashes and recovery
- [ ] Test timeout/hanging scenarios
- [ ] Verify error context appears in Talon logs and notifications

**Enhancements**:
- [ ] Add diagnostic command to show current configuration
- [ ] Add health check endpoint (if wrapper supports it)
- [ ] Better error messages for common issues:
  - "wrapper not found" → suggest installation path
  - "SDK missing" → suggest pip install command
  - "agent crash" → suggest checking codex-acp logs

### 4. Code Quality & Maintenance
**Status**: Ready for Review

**Tasks**:
- [ ] Code review of acp_client.py for threading safety
- [ ] Code review of modelHelpers.py ACP-related functions
- [ ] Verify type hints are complete and accurate
- [ ] Check docstrings are comprehensive
- [ ] Run static analysis (mypy, pylint) if available
- [ ] Ensure no unused imports or dead code

**Files to Review**:
- `lib/acp_client.py`
- `lib/modelHelpers.py` (ACP-related functions)
- `lib/talonSettings.py` (ACP settings definitions)

### 5. Feature Completeness
**Status**: Mostly Complete

**Implemented Features**:
- ✅ Wrapper detection and optional usage
- ✅ Direct command fallback
- ✅ Environment variable overrides
- ✅ Working directory support
- ✅ Additional arguments forwarding
- ✅ Transport connection pooling (singleton pattern)
- ✅ Error recovery with transport reset

**Potential Enhancements** (Out of current scope):
- [ ] Multiple simultaneous ACP sessions (currently singleton)
- [ ] Wrapper hot-reload capability
- [ ] ACP server mode (keep alive between requests)
- [ ] Performance metrics/monitoring
- [ ] Custom MCP server support injection

### 6. Integration with Existing Query Methods
**Status**: Complete

**Already Implemented**:
- ✅ Selectable via `user.model_endpoint = "acp"`
- ✅ Works alongside HTTP, llm CLI, and Copilot options
- ✅ Same prompt/response interface as other methods
- ✅ System message and context passing
- ✅ Image support (converted to descriptions)
- ✅ Model selection and override


## Verification Checklist

### Setup Verification
- [ ] Wrapper repo at `/home/carl/repos/acp-wrapper` is accessible
- [ ] Wrapper venv has required packages: `agent-client-protocol`, `pydantic`
- [ ] `run-acp-agent` script is executable
- [ ] `codex-acp` binary is available on PATH

### Functional Verification
- [ ] Settings appear in Talon settings viewer
- [ ] `user.model_endpoint = "acp"` selects ACP transport
- [ ] Voice command routes through ACP when endpoint is set
- [ ] Response appears in destination (paste, snippet, etc.)
- [ ] Model override works
- [ ] System prompt is passed correctly

### Error Handling Verification
- [ ] Missing wrapper shows helpful error message
- [ ] Missing SDK shows helpful error message
- [ ] Agent crash triggers recovery attempt
- [ ] Error context logged for debugging

### Performance Verification
- [ ] Wrapper startup time is acceptable
- [ ] Response latency is reasonable
- [ ] No memory leaks on repeated use
- [ ] Proper cleanup on Talon shutdown

## Dependencies

### Python Packages (in acp-wrapper)
- `agent-client-protocol >= 0.7.1`
- `pydantic >= 2.12`

### External Binaries
- `codex-acp` (from cola-io or custom ACP agent)

### Talon Integration
- Must work with Talon's asyncio event loop model
- Compatible with Talon's subprocess handling

## Related Documents
- [ACP Wrapper Virtualenv Plan](/plan/acp-wrapper-venv-plan.md)
- [ACP Integration Alternatives](/plan/acp-alternatives-plan.md)
- [ACP Wrapper README](../../../repos/acp-wrapper/README.md)
- [Talon-AI-Tools README](../readme.md)

## Timeline & Priority

### Phase 1: Documentation & Testing (High Priority)
- Write integration guide
- Add comprehensive unit tests
- Verify diagnostics work

### Phase 2: Error Handling Enhancement (Medium Priority)
- Improve error messages
- Add recovery scenarios
- Health check support

### Phase 3: Feature Additions (Low Priority)
- Multiple sessions support
- Performance monitoring
- Custom MCP server injection

## Notes
- The wrapper pattern allows independent SDK version management outside Talon's shared interpreter
- This design maintains compatibility with existing HTTP and LLM CLI query methods
- Threading model is carefully managed to work with Talon's asyncio integration
- All wrapper integration is transparent to users via standard Talon settings
