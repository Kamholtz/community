app: emacs
-

tag(): user.tabs
tag(): user.splits
tag(): user.line_commands

# VSCode hunt commands to port (replace TODO_* with emacs commands)
# symbol hunt [<user.text>]: user.emacs("TODO_SYMBOL_HUNT")
# symbol hunt all [<user.text>]: user.emacs("TODO_SYMBOL_HUNT_ALL")
# file hunt [<user.text>]: user.emacs("TODO_FILE_HUNT")
# file hunt (pace | paste): user.emacs("TODO_FILE_HUNT_PASTE")
# (term | terminal) focus hunt [<user.text>]: user.emacs("TODO_TERMINAL_FOCUS_HUNT")

# ----- GENERAL ----- #
#suplex: key(ctrl-x)
cancel: user.emacs("keyboard-quit")
exchange: user.emacs("exchange-point-and-mark")
execute: user.emacs("execute-extended-command")
execute {user.emacs_command}$: user.emacs(emacs_command)
execute <user.text>$:
    user.emacs("execute-extended-command")
    user.insert_formatted(text, "DASH_SEPARATED")
evaluate | (evaluate | eval) (exper | expression): user.emacs("eval-expression")
prefix: user.emacs_prefix()
prefix <user.number_signed_small>: user.emacs_prefix(number_signed_small)

abort recursive [edit]: user.emacs("abort-recursive-edit")
browse kill ring: user.emacs("browse-kill-ring")
fill paragraph: user.emacs("fill-paragraph")
insert char: user.emacs("insert-char")
occurs: user.emacs("occur")
other scroll [down]: user.emacs("scroll-other-window")
other scroll up: user.emacs("scroll-other-window-down")
package autoremove: user.emacs("package-autoremove")
package list | [package] list packages: user.emacs("list-packages")
reverse (lines | region): user.emacs("reverse-region")
disk: user.emacs("save-buffer")
save buffers kill emacs: user.emacs("save-buffers-kill-emacs")
save some buffers: user.emacs("save-some-buffers")
sort lines: user.emacs("sort-lines")
sort words: user.emacs("sort-words")
file [loop] continue: user.emacs("fileloop-continue")

go directory: user.emacs("dired-jump")
other go directory: user.emacs("dired-jump-other-window")

[toggle] debug on error: user.emacs("toggle-debug-on-error")
[toggle] debug on quit: user.emacs("toggle-debug-on-quit")
[toggle] input method: user.emacs("toggle-input-method")
[toggle] truncate lines: user.emacs("toggle-truncate-lines")
[toggle] word wrap: user.emacs("toggle-word-wrap")

manual: user.emacs("man")
manual <user.text>:
    user.emacs("man")
    user.insert_formatted(text, "DASH_SEPARATED")

# BUFFER SWITCHING #
switch: user.emacs("switch-to-buffer")
other switch: user.emacs("switch-to-buffer-other-window")
display: user.emacs("display-buffer")

# SHELL COMMANDS #
shell command: user.emacs("shell-command")
shell command inserting:
    user.emacs_prefix()
    user.emacs("shell-command")
shell command on region: user.emacs("shell-command-on-region")
shell command on region replacing:
    user.emacs_prefix()
    user.emacs("shell-command-on-region")

# CUSTOMIZE #
customize face: user.emacs("customize-face")
customize face <user.text>$:
    user.emacs("customize-face")
    user.insert_formatted(text, "DASH_SEPARATED")
customize group: user.emacs("customize-group")
customize variable: user.emacs("customize-variable")
(customize | custom) [theme] visit theme: user.emacs("custom-theme-visit-theme")

# MODE COMMANDS #
auto fill mode: user.emacs("auto-fill-mode")
dired omit mode: user.emacs("dired-omit-mode")
display line numbers mode: user.emacs("display-line-numbers-mode")
electric quote local mode: user.emacs("electric-quote-local-mode")
emacs lisp mode: user.emacs("emacs-lisp-mode")
fundamental mode: user.emacs("fundamental-mode")
global display line numbers mode: user.emacs("global-display-line-numbers-mode")
global highlight line mode: user.emacs("global-hl-line-mode")
global visual line mode: user.emacs("global-visual-line-mode")
highlight line mode: user.emacs("hl-line-mode")
lisp interaction mode: user.emacs("lisp-interaction-mode")
markdown mode: user.emacs("markdown-mode")
menu bar mode: user.emacs("menu-bar-mode")
overwrite mode: user.emacs("overwrite-mode")
paredit mode: user.emacs("paredit-mode")
rainbow mode: user.emacs("rainbow-mode")
read only mode: user.emacs("read-only-mode")
shell script mode: user.emacs("sh-mode")
sub word mode: user.emacs("subword-mode")
tab bar mode: user.emacs("tab-bar-mode")
talon script mode: user.emacs("talonscript-mode")
text mode: user.emacs("text-mode")
transient mark mode: user.emacs("transient-mark-mode")
visual line mode: user.emacs("visual-line-mode")
whitespace mode: user.emacs("whitespace-mode")

# MACROS #
emacs record: user.emacs("kmacro-start-macro")
emacs stop: user.emacs("kmacro-end-macro")
emacs play: user.emacs("kmacro-end-and-call-macro")

# PROFILER #
profiler start: user.emacs("profiler-start")
profiler stop: user.emacs("profiler-stop")
profiler report: user.emacs("profiler-report")

# WINDOW/SPLIT MANAGEMENT #
# What emacs calls windows, we call splits.
split solo: user.emacs("delete-other-windows")
[split] rebalance: user.emacs("balance-windows")
split shrink: user.emacs("shrink-window-if-larger-than-buffer")
other [split] shrink:
    user.split_next()
    user.emacs("shrink-window-if-larger-than-buffer")
    user.split_last()
split grow: user.emacs("enlarge-window")
split grow <number_small>: user.emacs("enlarge-window", number_small)
split shrink <number_small>:
    amount = number_small or 1
    user.emacs("enlarge-window", 0 - amount)
split widen [<number_small>]:
    user.emacs("enlarge-window-horizontally", number_small or 1)
split narrow [<number_small>]:
    user.emacs("shrink-window-horizontally", number_small or 1)

# ----- HELP ----- #
apropos: user.emacs_help("a")
describe (fun | function): user.emacs_help("f")
describe key: user.emacs_help("k")
describe key briefly: user.emacs_help("c")
describe symbol: user.emacs_help("o")
describe variable: user.emacs_help("v")
describe mode: user.emacs_help("m")
describe bindings: user.emacs_help("b")
describe (char | character): user.emacs("describe-character")
describe text properties: user.emacs("describe-text-properties")
describe face: user.emacs("describe-face")
view lossage: user.emacs_help("l")

apropos <user.text>$:
    user.emacs_help("a")
    user.insert_formatted(text, "DASH_SEPARATED")
    key(enter)
describe (fun | function) <user.text>$:
    user.emacs_help("f")
    user.insert_formatted(text, "DASH_SEPARATED")
    key(enter)
describe symbol <user.text>$:
    user.emacs_help("o")
    user.insert_formatted(text, "DASH_SEPARATED")
    key(enter)
describe variable <user.text>$:
    user.emacs_help("v")
    user.insert_formatted(text, "DASH_SEPARATED")
    key(enter)

# ----- FILES & BUFFERS -----
file open: user.emacs("find-file")
file rename: user.emacs("rename-file")
(file open | find file) at point: user.emacs("ffap")
other file open: user.emacs("find-file-other-window")

# File hunt commands (VSCode-style quick file picker)
file hunt [<user.text>]:
    user.emacs("consult-fd")
    sleep(50ms)
    insert(text or "")

file hunt (pace | paste):
    user.emacs("consult-fd")
    sleep(50ms)
    edit.paste()

# File hunt for +default/find-file-under-here
file hunt under here [<user.text>]:
    user.emacs("+default/find-file-under-here")
    sleep(50ms)
    insert(text or "")

file hunt under here (pace | paste):
    user.emacs("+default/find-file-under-here")
    sleep(50ms)
    edit.paste()

# File hunt for find-file
file hunt find file [<user.text>]:
    user.emacs("find-file")
    sleep(50ms)
    insert(text or "")

file hunt find file (pace | paste):
    user.emacs("find-file")
    sleep(50ms)
    edit.paste()

(file | buffer) close:
    user.emacs("kill-buffer")
    key(enter)

please [<user.text>]:
    user.emacs("execute-extended-command")
    sleep(50ms)
    insert(text or "")

please (pace | paste):
    user.emacs("execute-extended-command")
    sleep(50ms)
    edit.paste()

# Buffer hunt commands (VSCode-style quick buffer picker)
buffer hunt [<user.text>]:
    user.emacs("consult-buffer")
    sleep(50ms)
    insert(text or "")

buffer hunt (pace | paste):
    user.emacs("consult-buffer")
    sleep(50ms)
    edit.paste()

# Buffer hunt commands (VSCode-style quick buffer picker)
symbol hunt [<user.text>]:
    user.emacs("core-lsp-document-symbols")
    sleep(50ms)
    insert(text or "")

symbol hunt (pace | paste):
    user.emacs("core-lsp-document-symbols")
    sleep(50ms)
    edit.paste()

# Buffer hunt commands (VSCode-style quick buffer picker)
symbol hunt all [<user.text>]:
    user.emacs("core-lsp-workspace-symbols")
    sleep(50ms)
    insert(text or "")

symbol hunt all (pace | paste):
    user.emacs("core-lsp-workspace-symbols")
    sleep(50ms)
    edit.paste()

buffer kill: user.emacs("kill-buffer")
buffer bury: user.emacs("bury-buffer")
buffer revert | revert buffer: user.emacs("revert-buffer")
buffer finish:
    edit.save()
    user.emacs("server-edit")
buffer list: user.emacs("buffer-menu")
buffer next: user.emacs("next-buffer")
buffer last: user.emacs("previous-buffer")
buffer rename: user.emacs("rename-buffer")
buffer widen: user.emacs("widen")
buffer narrow | [buffer] narrow to region: user.emacs("narrow-to-region")

diff (buffer | [buffer] with file):
    user.emacs("diff-buffer-with-file")
    key(enter)

# ----- MOTION AND EDITING ----- #
mark: user.emacs("set-mark-command")
go back: user.emacs("pop-to-mark-command")
global [go] back: user.emacs("pop-global-mark")

auto indent: user.emacs("indent-region")
indent <user.number_signed_small>: user.emacs("indent-rigidly", number_signed_small)

search back: user.emacs("isearch-backward")
search regex | regex search: user.emacs("isearch-forward-regexp")
(search regex | regex search) back: user.emacs("isearch-backward-regexp")
hunt this: user.emacs("evil-ex-search-forward")
hunt this <number_small>: user.emacs("evil-ex-search-forward", number_small)
hunt this <user.text>:
    user.emacs("evil-ex-search-forward")
    sleep(50ms)
    insert(text)
hunt this <number_small> <user.text>:
    user.emacs("evil-ex-search-forward", number_small)
    sleep(50ms)
    insert(text)
replace: user.emacs("query-replace")
replace regex | regex replace: user.emacs("query-replace-regexp")
# These start a word/symbol-search or toggle an existing search's mode.
search [toggle] words: user.emacs("isearch-forward-word")
search [toggle] symbol: user.emacs("isearch-forward-symbol")
# These keybindings are only active in isearch-mode.
search edit: user.emacs_meta("e")
search toggle case [fold | sensitive]: user.emacs_meta("c")
search toggle regex: user.emacs_meta("r")

highlight lines matching [regex]: user.emacs("highlight-lines-matching-regexp")
highlight phrase: user.emacs("highlight-phrase")
highlight regex: user.emacs("highlight-regexp")
unhighlight (regex | phrase): user.emacs("unhighlight-regexp")
unhighlight all:
    user.emacs_prefix()
    user.emacs("unhighlight-regexp")

recenter:
    user.emacs_prefix()
    user.emacs("recenter-top-bottom")
(center | [center] <number_small> from) top:
    user.emacs("recenter-top-bottom", number_small or 0)
(center | [center] <number_small> from) bottom:
    number = number_small or 0
    user.emacs("recenter-top-bottom", -1 - number)
go <number> top:
    edit.jump_line(number)
    user.emacs("recenter-top-bottom", 0)
go <number> bottom:
    edit.jump_line(number)
    user.emacs("recenter-top-bottom", -2)

next error | error next: user.emacs("next-error")
last error | error last: user.emacs("previous-error")

term right: user.emacs("forward-sexp")
term left: user.emacs("backward-sexp")
term up: user.emacs("backward-up-list")
term end: user.emacs("up-list")
term down: user.emacs("down-list")
term kill: user.emacs("kill-sexp")
term wipe: user.emacs("kill-sexp", -1)
term (mark | select): user.emacs("mark-sexp")
term copy:
    user.emacs("mark-sexp")
    edit.copy()
term freeze:
    user.emacs("mark-sexp")
    user.emacs("comment-region")
term [auto] indent:
    user.emacs("mark-sexp")
    user.emacs("indent-region")

(sentence | sent) (right | end): edit.sentence_end()
(sentence | sent) (left | start): edit.sentence_start()
(sentence | sent) kill: user.emacs("kill-sentence")

graph kill: user.emacs("kill-paragraph")
graph up: edit.paragraph_start()
graph down: edit.paragraph_end()
graph mark: user.emacs("mark-paragraph")
graph copy:
    user.emacs("mark-paragraph")
    edit.copy()
graph cut:
    user.emacs("mark-paragraph")
    edit.cut()

# NB. can use these to implement "drag <X> left/right/up/down" commands,
# but note that 'transpose line' and 'drag line down' are different.
transpose [word | words]: user.emacs("transpose-words")
transpose (term | terms): user.emacs("transpose-sexps")
transpose (char | chars): user.emacs("transpose-chars")
transpose (line | lines): user.emacs("transpose-lines")
transpose (sentence | sentences): user.emacs("transpose-sentences")
transpose (graph | graphs | paragraphs): user.emacs("transpose-paragraphs")

register (copy | save): user.emacs("copy-to-register")
register (paste | insert): user.emacs("insert-register")
register jump: user.emacs("jump-to-register")
register (copy | save) rectangle: user.emacs("copy-rectangle-to-register")

rectangle clear: user.emacs("clear-rectangle")
rectangle delete: user.emacs("delete-rectangle")
rectangle kill: user.emacs("kill-rectangle")
rectangle open: user.emacs("open-rectangle")
rectangle (copy | save) [to] register: user.emacs("copy-rectangle-to-register")
rectangle (yank | paste): user.emacs("yank-rectangle")
rectangle copy: user.emacs("copy-rectangle-as-kill")
rectangle number lines: user.emacs("rectangle-number-lines")

# ----- XREF SUPPORT ----- #
[xref] find definition: user.emacs("xref-find-definitions")
[xref] find definition other window: user.emacs("xref-find-definitions-other-window")
[xref] find definition other frame: user.emacs("xref-find-definitions-other-frame")
[xref] find references: user.emacs("xref-find-references")
[xref] find references [and] replace: user.emacs("xref-find-references-and-replace")
xref find apropos: user.emacs("xref-find-apropos")
xref go back: user.emacs("xref-go-back")
visit tags table: user.emacs("visit-tags-table")

# ----- PROJECT SUPPORT ----- #
project [find] file: user.emacs("project-find-file")
project [find] (regex | grep): user.emacs("project-find-regexp")
project [query] replace regex: user.emacs("project-query-replace-regexp")
project (dired | directory): user.emacs("projectile-dired")
project [run] shell: user.emacs("projectile-run-shell")
project [run] eshell: user.emacs("projectile-run-eshell")
project search: user.emacs("project-search")
project vc dir: user.emacs("project-vc-dir")
project compile [project]: user.emacs("projectile-compile-project")
project [run] shell command: user.emacs("projectile-run-shell-command-in-root")
project [run] async shell command:
    user.emacs("projectile-run-async-shell-command-in-root")
project (switch [to buffer] | buffer | buff): user.emacs("projectile-switch-to-buffer")
project kill [buffers]: user.emacs("projectile-kill-buffers")
project switch [project]: user.emacs("project-switch-project")

# ----- VC/GIT SUPPORT ----- #
vc (annotate | blame): user.emacs("vc-annotate")

# Magit support
magit status: user.emacs("magit-status")
git status: user.emacs("magit-status")

# ----- MAJOR & MINOR MODES ----- #
# python-mode #
python mode: user.emacs("python-mode")
run python: user.emacs("run-python")
python [shell] send buffer: user.emacs("python-shell-send-buffer")
python [shell] send file: user.emacs("python-shell-send-file")
python [shell] send region: user.emacs("python-shell-send-region")
python [shell] send (function | defun): user.emacs("python-shell-send-defun")
python [shell] send statement: user.emacs("python-shell-send-statement")
python (shell switch | switch [to] shell): user.emacs("python-shell-switch-to-shell")

# smerge-mode #
smerge mode: user.emacs("smerge-mode")
merge next: user.emacs("smerge-next")
merge last: user.emacs("smerge-prev")
merge keep upper: user.emacs("smerge-keep-upper")
merge keep lower: user.emacs("smerge-keep-lower")
merge keep base: user.emacs("smerge-keep-base")
merge keep (this | current): user.emacs("smerge-keep-current")
merge refine: user.emacs("smerge-refine")
merge split: user.emacs("smerge-resolve")

# outline-minor-mode #
# frequent: overview, show, hide, next, last, forward, backward, up
outline minor mode: user.emacs("outline-minor-mode")
outline show all: user.emacs("outline-show-all")
outline show entry: user.emacs("outline-show-entry")
outline hide entry: user.emacs("outline-hide-entry")
outline show [subtree]: user.emacs("outline-show-subtree")
outline hide [subtree]: user.emacs("outline-hide-subtree")
outline show children: user.emacs("outline-show-children")
outline show branches: user.emacs("outline-show-branches")
outline hide leaves: user.emacs("outline-hide-leaves")
outline hide sublevels: user.emacs("outline-hide-sublevels")
outline (hide body | [show] (overview | outline)): user.emacs("outline-hide-body")
outline hide other: user.emacs("outline-hide-other")
outline forward [same level]: user.emacs("outline-forward-same-level")
outline (backward | back) [same level]: user.emacs("outline-backward-same-level")
outline next [visible heading]: user.emacs("outline-next-visible-heading")
outline (previous | last) [visible heading]:
    user.emacs("outline-previous-visible-heading")
outline insert [heading]: user.emacs("outline-insert-heading")
outline up [heading]: user.emacs("outline-up-heading")
outline promote: user.emacs("outline-promote")
outline demote: user.emacs("outline-demote")
outline move [subtree] down: user.emacs("outline-move-subtree-down")
outline move [subtree] up: user.emacs("outline-move-subtree-up")
outline mark [subtree]: user.emacs("outline-mark-subtree")

# ----- WINDOW MOVEMENT (windmove) ----- #
(win | window) right: user.emacs("windmove-right")
(win | window) left: user.emacs("windmove-left")
(win | window) up: user.emacs("windmove-up")
(win | window) down: user.emacs("windmove-down")

# ----- AGENT SHELL (chat) COMMANDS ----- #
chat display buffer: user.emacs("agent-shell--display-buffer")
chat anthropic start claude code: user.emacs("agent-shell-anthropic-start-claude-code")
chat auggie start agent: user.emacs("agent-shell-auggie-start-agent")
chat clear buffer: user.emacs("agent-shell-clear-buffer")
chat cline start agent: user.emacs("agent-shell-cline-start-agent")
chat completion mode: user.emacs("agent-shell-completion-mode")
chat copy session id: user.emacs("agent-shell-copy-session-id")
chat cursor start agent: user.emacs("agent-shell-cursor-start-agent")
chat cycle session mode: user.emacs("agent-shell-cycle-session-mode")
chat delete interaction at point: user.emacs("agent-shell-delete-interaction-at-point")
chat diff accept all: user.emacs("agent-shell-diff-accept-all")
chat diff mode: user.emacs("agent-shell-diff-mode")
chat diff open file: user.emacs("agent-shell-diff-open-file")
chat diff reject all: user.emacs("agent-shell-diff-reject-all")
chat droid start agent: user.emacs("agent-shell-droid-start-agent")
chat fork: user.emacs("agent-shell-fork")
chat github start copilot: user.emacs("agent-shell-github-start-copilot")
chat google start gemini: user.emacs("agent-shell-google-start-gemini")
chat goose start agent: user.emacs("agent-shell-goose-start-agent")
chat help menu: user.emacs("agent-shell-help-menu")
chat insert file: user.emacs("agent-shell-insert-file")
chat insert shell command output: user.emacs("agent-shell-insert-shell-command-output")
chat interrupt: user.emacs("agent-shell-interrupt")
chat jump to latest permission button row:
    user.emacs("agent-shell-jump-to-latest-permission-button-row")
chat kiro start agent: user.emacs("agent-shell-kiro-start-agent")
chat mistral start vibe: user.emacs("agent-shell-mistral-start-vibe")
chat mode: user.emacs("agent-shell-mode")
chat new downloads shell: user.emacs("agent-shell-new-downloads-shell")
chat new shell: user.emacs("agent-shell-new-shell")
chat new temp shell: user.emacs("agent-shell-new-temp-shell")
chat new worktree shell: user.emacs("agent-shell-new-worktree-shell")
chat newline: user.emacs("agent-shell-newline")
chat next input: user.emacs("agent-shell-next-input")
chat next item: user.emacs("agent-shell-next-item")
chat next permission button: user.emacs("agent-shell-next-permission-button")
chat open transcript: user.emacs("agent-shell-open-transcript")
chat openai start codex: user.emacs("agent-shell-openai-start-codex")
chat opencode start agent: user.emacs("agent-shell-opencode-start-agent")
chat other buffer: user.emacs("agent-shell-other-buffer")
chat pi start agent: user.emacs("agent-shell-pi-start-agent")
chat previous input: user.emacs("agent-shell-previous-input")
chat previous item: user.emacs("agent-shell-previous-item")
chat previous permission button: user.emacs("agent-shell-previous-permission-button")
chat prompt compose: user.emacs("agent-shell-prompt-compose")
chat queue request: user.emacs("agent-shell-queue-request")
chat qwen start: user.emacs("agent-shell-qwen-start")
chat reload: user.emacs("agent-shell-reload")
chat remove pending request: user.emacs("agent-shell-remove-pending-request")
chat rename buffer: user.emacs("agent-shell-rename-buffer")
chat reset logs: user.emacs("agent-shell-reset-logs")
chat restart: user.emacs("agent-shell-restart")
chat resume pending requests: user.emacs("agent-shell-resume-pending-requests")
chat resume session: user.emacs("agent-shell-resume-session")
chat search history: user.emacs("agent-shell-search-history")
chat send clipboard image: user.emacs("agent-shell-send-clipboard-image")
chat send clipboard image to: user.emacs("agent-shell-send-clipboard-image-to")
chat send current file: user.emacs("agent-shell-send-current-file")
chat send dwim: user.emacs("agent-shell-send-dwim")
chat send file: user.emacs("agent-shell-send-file")
chat send file to: user.emacs("agent-shell-send-file-to")
chat send other file: user.emacs("agent-shell-send-other-file")
chat send region: user.emacs("agent-shell-send-region")
chat send region to: user.emacs("agent-shell-send-region-to")
chat send screenshot: user.emacs("agent-shell-send-screenshot")
chat send screenshot to: user.emacs("agent-shell-send-screenshot-to")
chat set session mode: user.emacs("agent-shell-set-session-mode")
chat set session model: user.emacs("agent-shell-set-session-model")
chat show usage: user.emacs("agent-shell-show-usage")
chat submit: user.emacs("agent-shell-submit")
chat toggle: user.emacs("agent-shell-toggle")
chat toggle logging: user.emacs("agent-shell-toggle-logging")
chat UI backward block: user.emacs("agent-shell-ui-backward-block")
chat UI forward block: user.emacs("agent-shell-ui-forward-block")
chat UI mode: user.emacs("agent-shell-ui-mode")
chat UI toggle fragment at point: user.emacs("agent-shell-ui-toggle-fragment-at-point")
chat version: user.emacs("agent-shell-version")
chat view ACP logs: user.emacs("agent-shell-view-acp-logs")
chat view traffic: user.emacs("agent-shell-view-traffic")
chat viewport compose cancel: user.emacs("agent-shell-viewport-compose-cancel")
chat viewport compose help menu: user.emacs("agent-shell-viewport-compose-help-menu")
chat viewport compose peek last: user.emacs("agent-shell-viewport-compose-peek-last")
chat viewport compose send: user.emacs("agent-shell-viewport-compose-send")
chat viewport compose send and kill:
    user.emacs("agent-shell-viewport-compose-send-and-kill")
chat viewport compose send and wait for response:
    user.emacs("agent-shell-viewport-compose-send-and-wait-for-response")
chat viewport copy session id: user.emacs("agent-shell-viewport-copy-session-id")
chat viewport cycle session mode: user.emacs("agent-shell-viewport-cycle-session-mode")
chat viewport edit mode: user.emacs("agent-shell-viewport-edit-mode")
chat viewport help menu: user.emacs("agent-shell-viewport-help-menu")
chat viewport interrupt: user.emacs("agent-shell-viewport-interrupt")
chat viewport next history: user.emacs("agent-shell-viewport-next-history")
chat viewport next item: user.emacs("agent-shell-viewport-next-item")
chat viewport next page: user.emacs("agent-shell-viewport-next-page")
chat viewport open transcript: user.emacs("agent-shell-viewport-open-transcript")
chat viewport previous history: user.emacs("agent-shell-viewport-previous-history")
chat viewport previous item: user.emacs("agent-shell-viewport-previous-item")
chat viewport previous page: user.emacs("agent-shell-viewport-previous-page")
chat viewport queue request: user.emacs("agent-shell-viewport-queue-request")
chat viewport refresh: user.emacs("agent-shell-viewport-refresh")
chat viewport remove pending request:
    user.emacs("agent-shell-viewport-remove-pending-request")
chat viewport reply: user.emacs("agent-shell-viewport-reply")
chat viewport reply 1: user.emacs("agent-shell-viewport-reply-1")
chat viewport reply 2: user.emacs("agent-shell-viewport-reply-2")
chat viewport reply 3: user.emacs("agent-shell-viewport-reply-3")
chat viewport reply 4: user.emacs("agent-shell-viewport-reply-4")
chat viewport reply 5: user.emacs("agent-shell-viewport-reply-5")
chat viewport reply 6: user.emacs("agent-shell-viewport-reply-6")
chat viewport reply 7: user.emacs("agent-shell-viewport-reply-7")
chat viewport reply 8: user.emacs("agent-shell-viewport-reply-8")
chat viewport reply 9: user.emacs("agent-shell-viewport-reply-9")
chat viewport reply again: user.emacs("agent-shell-viewport-reply-again")
chat viewport reply continue: user.emacs("agent-shell-viewport-reply-continue")
chat viewport reply more: user.emacs("agent-shell-viewport-reply-more")
chat viewport reply yes: user.emacs("agent-shell-viewport-reply-yes")
chat viewport resume pending requests:
    user.emacs("agent-shell-viewport-resume-pending-requests")
chat viewport search history: user.emacs("agent-shell-viewport-search-history")
chat viewport set session mode: user.emacs("agent-shell-viewport-set-session-mode")
chat viewport set session model: user.emacs("agent-shell-viewport-set-session-model")
chat viewport view ACP logs: user.emacs("agent-shell-viewport-view-acp-logs")
chat viewport view last: user.emacs("agent-shell-viewport-view-last")
chat viewport view mode: user.emacs("agent-shell-viewport-view-mode")
chat viewport view traffic: user.emacs("agent-shell-viewport-view-traffic")
chat yank dwim: user.emacs("agent-shell-yank-dwim")

# =====================================
# Hunt
# =====================================

private config hunt [<user.text>]:
    user.emacs("doom/find-file-in-private-config")
    sleep(50ms)
    insert(text or "")

# =====================================
# Tabs
# =====================================

tab new: user.emacs("tab-bar-new-tab")
tab close: user.emacs("tab-bar-close-tab")
tab next: user.emacs("tab-bar-switch-to-next-tab")
tab last: user.emacs("tab-bar-switch-to-prev-tab")
tab list: user.emacs("tab-list")
tab rename: user.emacs("tab-bar-rename-tab")
tab move left: user.emacs("tab-bar-move-tab-backward")
tab move right: user.emacs("tab-bar-move-tab")
tab switch <number_small>: user.emacs("tab-bar-select-tab", number_small)
