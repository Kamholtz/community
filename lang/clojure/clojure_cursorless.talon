code.language: clojure
tag: user.cursorless
-

# file
eval file: user.vscode("calva.loadFile")
eval to cursor: user.vscode("calva.evaluateStartOfFileToCursor")

# form
eval form: user.vscode("calva.evaluateEnclosingForm")
eval (top|top form) down: user.vscode("calva.evaluateTopLevelFormToCursor")
eval (top|top form): user.vscode("calva.evaluateCurrentTopLevelForm")
eval (top|top form) as comment: user.vscode("calva.evaluateTopLevelFormAsComment")

# selection
eval selection: user.vscode("calva.evaluateSelection")
eval selection as comment: user.vscode("calva.evaluateSelectionAsComment")

# interrupt
interrupt eval: user.vscode("calva.interruptAllEvaluations")

# repl
repl show: user.vscode("calva.showReplOutputView")

repl kill: user.vscode("calva.jackOut")
repl connect: user.vscode("calva.connect")