# ACP wrapper virtualenv plan

## Context
- The existing ACP transport lives inside `talon-ai-tools` and imports `agent-client-protocol` from the shared Talon `.venv`, which is forced to prepend `/home/carl/talon/resources/python/...` and cannot upgrade `typing_extensions`/`pydantic` without affecting core Talon.
- Instead of pinning the SDK inside that interpreter, we will build a dedicated Python project outside the Talon directory that owns its own virtual environment (`agent-client-protocol`, `codex-acp`, and any helper glue). Talon will treat that project as if it were the agent binary by pointing `user.model_acp_agent_command` at a wrapper script inside it.

## Goals
1. Create a standalone project (e.g., `/home/carl/repos/acp-wrapper`) whose `venv` is outside Talon.
2. Provide a small wrapper/adapter inside that project that activates the `venv`, ensures the SDK dependencies are installed, and then spawns `codex-acp` (or another ACP agent) while preserving stdin/stdout pipes, logging, and expected JSON-RPC framing.
3. Define how Talon should launch the wrapper process and how we can verify the end-to-end flow with automated tests.

## Steps

### 1. Project/venv layout
1. Create a new directory such as `/home/carl/repos/acp-wrapper`.
2. Inside that repo, add a `pyproject.toml` specifying `agent-client-protocol>=0.7.1`, `pydantic>=2.12`, and any tooling (e.g., `pytest`, `build`).
3. Create the virtualenv, e.g., `python -m venv /home/carl/repos/acp-wrapper/.venv`, and install `pip install -r requirements.txt`.
4. Document the install steps so that future updates only modify the dedicated repo, leaving Talon’s shared interpreter untouched.
- ✅ Implemented this layout: `/home/carl/repos/acp-wrapper` now hosts `pyproject.toml`, `requirements.txt`, docs, and an actual `.venv` with `agent-client-protocol`/`pydantic`. The README spells out how to rebuild the venv and clarifies that `codex-acp` still comes from Talon’s npm installation path (or any other pre-existing binary) and is not installed via pip.

### 2. Wrapper architecture
1. Build a launch script (shell or Python) inside the project—call it `run-acp-agent`—that:
   - Activates the project’s `.venv` (source `./.venv/bin/activate` or adjust `$PATH`).
   - Ensures `agent-client-protocol` is importable (optionally run a quick health check by importing `_ensure_acp_dependency` before spawn).
   - Executes the real agent binary (`codex-acp`) with passed arguments, forwarding `stdin`/`stdout`/`stderr` so Talon sees the same JSON-RPC stream.
   - Optionally logs startup details (command line, cwd, env) so Talon’s `ACPFailure` notices see context.
2. The script should accept optional args/env to mirror Talon settings (`user.model_acp_agent_args`, `user.model_acp_agent_env`, `user.model_acp_agent_cwd`), but the wrapper can also parse Talon’s environment variables and pass them through.
3. Optionally provide a lightweight Python adapter that sits between the wrapper and `codex-acp` to inject additional logging or health endpoints (e.g., expose a TCP port for diagnostics) if needed.
- ✅ The wrapper is a `bash`/`\`run-acp-agent\`` script that activates `.venv`, then execs `python -m acp_wrapper.cli`. The `acp_wrapper.cli` driver logs startup context, imports `acp` from `agent-client-protocol`, respects `--agent-cmd`, `--agent-cwd`, and repeated `--agent-env` overrides (with `ACP_WRAPPER_*` fallbacks), and proxies stdin/stdout/stderr to whatever command (default `codex-acp`) is chosen. The `acp_wrapper.launcher` helpers normalize commands, environment overrides, and emit diagnostics before the subprocess is spawned.

### 3. Talon integration
1. Point `user.model_acp_agent_command` (see `my-config/user.talon:15` and `talon-ai-tools/lib/modelHelpers.py:436`) to `/home/carl/repos/acp-wrapper/run-acp-agent`.
2. Keep `user.model_acp_agent_args/cwd/env` available for overriding the wrapped agent’s behavior; the wrapper just forwards them to `codex-acp`.
3. Because `ACPTransport` uses `asyncio.create_subprocess_exec` with `stdin` and `stdout` pipes (`talon-ai-tools/lib/acp_client.py:120`), the wrapper must behave like a normal CLI: whatever it writes to stdout becomes the agent’s JSON-RPC output and whatever it reads from stdin is proxied to `codex-acp`.
4. Ensure the wrapper propagates exit codes so Talon’s `_ensure_connection` logic can detect failures and reinitialize the agent (e.g., log and re-raise if `codex-acp` dies).
- ✅ `my-config/user.talon` now points `user.model_acp_agent_command` at the wrapper. Any `user.model_acp_agent_*` overrides Talon still provides are forwarded through to the final `codex-acp` (or whatever command `ACP_WRAPPER_AGENT_COMMAND`/`--agent-cmd` selects).

### 4. Verification & automated tests
1. Add unit tests inside the wrapper project (e.g., `tests/test_wrapper.py`) that:
   - Launch the wrapper with a dummy agent (a simple Python script implementing the minimal JSON-RPC handshake) and assert that the wrapper proxies stdin/stdout correctly.
   - Simulate missing dependencies by temporarily renaming `agent-client-protocol` and verifying the wrapper returns a descriptive error (mirror `ACPTransport`’s failure path).
2. Add integration/smoke tests that:
   - Spawn `ACPTransport` from `talon-ai-tools` (maybe via a pytest fixture pointing `settings.user.model_acp_agent_command` at the wrapper) and ensure `send_request_to_acp` covers `AgentMessageChunk` responses (mock responses from the dummy agent).
   - Run `gpt_apply_prompt` or a simplified version to confirm actual Talon commands still complete when Talon talks to the wrapper.
3. Automate the tests with `pytest` so they can be run from the wrapper project (`python -m pytest`). Reference them in documentation so maintainers know how to verify after upgrades.
- ✅ Added `tests/test_wrapper.py` plus a `tests/dummy_agent.py`; pytest now covers stdin/stdout proxying as well as the missing dependency error path. The README documents the `python -m pytest` workflow so maintainers can rerun the suite whenever dependencies change.

### 5. Maintenance considerations
1. Keep the wrapper repo in sync with `agent-client-protocol` and `codex-acp` updates by pinning versions in `pyproject.toml` and updating them as needed; the project’s tests will signal breaking changes.
2. Document how to regenerate the virtualenv (`python -m venv`, `pip install`, `pip freeze`) and how to point Talon at the wrapper.
3. Add logging around agent startup (matching Talon’s existing logs) so missing binaries/dependencies still trigger the expected notifications (`ACPFailure` in `modelHelpers.py:412`).

## Deliverables
- New repo directory `/home/carl/repos/acp-wrapper` with `pyproject.toml`, `.venv`, and `run-acp-agent`.
- Wrapper tests and documentation proving Talon still receives `AgentMessageChunk` updates through the new subprocess.
- Updated Talon settings/examples that show `user.model_acp_agent_command` pointing at the wrapper plus any required environment wiring.
