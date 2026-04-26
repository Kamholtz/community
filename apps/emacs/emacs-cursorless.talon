app: emacs
-

curse start: user.emacs("cursorless-casual-start")
curse restart: user.emacs("cursorless-casual-restart")
curse stop: user.emacs("cursorless-casual-stop")
curse reload files: user.emacs("cursorless-casual-reload-files")
curse open debug buffers: user.emacs("cursorless-casual-open-debug-buffers")
curse open protocol buffer: user.emacs("cursorless-casual-open-protocol-buffer")
curse open latest log: user.emacs("cursorless-casual-open-latest-log")
curse open log picker: user.emacs("cursorless-casual-open-log-picker")
curse copy latest log path: user.emacs("cursorless-casual-copy-latest-log-path")
curse copy session id: user.emacs("cursorless-casual-copy-session-id")
curse open protocol [buffer] [at] latest [command]:
    user.emacs("cursorless-casual-open-protocol-buffer-at-latest-command")
curse capture visible state: user.emacs("cursorless-casual-capture-visible-state")
curse restart server: user.emacs("cursorless-casual-restart-server")
curse restart and restore: user.emacs("cursorless-casual-restart-and-restore")
curse open js test buffer: user.emacs("cursorless-casual-open-js-test-buffer")
curse run debug command: user.emacs("cursorless-casual-run-debug-command")
curse describe debug commands: user.emacs("cursorless-casual-describe-debug-commands")
curse reload and restart: user.emacs("cursorless-casual-reload-and-restart")

curse refresh hat overlays: user.emacs("cursorless-prototype-refresh-hat-overlays")
curse monitoring reset: user.emacs("cursorless-prototype-monitoring-reset")
curse monitoring stats alist: user.emacs("cursorless-prototype-monitoring-stats-alist")
curse monitoring flush summary:
    user.emacs("cursorless-prototype-monitoring-flush-summary")
curse start talon events tail:
    user.emacs("cursorless-prototype-start-talon-events-tail")
curse stop talon events tail: user.emacs("cursorless-prototype-stop-talon-events-tail")
curse send document created: user.emacs("cursorless-prototype-send-document-created")
curse send current document created:
    user.emacs("cursorless-prototype-send-current-document-created")
curse send current document changed:
    user.emacs("cursorless-prototype-send-current-document-changed")
curse send current document closed:
    user.emacs("cursorless-prototype-send-current-document-closed")
curse send run command: user.emacs("cursorless-prototype-send-run-command")
curse send invalid run command:
    user.emacs("cursorless-prototype-send-invalid-run-command")
curse replay last callback: user.emacs("cursorless-prototype-replay-last-callback")
curse start: user.emacs("cursorless-prototype-start")
curse stop: user.emacs("cursorless-prototype-stop")
curse restart: user.emacs("cursorless-prototype-restart")
curse run demo: user.emacs("cursorless-prototype-run-demo")

curse log reset: user.emacs("cursorless-command-log-reset")
curse log enable outline folding:
    user.emacs("cursorless-command-log-enable-outline-folding")
curse log open latest command: user.emacs("cursorless-command-log-open-latest-command")
curse log hide command details:
    user.emacs("cursorless-command-log-hide-command-details")
curse log show all command details:
    user.emacs("cursorless-command-log-show-all-command-details")

curse server check and handle request:
    user.emacs("cursorless-command-server-check-and-handle-request")
curse server start: user.emacs("cursorless-command-server-start")
curse server stop: user.emacs("cursorless-command-server-stop")

curse engine send hat settings: user.emacs("cursorless-engine-send-hat-settings")

curse log copy latest path: user.emacs("cursorless-session-log-copy-latest-path")
curse log copy session id: user.emacs("cursorless-session-log-copy-session-id")
curse log open latest: user.emacs("cursorless-session-log-open-latest")
