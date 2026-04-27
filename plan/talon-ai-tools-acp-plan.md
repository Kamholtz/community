# Talon-ai-tools ACP transport plan

## Goal
Outline the talon-ai-tools work that must land after choosing between the wrapper-based virtualenv or vendored SDK route so the ACP transport keeps working while Talon's shared interpreter stays untouched.

## Context
- `talon-ai-tools/lib/acp_client.py` currently defines `ACPTransport`, `ACPClientSession`, and the helpers that import `agent-client-protocol`/`acp`. This module drives Talon's stdin/stdout JSON-RPC stream to `codex-acp`.
- `talon-ai-tools/lib/modelHelpers.py` exposes the Talon settings (`user.model_endpoint`, `user.model_acp_agent_command`, `user.model_acp_agent_*`) that control which transport to start and how to launch the agent.
- Any change must keep the HTTP path (`model_helpers.get_model_helper`) stable and continue surfacing diagnostics (missing binary, SDK import errors, failing subprocess) so `ACPFailure` logging still works.
- The wrapper repo described in `plan/acp-wrapper-venv-plan.md` shows how to wrap `codex-acp` with a dedicated venv. Option B contemplates replicating a minimal subset of `agent-client-protocol` inside talon-ai-tools to avoid the dependency altogether.

## Option A — external virtualenv wrapper
1. **Audit the existing transport.** Read `talon-ai-tools/lib/acp_client.py` to enumerate every `acp` import/typing usage, confirm `ACPTransport` drives the subprocess via `asyncio.create_subprocess_exec`, and verify the stdin/stdout framing only depends on `agent-client-protocol` helpers (e.g., `AgentMessageChunk`, `text_block`, framing helpers). Note where `ACPClientSession` and `ACPTransport` currently raise `ACPFailure` so we can keep those paths intact when the wrapper is inserted.
2. **Wire the wrapper command through `modelHelpers`.** Update `talon-ai-tools/lib/modelHelpers.py` so it defaults `user.model_acp_agent_command` to the wrapper (maintaining overrides from `user.model_acp_agent_args/env/cwd`) while leaving `user.model_endpoint` as the HTTP/ACP toggle that the rest of the helpers rely on. Ensure the helper surfaces diagnostic metadata (command line, cwd, environment) to `ACPFailure` when the wrapper fails to start or returns a non-zero exit code, and add developer-friendly log messages that explain the wrapper/vendored venv context.
3. **Guard diagnostics and feature parity.** Keep the existing `ACPFailure` paths for missing binaries or SDK import errors but update the wording to mention the wrapper’s path and dedicated venv so the failures continue to reach Talon’s log stream. Confirm that any logic that inspects the agent command or `ACPClientSession` session updates still works once Talon talks to the wrapper.
4. **Integration and regression tests.** Add end-to-end tests (likely under `talon-ai-tools/tests/` or the repo's existing test suite) that start `ACPTransport` with `user.model_acp_agent_command` pointed at the wrapper, assert `send_request_to_acp` still receives `AgentMessageChunk` responses, and cover failure scenarios such as the wrapper’s subprocess failing to launch. Include tests for the diagnostic logging so we can detect when the wrapper misconfigures its venv.

## Option B — vendoring minimal helper code
1. **Catalog the required API surface.** Enumerate the exact functions, classes, and protocols `ACPTransport` pulls from `agent-client-protocol` (e.g., `connect_to_agent`, `ClientSideConnection`, message framing helpers, `AgentMessageChunk`, `session_update` callbacks) and capture any dependencies on `typing_extensions`/`pydantic` models or helpers so we know what to reimplement or adapt.
2. **Vendor a lightweight implementation inside `talon-ai-tools`.** Introduce a small helper module (or extend `talon-ai-tools/lib/acp_client.py`) that reproduces the necessary framing, connection, and message types while depending only on the Python standard library and Talon’s pinned typing helpers. Keep the exported API identical to what `ACPTransport` currently expects so it can be swapped in without touching the rest of the app.
3. **Preserve transport features and handshake behavior.** Mirror every `ACPTransport` expectation (session updates, `text_block` events, JSON-RPC framing, handshake names) so the vendored implementation continues to talk to `codex-acp` exactly as before. Add comments or docstrings that specify which upstream spec constants would need updates if `agent-client-protocol` changes.
4. **Maintenance and testing.** Add targeted tests that mock `codex-acp` (or reuse the dummy agent used in the wrapper plan) to validate the vendored helpers exercise the same response types, error handling, and diagnostics as the real SDK. Document an upstream-sync workflow (e.g., rerun import diffs, rerun `python -m pytest`) so future updates to `agent-client-protocol` can be reflected here without accidental drift.

## Documentation updates
- Keep `plan/acp-wrapper-venv-plan.md` and `plan/acp-alternatives-plan.md` synchronized with whichever option is chosen, ensuring each references the talon-ai-tools steps described here.
- Add a short section to the high-level documentation (e.g., `README.md` or a developer note) explaining how to configure `user.model_acp_agent_command`/`user.model_acp_agent_*` when using the wrapper, and document how diagnostics from the wrapper propagate into `ACPFailure`.
- If Option B is picked, add a note to `plan/talon-ai-tools-acp-plan.md` (or a dedicated developer doc) describing how to spot and update the vendored helpers when `agent-client-protocol` releases break compatibility.

## Verification list
- Continue surfacing diagnostics when the agent binary/SDK is missing, regardless of whether the wrapper or vendor approach is used.
- Confirm `user.model_endpoint`, `user.model_acp_agent_command`, and the transport selection code still respect Talon's model helper paths, including any fallback to HTTP helpers when ACP is disabled.
- Run Talon regression checks (e.g., `gpt_apply_prompt` for both HTTP and ACP endpoints) and repeat the agent startup tests to prove signal arrives through the new process path.

## Status
- [ ] Work plan drafted; waiting on repo-specific details before implementing.
