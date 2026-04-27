# ACP integration alternatives

## Goal
Estimate the complexity of two approaches that avoid pinning `agent-client-protocol` into Talon’s shared interpreter:
1. Spawn the agent from a separate virtualenv.
2. Vendor the minimal ACP helper code inside `talon-ai-tools`.

## Shared checkpoints
1. **Current ACP flow**: confirm how `ACPTransport` currently imports `acp`, which files/classes it needs, and where typing-related dependencies propagate (e.g., `typing_extensions` via `pydantic`/`torch`/`typing-inspection`).
2. **Talon environment constraints**: document how the shared `/home/carl/talon/resources/python/...` site-packages get prepended to the `.venv`, so we know why pip can’t upgrade `typing_extensions` there without breaking other packages.
3. **Startup constraints**: determine what Talon expects when the ACP transport spawns `codex-acp` (stdin/stdout pipes, environment variables, logging, expected responses) so we can preserve those when wrapping another process.

## Option A: External virtualenv
1. **Agent command**: verify how to point `user.model_acp_agent_command` at a wrapper script that activates the new venv and launches `codex-acp`; note whether extra args are needed (workspace path, env).
2. **Dependency install**: estimate steps to create the venv, install `agent-client-protocol`/`codex-acp`, and keep it in sync with Talon updates.
3. **Testing**: list checks to ensure Talon can still open a session and receive `AgentMessageChunk` content through the new subprocess path, including error handling/logging when the helper fails.

## Option B: Vendored ACP helper
1. **Minimal API surface**: catalogue which classes/functions `ACPTransport` actually uses (e.g., `connect_to_agent`, `ClientSideConnection`, `text_block`, `session_update` callbacks, JSON-RPC framing) so we know how much of the SDK must be reimplemented.
2. **Dependency verification**: identify the typing-related requirements of the vendored code (likely only `typing_extensions` and `pydantic`, but confirm) and determine whether we can pin them to Talon’s existing version or bundle the helpers with their own vendored typings.
3. **Maintenance cost**: note how often the vendored code must be updated when the ACP spec advances and what tests/doc updates are needed to make sure it still talks to `codex-acp`.

## Verification list
- ensure whichever approach we choose still exposes diagnostics when the agent binary or SDK is missing
- confirm `user.model_endpoint` and new settings still control the transport and don’t regress other `model_helpers` paths
- run Talon unit/functional checks (e.g., `gpt_apply_prompt`) against both HTTP and ACP settings to prove fallback stability

No questions at this point.

## Status
- [x] Shared checkpoints inspected (ACP import, site-packages layering, expected agent startup contract).
- [x] Option A researched (agent command settings, venv install steps, testing expectations).
- [x] Option B researched (required ACP API surface, typing dependencies, maintenance/test burden).
- [x] Recommendation pending in final summary.
