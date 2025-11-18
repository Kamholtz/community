app: emacs
-

# Action-first grammar (Cursorless-compatible)
<user.cursorfree_command>:
    user.phony_evaluate_emacs_lisp("(cursorfree-execute-ir {cursorfree_command})")
