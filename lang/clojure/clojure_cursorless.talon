code.language: clojure
tag: user.cursorless
-

# file
(eval | evaluate) current: user.vscode("calva.evaluateSelection")
(eval | evaluate) file: user.vscode("calva.loadFile")
(eval | evaluate) to cursor: user.vscode("calva.evaluateStartOfFileToCursor")

# form
(eval | evaluate) form: user.vscode("calva.evaluateEnclosingForm")
(eval | evaluate) (top | top form) down: user.vscode("calva.evaluateTopLevelFormToCursor")
(eval | evaluate) (top | top form): user.vscode("calva.evaluateCurrentTopLevelForm")
(eval | evaluate) (top | top form) as comment: user.vscode("calva.evaluateTopLevelFormAsComment")

# selection
eval selection: user.vscode("calva.evaluateSelection")
eval selection as comment: user.vscode("calva.evaluateSelectionAsComment")

# raise
raise form: user.vscode("paredit.raiseSexp")

# interrupt
interrupt eval: user.vscode("calva.interruptAllEvaluations")

# repl
repl show: user.vscode("calva.showReplOutputView")

repl kill: user.vscode("calva.jackOut")
repl connect: user.vscode("calva.connect")
