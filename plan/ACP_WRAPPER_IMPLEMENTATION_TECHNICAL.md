# ACP Wrapper Integration - Technical Implementation Details

This document provides a technical deep-dive into how the ACP wrapper is integrated with talon-ai-tools.

## Architecture Overview

### Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│  Talon Voice Input                                       │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│  GPT/gpt.py → send_request()                            │
│  Picks appropriate model helper based on endpoint       │
└──────────────────────────┬──────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │ Check endpoint  │
                  └────────┬────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
      ┌───▼──┐         ┌──▼──┐        ┌──▼──┐
      │ HTTP │         │ LLM  │       │ ACP  │
      └──────┘         └──────┘       └───┬──┘
                                           │
                ┌──────────────────────────▼──────────────────────────┐
                │  modelHelpers.py: send_request_to_acp()             │
                │  - Validates endpoint = "acp"                       │
                │  - Calls _get_acp_transport()                       │
                │  - Builds ACP blocks from prompt                    │
                │  - Sends prompt and collects response               │
                │  - Formats response for Talon                       │
                └──────────────────────────┬──────────────────────────┘
                                           │
                ┌──────────────────────────▼──────────────────────────┐
                │  modelHelpers.py: _get_acp_transport()              │
                │  - Singleton factory pattern                        │
                │  - Calls _resolve_acp_agent_settings()              │
                │  - Creates ACPTransport instance                    │
                │  - Caches for reuse                                 │
                └──────────────────────────┬──────────────────────────┘
                                           │
                ┌──────────────────────────▼──────────────────────────┐
                │  modelHelpers.py: _resolve_acp_agent_settings()     │
                │  - Checks user.model_acp_use_wrapper                │
                │  - Calls _find_acp_wrapper_command()                │
                │  - Returns: (command, args, cwd, env, context)      │
                └──────────────────────────┬──────────────────────────┘
                                           │
                ┌──────────────────────────▼──────────────────────────┐
                │  acp_client.py: ACPTransport.__init__()             │
                │  - Validates command is not empty                   │
                │  - Parses args, env, cwd                            │
                │  - Starts event loop thread                         │
                │  - Waits for loop ready                             │
                │  - Spawns agent on first use                        │
                └──────────────────────────┬──────────────────────────┘
                                           │
          ┌────────────────────────────────┼────────────────────────────┐
          │                                │                            │
    ┌─────▼────┐              ┌───────────▼────────────┐       ┌──────▼──┐
    │  Wrapper  │              │  codex-acp direct      │       │  Other   │
    │ command   │              │  (if wrapper disabled) │       │  agent   │
    └─────┬────┘              └────────────────────────┘       └──────────┘
          │
    /home/carl/repos/acp-wrapper/run-acp-agent
          │
    ┌─────▼──────────────────────────────────────┐
    │  Wrapper Script Actions:                   │
    │  1. Activate .venv                         │
    │  2. Import dependency check                │
    │  3. Exec codex-acp (or other agent)        │
    │  4. Forward stdin/stdout/stderr            │
    │  5. Preserve JSON-RPC framing              │
    └─────┬──────────────────────────────────────┘
          │
    ┌─────▼──────────────────────────────────────┐
    │  codex-acp Process                         │
    │  - Receives JSON-RPC requests on stdin     │
    │  - Processes with LLM backend              │
    │  - Sends responses on stdout               │
    │  - Maintains session across requests       │
    └─────┬──────────────────────────────────────┘
          │
    ┌─────▼──────────────────────────────────────┐
    │  LLM Backend (Claude, GPT, etc)            │
    │  - Processes prompt                        │
    │  - Generates response                      │
    │  - Returns via codex-acp                   │
    └──────────────────────────────────────────┘
```

## Implementation Walkthrough

### 1. Settings Definition (`talonSettings.py`)

```python
mod.setting(
    "model_endpoint",
    type=str,
    default="https://api.openai.com/v1/chat/completions",
    desc='...set to "acp" to use ACP...'
)

mod.setting(
    "model_acp_use_wrapper",
    type=bool,
    default=True,
    desc="Prefer wrapper command if available"
)

mod.setting(
    "model_acp_agent_command",
    type=str,
    default="codex-acp",
    desc="Agent binary or wrapper path"
)

mod.setting(
    "model_acp_agent_args",      # Additional arguments
    "model_acp_agent_cwd",       # Working directory
    "model_acp_agent_env",       # Environment variables (KEY=VALUE format)
)
```

### 2. Endpoint Routing (`modelHelpers.py` - `send_request()`)

```python
def send_request(...):
    # ...setup code...
    model_endpoint: str = settings.get("user.model_endpoint")

    if model_endpoint == "llm":
        response = send_request_to_llm_cli(...)
    elif model_endpoint == "acp":
        response = send_request_to_acp(...)
    else:  # Default to HTTP API
        response = send_request_to_api(...)

    return response
```

### 3. Wrapper Detection (`modelHelpers.py`)

```python
ACP_WRAPPER_ENV = "ACP_WRAPPER_COMMAND"
ACP_WRAPPER_DEFAULT = Path.home() / "repos" / "acp-wrapper" / "run-acp-agent"

def _find_acp_wrapper_command() -> str | None:
    # Priority order:
    # 1. Environment variable override
    override = os.environ.get(ACP_WRAPPER_ENV)
    if override:
        return override

    # 2. Default installation path
    if ACP_WRAPPER_DEFAULT.exists():
        return str(ACP_WRAPPER_DEFAULT)

    # 3. Not found
    return None
```

### 4. Settings Resolution (`modelHelpers.py`)

```python
def _resolve_acp_agent_settings() -> tuple[str, str, str|None, str|None, str]:
    user_command = settings.get("user.model_acp_agent_command") or ""
    args = settings.get("user.model_acp_agent_args") or ""
    cwd = settings.get("user.model_acp_agent_cwd") or None
    env = settings.get("user.model_acp_agent_env") or None
    use_wrapper = settings.get("user.model_acp_use_wrapper")

    wrapper_command = _find_acp_wrapper_command() if use_wrapper else None

    # Resolve final command with priority:
    # 1. Explicit user command (if not default "codex-acp")
    # 2. Wrapper if available
    # 3. Default "codex-acp"
    final_command = user_command if user_command != "codex-acp" else ""
    source = "ACP command"

    if wrapper_command and not final_command:
        final_command = wrapper_command
        source = "ACP wrapper"

    if not final_command:
        final_command = "codex-acp"

    context = _format_acp_context(final_command, args, cwd, env, source)

    return final_command, args, cwd, env, context
```

### 5. Transport Singleton (`modelHelpers.py`)

```python
_acp_transport: ACPTransport | None = None
_acp_command_context: str | None = None

def _get_acp_transport() -> ACPTransport:
    global _acp_transport, _acp_command_context

    if _acp_transport is None:
        # Resolve settings
        command, args, cwd, env, context = _resolve_acp_agent_settings()
        _acp_command_context = context

        try:
            # Create transport
            _acp_transport = ACPTransport(
                command=command,
                args=args,
                cwd=cwd,
                env=env,
            )
        except Exception as exc:
            LOGGER.exception("Failed to initialize ACP agent (%s)", context)
            raise RuntimeError(f"ACP agent startup failed ({context}): {exc}") from exc

    return _acp_transport

def _reset_acp_transport() -> None:
    global _acp_transport, _acp_command_context
    _acp_transport = None
    _acp_command_context = None
```

### 6. Transport Layer (`acp_client.py`)

```python
class ACPTransport:
    def __init__(self, command: str, args: str, cwd: str|None, env: str|None):
        # Parse and validate inputs
        self._command_tokens = _parse_tokenized(command)
        self._command_tokens += _parse_tokenized(args)
        self._cwd = Path(cwd).expanduser() if cwd else None
        self._env = os.environ.copy()
        self._env.update(_parse_env(env or ""))

        # Setup event loop thread (for async/sync bridge)
        self._loop = asyncio.new_event_loop()
        self._loop_ready = threading.Event()
        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True,
            name="talon-acp"
        )
        self._thread.start()
        self._loop_ready.wait()

    async def _async_spawn_agent(self) -> None:
        LOGGER.info("Starting ACP agent: %s", " ".join(self._command_tokens))

        # Create subprocess with piped stdio
        proc = await asyncio.create_subprocess_exec(
            *self._command_tokens,
            stdin=aio_subprocess.PIPE,
            stdout=aio_subprocess.PIPE,
            cwd=str(self._cwd) if self._cwd else None,
            env=self._env,
        )

        # Establish ACP connection
        self._process = proc
        self._conn = connect_to_agent(
            self._client_impl,
            proc.stdin,
            proc.stdout
        )

        # Initialize ACP session
        await self._initialize_session()

    async def _initialize_session(self) -> None:
        await self._conn.initialize(
            protocol_version=PROTOCOL_VERSION,
            client_capabilities=ClientCapabilities(),
            client_info=Implementation(
                name="talon-ai-tools",
                title="Talon AI Tools",
                version="1.0"
            ),
        )
        session = await self._conn.new_session(
            cwd=str(self._cwd or Path.cwd()),
            mcp_servers=[]
        )
        self._session_id = session.session_id

    async def _async_prompt(self, blocks: list[Any], model: str) -> str:
        # Ensure connection is alive
        await self._ensure_connection()
        session_id = self._ensure_session_id()

        # Optionally override model
        if model:
            try:
                await self._conn.set_session_model(
                    model_id=model,
                    session_id=session_id
                )
            except RequestError as exc:
                LOGGER.debug("ACP ignored model switch to %s: %s", model, exc)

        # Send prompt and collect response
        self._response_chunks.clear()
        await self._conn.prompt(prompt=blocks, session_id=session_id)

        return self._pop_responses()
```

### 7. Response Capture (`acp_client.py`)

```python
class _TalonACPClient(Client):
    async def session_update(self, session_id: str, update: Any, **kwargs: Any) -> None:
        # Called when agent sends AgentMessageChunk
        if isinstance(update, AgentMessageChunk):
            content = update.content
            text = self._text_from_content(content)
            self._transport._append_response(text)

    def _text_from_content(self, content: Any) -> str:
        if isinstance(content, TextContentBlock):
            return content.text
        elif isinstance(content, ImageContentBlock):
            return "<image>"
        elif isinstance(content, ResourceContentBlock):
            return getattr(content, "uri", "<resource>")
        elif isinstance(content, EmbeddedResourceContentBlock):
            return "<resource>"
        elif isinstance(content, AudioContentBlock):
            return "<audio>"
        return ""
```

## Key Design Decisions

### 1. Wrapper Preference Model
- **Default**: Use wrapper if available (`user.model_acp_use_wrapper=True`)
- **Rationale**: Wrapper isolates dependencies from Talon's shared interpreter
- **Override**: Users can disable wrapper or specify direct command

### 2. Singleton Transport Pattern
- **Goal**: Reuse single agent process across requests
- **Benefit**: Preserves session state between prompts
- **Recovery**: Reset transport on error and reconnect on next request

### 3. Threading Model
- **Problem**: Talon integrates asyncio differently than standard Python
- **Solution**: Spin up dedicated event loop thread in transport
- **Interface**: `_call_async()` bridges sync Talon calls to async transport

### 4. Environment Variable Parsing
- **Format**: Space-separated KEY=VALUE entries
- **Flexible**: Supports multiple overrides via `user.model_acp_agent_env`
- **Precedence**: CLI args override default, env vars override settings

### 5. Error Recovery
- **Pattern**: Singleton reset on failure → reconnect on next request
- **Benefit**: Transient failures don't permanently break agent
- **Logging**: Full context (command, args, env) logged for debugging

## Testing Considerations

### Unit Test Scope
- Settings resolution logic
- Command/arg/env parsing
- Block building from prompts
- Context string formatting
- Error path handling

### Integration Test Scope
- Transport creation and connection
- Request/response proxying
- Session lifecycle
- Multiple sequential requests
- Model override behavior

### End-to-End Test Scope
- Real wrapper subprocess interaction
- Real codex-acp (or mock) agent response
- Full JSON-RPC framing
- Talon voice command → result flow

### Test Helpers Needed
- Mock subprocess generator (dummy agent)
- Mock ACPTransport for isolation testing
- Fixture for temporary acp-wrapper directory
- Fixture for environment variable isolation

## Common Issues & Solutions

### Issue 1: "Failed to find wrapper binary"
**Symptoms**: Falls back to codex-acp, logs warning
**Solution**:
- Check `ACP_WRAPPER_COMMAND` env var
- Verify `~/.repos/acp-wrapper/run-acp-agent` exists
- Verify executable permissions: `chmod +x run-acp-agent`

### Issue 2: "agent-client-protocol import failed"
**Symptoms**: RuntimeError about missing package
**Solution**:
- Check wrapper venv: `~/.repos/acp-wrapper/.venv/bin/python -m pip list`
- Rebuild venv: `cd ~/.repos/acp-wrapper && python -m venv .venv && pip install -r requirements.txt`
- Verify SDK version in requirements.txt

### Issue 3: "JSON-RPC framing error"
**Symptoms**: Agent process exits or returns garbage
**Solution**:
- Check codex-acp binary validity
- Verify wrapper properly forwards stdin/stdout
- Enable debug logging: `LOGGER.setLevel(logging.DEBUG)`
- Check agent logs if available

### Issue 4: "Session hangs or timeout"
**Symptoms**: Prompt appears to hang indefinitely
**Solution**:
- Check agent resource availability (CPU, memory)
- Review codex-acp logs for stalled requests
- Consider adding request timeout to future versions

## Related Standards & Specifications

- **ACP Protocol**: https://github.com/zed-industries/codex-acp
- **Agent-Client-Protocol SDK**: https://github.com/zed-industries/agent-client-protocol
- **JSON-RPC 2.0**: https://www.jsonrpc.org/specification
- **Talon API**: https://talon.wiki
