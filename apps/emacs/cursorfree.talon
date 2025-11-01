app: emacs
-

<user.cursorfree_command>:
    user.phony_evaluate_emacs_lisp("(with-selected-window {window} (cursorfree-evaluate {cursorfree_command}))")
