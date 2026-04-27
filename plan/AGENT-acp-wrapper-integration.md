# Agent: ACP Wrapper Integration for Talon-AI-Tools

**Objective**: Complete the integration of the ACP wrapper (`/home/carl/repos/acp-wrapper`) with `talon-ai-tools` to enable Codex ACP as a reliable LLM query method.

**Status**: ✅ INTEGRATION EXISTS, ⚠️ TESTING & DOCUMENTATION NEEDED

## Summary
The architectural integration between `talon-ai-tools` and the ACP wrapper is **already implemented**. The transport layer, settings, and routing logic are in place. This agent tracks completing the remaining documentation, testing, verification, and enhancement work.

## Key Files Involved
- `/home/carl/.talon/user/talon-ai-tools/lib/acp_client.py` - ACP transport implementation
- `/home/carl/.talon/user/talon-ai-tools/lib/modelHelpers.py` - Model routing and ACP integration
- `/home/carl/.talon/user/talon-ai-tools/lib/talonSettings.py` - Settings definitions
- `/home/carl/.talon/user/talon-ai-tools/readme.md` - User documentation
- `/home/carl/repos/acp-wrapper/` - Wrapper project (reference)

## Work Breakdown

### Phase 1: Documentation (Immediate)
**Priority**: HIGH - Enables users to set up and troubleshoot

- [ ] **Create Integration Guide** (`docs/ACP_WRAPPER_INTEGRATION.md`)
  - Installation and setup steps
  - Configuration examples (default, custom agent, disabled wrapper)
  - Troubleshooting common issues
  - Expected file locations and permissions
  - Estimated effort: 2-3 hours

- [ ] **Enhance README**
  - Add comprehensive ACP section beyond current basic info
  - Link to integration guide
  - Add examples of common configurations
  - Estimated effort: 1 hour

### Phase 2: Testing (High Priority)
**Priority**: HIGH - Ensures reliability and helps users debug

- [ ] **Add Unit Tests** (`tests/test_acp_integration.py`)
  - Test wrapper detection logic (`_find_acp_wrapper_command`)
  - Test settings resolution (`_resolve_acp_agent_settings`)
  - Test block building (`_build_acp_blocks`)
  - Test context formatting (`_format_acp_context`)
  - Estimated effort: 3-4 hours

- [ ] **Add Integration Tests**
  - Mock ACP responses and verify routing
  - Test error handling and recovery
  - Test with dummy agent (like in acp-wrapper tests)
  - Estimated effort: 2-3 hours

- [ ] **End-to-End Testing**
  - Document manual testing procedures
  - Create test checklist for functional verification
  - Estimated effort: 1-2 hours

### Phase 3: Diagnostics & Error Handling (Medium Priority)
**Priority**: MEDIUM - Improves user experience during troubleshooting

- [ ] **Verify Current Diagnostics**
  - Test missing wrapper binary scenario → verify helpful error
  - Test missing SDK scenario → verify helpful error
  - Test agent crash → verify recovery works
  - Estimated effort: 2 hours

- [ ] **Enhance Error Messages**
  - Add specific guidance for each error type
  - Include suggested fixes or commands
  - Estimated effort: 1-2 hours

- [ ] **Add Diagnostic Command** (Talon action)
  - Show current ACP configuration
  - Check wrapper availability
  - Check SDK installation
  - Estimated effort: 2-3 hours

### Phase 4: Code Review & Quality (Medium Priority)
**Priority**: MEDIUM - Ensures code quality and maintainability

- [ ] **Code Review**
  - Review threading model in `ACPTransport`
  - Review async/sync bridge
  - Check type hints completeness
  - Review error handling paths
  - Estimated effort: 2 hours

- [ ] **Documentation Enhancements**
  - Add comprehensive docstrings
  - Document threading model
  - Document async/sync interaction
  - Estimated effort: 1-2 hours

- [ ] **Static Analysis**
  - Run mypy type checking (if available)
  - Check for unused imports
  - Check for dead code
  - Estimated effort: 1 hour

### Phase 5: Feature Verification (Low Priority, Validation Only)
**Priority**: LOW - Confirms existing features work as expected

- [ ] **Verify Feature Completeness**
  - Wrapper detection and selection
  - Direct command override
  - Environment variables support
  - Working directory support
  - Arguments forwarding
  - Transport connection pooling
  - Error recovery
  - Estimated effort: 1-2 hours

## Dependencies & Prerequisites
- ACP wrapper repo fully implemented at `/home/carl/repos/acp-wrapper`
- Talon voice system functional
- Python testing framework (pytest recommended)
- Access to codex-acp binary

## Success Criteria
1. ✅ All integration code present and functional
2. ⚠️ Comprehensive test coverage (>80% for acp_client.py)
3. ⚠️ Clear user documentation for setup and troubleshooting
4. ⚠️ Helpful error messages for all failure scenarios
5. ⚠️ Verified end-to-end functionality with real wrapper
6. ⚠️ Code quality review completed

## Risk Assessment
**Low Risk**: The integration is relatively straightforward (subprocess management + async/sync bridge)
- Main risks: threading issues, subprocess stdio handling, dependency import failures
- Mitigated by: test coverage, error recovery pattern, detailed logging

## Timeline Estimate
- **Phase 1 (Documentation)**: 3-4 hours
- **Phase 2 (Testing)**: 6-8 hours
- **Phase 3 (Diagnostics)**: 3-5 hours
- **Phase 4 (Code Review)**: 4-5 hours
- **Phase 5 (Verification)**: 1-2 hours

**Total Estimate**: 17-24 hours

## Next Steps
1. Create integration guide and documentation
2. Implement comprehensive test suite
3. Verify error handling paths
4. Perform code review and refactoring if needed
5. Create diagnostic tools for troubleshooting
6. Run manual end-to-end validation

## Notes
- The wrapper pattern is the chosen solution over vendoring SDK code
- This design keeps Talon's shared interpreter isolated from ACP dependencies
- The integration is transparent to users via standard Talon settings
- Thread safety is managed through the event loop pattern
