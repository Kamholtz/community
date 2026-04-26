The following list are Cursorless, Emacs, commands. When the Emacs application is active, I want these commands to be available. H command should be starting with the word "curse".

You should make a checklist item from each item in the list within this file and check them off as you make each command.

You should make a new file for these specific Emacs commands in the same directory as the existing Emacs, talon, config.

The file name should be. emacs-cursorless.talon

- [x] `cursorless-casual-start`: Start Cursorless in Talon mode for normal development.
- [x] `cursorless-casual-restart`: Restart the Cursorless host and keep command-server settings.
- [x] `cursorless-casual-stop`: Stop the Cursorless host and command server.
- [x] `cursorless-casual-reload-files`: Reload Cursorless source files from disk (optionally restart host).
- [x] `cursorless-casual-open-debug-buffers`: Display output, protocol, stderr, and Talon event buffers for debugging.
- [x] `cursorless-casual-open-protocol-buffer`: Open the Cursorless protocol buffer for debugging.
- [x] `cursorless-casual-open-latest-log`: Open the latest per-request Org log.
- [x] `cursorless-casual-open-log-picker`: Open a picker for per-request Org logs.
- [x] `cursorless-casual-copy-latest-log-path`: Copy the latest per-request Org log path.
- [x] `cursorless-casual-copy-session-id`: Copy the current Emacs session id.
- [x] `cursorless-casual-open-protocol-buffer-at-latest-command`: Open protocol buffer at the latest outbound runCommand entry.
- [x] `cursorless-casual-capture-visible-state`: Show all visible buffers and files.
- [x] `cursorless-casual-restart-server`: Stop and restart the Emacs server.
- [x] `cursorless-casual-restart-and-restore`: Capture visible files, restart Emacs server, reopen files, start Cursorless.
- [x] `cursorless-casual-open-js-test-buffer`: Open the buffer used by Cursorless live sync tests.
- [x] `cursorless-casual-run-debug-command`: Execute a Cursorless debug command via completion.
- [x] `cursorless-casual-describe-debug-commands`: Show help buffer with Cursorless debugging commands and key hints.
- [x] `cursorless-casual-reload-and-restart`: Reload Cursorless files and force a host restart.

- [x] `cursorless-prototype-refresh-hat-overlays`: Rerender all currently tracked hats using the latest customization values.
- [x] `cursorless-prototype-monitoring-reset`: Reset in-memory monitoring counters.
- [x] `cursorless-prototype-monitoring-stats-alist`: Show current monitoring stats as an alist.
- [x] `cursorless-prototype-monitoring-flush-summary`: Force one monitoring summary emission now.
- [x] `cursorless-prototype-start-talon-events-tail`: Start Talon events.tail() logging in a dedicated process buffer.
- [x] `cursorless-prototype-stop-talon-events-tail`: Stop the Talon events.tail() logging process.
- [x] `cursorless-prototype-send-document-created`: Send a hardcoded documentCreated message.
- [x] `cursorless-prototype-send-current-document-created`: Send a serialized documentCreated snapshot for the current window.
- [x] `cursorless-prototype-send-current-document-changed`: Send a serialized documentChanged snapshot for the current window.
- [x] `cursorless-prototype-send-current-document-closed`: Send documentClosed for the current window and remove it from the registry.
- [x] `cursorless-prototype-send-run-command`: Send a hardcoded runCommand message.
- [x] `cursorless-prototype-send-invalid-run-command`: Send an intentionally invalid runCommand message for negative testing.
- [x] `cursorless-prototype-replay-last-callback`: Replay the most recently saved callback message.
- [x] `cursorless-prototype-start`: Start the Node.js Cursorless sidecar process and run the demo flow.
- [x] `cursorless-prototype-stop`: Stop the running Cursorless prototype process.
- [x] `cursorless-prototype-restart`: Restart the host from healthy or failed states.
- [x] `cursorless-prototype-run-demo`: Send the hardcoded document and command to the running process.

- [x] `cursorless-command-log-reset`: Reset command outcome logging state.
- [x] `cursorless-command-log-enable-outline-folding`: Enable outline-based folding in the current command log buffer.
- [x] `cursorless-command-log-open-latest-command`: Open protocol buffer at the latest command outcome heading.
- [x] `cursorless-command-log-hide-command-details`: Fold protocol log to top-level command headings.
- [x] `cursorless-command-log-show-all-command-details`: Unfold all command protocol blocks.

- [x] `cursorless-command-server-check-and-handle-request`: Check for request.json and process it if present.
- [x] `cursorless-command-server-start`: Start polling for Talon-compatible file RPC requests.
- [x] `cursorless-command-server-stop`: Stop polling for requests.

- [x] `cursorless-engine-send-hat-settings`: Send current hat settings to the running Node host.

- [x] `cursorless-session-log-copy-latest-path`: Copy the latest request log path to the kill ring.
- [x] `cursorless-session-log-copy-session-id`: Copy the current session UUID to the kill ring.
- [x] `cursorless-session-log-open-latest`: Open the latest current-session log file.
