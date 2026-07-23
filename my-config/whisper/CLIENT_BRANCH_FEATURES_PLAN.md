# Whisper Mode Client-Branch Features Plan

## Goal

Extend Talon's Whisper mode to support the optional transcript polishing,
session polishing, vocabulary, and screen-context features described in
`realtimestt-cli/CLIENT_BRANCH_FEATURES.md`, while preserving the existing
low-latency realtime and final transcript behavior.

The implementation will primarily update:

- `my-config/whisper/whisper_mode.py`
- `my-config/whisper/whisper_mode.talon`
- `realtimestt-cli/webserver/client.py` where persistent client control is
  required

## 1. Define the Talon-facing behavior

Add actions and voice commands for:

- Starting and stopping Whisper with graceful session polishing.
- Requesting session polishing without stopping.
- Setting screen context from text.
- Capturing and sending a screenshot as context.
- Showing the current context.
- Clearing context.
- Viewing or inserting the last session-polished transcript.

Add Talon settings controlling:

- Whether per-segment polishing is used.
- How long to wait for `polished` before inserting the original `full`.
- Whether stopping Whisper requests session polishing.
- The graceful-shutdown timeout.
- Screenshot capture behavior and context-command timeout.

## 2. Refactor transcript state

Replace the single `_whisper_last_full` value with structured pending transcript
state containing:

- The original `full` text.
- An optional `polished` replacement.
- Whether the transcript has been inserted.
- Its fallback timer.
- Its Whisper history-entry identity.

This state is necessary because a `polished` event does not contain a transcript
ID. It implicitly replaces the most recent corresponding `full` event.

Keep duplicate-event suppression, but separate it from pending transcript
association so repeated text in two legitimate utterances is not accidentally
dropped.

## 3. Support per-segment polished transcripts

Use safe deferred insertion:

1. On `full`, display the final transcript immediately.
2. Start a short configurable fallback timer instead of inserting immediately.
3. If `polished` arrives, cancel the timer and insert the polished text.
4. If no polished text arrives before the timeout, insert the original `full`.
5. Store only the text actually inserted in Whisper history.
6. Display distinct `Polishing` and `Polished` HUD/subtitle states.

Deferred insertion is safer than inserting `full` and later issuing backspaces:
the user might move the caret, change applications, or edit the inserted text
before the polished event arrives.

If polishing is disabled, provide a setting that makes `full` insertion
immediate and preserves the current behavior.

## 4. Add a persistent machine-control channel to the client

The current CLI exposes context operations only as startup options. Talon also
cannot send `session_polish` or `disconnect` to an already-running client.

Extend `webserver/client.py` with JSON Lines commands on stdin:

```json
{"type":"session_polish"}
{"type":"disconnect"}
{"type":"context_text","content":"Visible file: server.py"}
{"type":"context_image","content":{"mime_type":"image/png","data":"..."}}
{"type":"context_status"}
{"type":"clear_context"}
```

Keep websocket events on stdout and diagnostic logs on stderr. Start the client
from Talon with `stdin=subprocess.PIPE`, and write commands through a
thread-safe command queue.

Using the existing persistent connection is important because session polishing
must operate on the websocket session that accumulated the finalized
transcripts. A separate one-shot client would have an empty session transcript.

## 5. Implement graceful Whisper shutdown

Change `whisper_done` from immediate process termination to an asynchronous
shutdown sequence:

1. Flush or resolve any pending `full` transcript insertion.
2. Send `{"type":"disconnect"}` to the active client.
3. Handle `session_disconnect_pending`.
4. Wait for `session_polished` or `session_error`.
5. Save and display the session result.
6. Allow the server to close the websocket.
7. Restore Talon modes, speech, HUD theme, status icon, and subtitles.
8. Force-terminate the client only after a configurable timeout.

Do not rely on simulated Ctrl+C. It is unreliable on Windows when the client is
started with `CREATE_NO_WINDOW`.

## 6. Handle session events

Add handlers for:

- `session_disconnect_pending`: show a `Finishing transcription` state.
- `session_polished`: save the result, notify the user, and expose actions to
  display, copy, or insert it.
- `session_error`: retain the normal per-utterance transcripts and report the
  failure without losing existing text.

Do not automatically replace all previously inserted text with the
session-polished result. A Whisper session may span multiple fields,
applications, or caret positions.

## 7. Add screen-context actions

Implement actions equivalent to:

```text
whisper_context_set(text)
whisper_context_capture()
whisper_context_show()
whisper_context_clear()
```

For screenshot context:

1. Capture the active window or selected screen through Talon.
2. Encode the image as PNG, preferably in memory.
3. Send it through the persistent client control channel.
4. Handle `context_pending`, `context_updated`, and `context_error`.
5. Prevent overlapping capture requests, or explicitly replace the pending
   request.

Display `context_status` in an ImGui window because it contains structured data
and may be too long for a notification.

Direct text context should be exposed as a Talon action for use by other scripts
and integrations. Free-form spoken arguments are less suitable while
`user.whisper` mode suppresses normal command mode.

## 8. Update UI states and voice commands

Extend the status labels and subtitle colors for:

- `polishing`
- `polished`
- `session_finishing`
- `context_pending`
- `context_ready`
- `context_error`

Add commands to `whisper_mode.talon`, with final wording confirmed during
implementation. Candidate phrases are:

```talon
whisper polish session: user.whisper_polish_session()
whisper context screen: user.whisper_context_capture()
whisper context show: user.whisper_context_show()
whisper context clear: user.whisper_context_clear()
whisper session show: user.whisper_session_show()
whisper session insert: user.whisper_session_insert()
```

Ensure the commands that must work while Whisper is active are scoped so they
remain available in `user.whisper` mode.

## 9. Vocabulary integration

Keep `webserver/vocabulary.json` as the single source of truth.

No duplicate Talon-side replacement logic is required because:

- Vocabulary terms are added to Whisper and polishing prompts by the server.
- Deterministic replacements are applied by the server before polishing.
- `full` events already contain those replacements.

Optionally add an action to open the vocabulary file, but do not maintain a
second vocabulary copy in `whisper_mode.py`.

## 10. Separate stdout and stderr handling

The client documents that JSON Lines events are written to stdout and logs to
stderr. Update subprocess handling so:

- stdout is parsed strictly as JSON Lines.
- stderr is drained independently to avoid a blocked pipe.
- useful errors can be logged or surfaced without being treated as websocket
  events.

The current `stderr=subprocess.STDOUT` arrangement works only because invalid
JSON lines are silently ignored; explicit separation will make failures easier
to diagnose.

## 11. Testing

Add isolated tests for:

- `full` followed by `polished`.
- `full` with no polished response.
- Polishing disabled with immediate `full` insertion.
- Multiple sequential `full`/`polished` pairs.
- Legitimate repeated transcript text.
- Duplicate websocket events.
- Shutdown while transcription or polishing is pending.
- `session_disconnect_pending`, `session_polished`, and `session_error`.
- Graceful-shutdown timeout and forced cleanup.
- Every context response type.
- Screenshot encoding and supported MIME types.
- Process EOF and reconnect behavior.
- Whisper history containing the text actually inserted.
- Client logs on stderr never being interpreted as websocket events.

Where practical, separate event/state logic from Talon UI calls so it can be
unit-tested without a live Talon process.

## 12. Validation workflow

Before implementation, run the required pre-edit hook:

```bash
python3 .agents/scripts/agent_pre_edit_commit.py
```

During implementation, run the quick repository gate:

```bash
python3 .agents/scripts/check_talon_config.py --skip-tests
```

After changing Talon Python or `.talon` files, check reload errors:

```bash
python3 .agents/scripts/check_talon_config.py --talon-errors
```

Before handoff, run the full repository gate:

```bash
python3 .agents/scripts/check_talon_config.py
```

Perform live integration checks with:

- Polisher enabled and disabled.
- Polisher timeout or model failure.
- Direct text context.
- Screenshot context success and extraction failure.
- Context show and clear.
- Session polish while connected.
- Graceful Whisper shutdown with a final transcription still in flight.

## Suggested implementation order

1. Separate pure transcript state from Talon UI and insertion operations.
2. Add `polished` event handling and fallback insertion.
3. Add the client's persistent stdin control protocol.
4. Add graceful session shutdown and session event handling.
5. Add direct context commands.
6. Add screenshot capture and context status UI.
7. Add Talon actions, voice commands, settings, and documentation.
8. Complete automated and live validation.

