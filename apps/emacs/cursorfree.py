from talon import Context, Module
import talon, subprocess, json, threading

module = Module()

@module.capture(rule="[{user.phony_cursorfree_colors}] [{user.phony_cursorfree_shapes}] <user.any_alphanumeric_key>")
def cursorfree_hat(m) -> list[str]:
    color = m.phony_cursorfree_colors if hasattr(m, "phony_cursorfree_colors") else "nil"
    shape = m.phony_cursorfree_shapes if hasattr(m, "phony_cursorfree_shapes") else "nil"

    escape = {"\\": "\\\\",
              "(": "\\(",
              ")": "\\)",
              "[": "\\[",
              "]": "\\]"}
    character = escape.get(m.any_alphanumeric_key, m.any_alphanumeric_key)
    return f"(cursorfree--pusher (cursorfree--make-target-from-hat ?{character} {color} {shape}))"

@module.capture(rule="car <user.any_alphanumeric_key>")
def cursorfree_quoted_char(m) -> list[str]:
    return f"(cursorfree--pusher ?{m.any_alphanumeric_key})"

@module.capture(rule="numb <number>")
def cursorfree_quoted_number(m) -> list[str]:
    return f"(cursorfree--pusher {m.number})"

@module.capture(rule="word <word>")
def cursorfree_quoted_word(m) -> list[str]:
    return f"(cursorfree--pusher \"{m.word}\")"

@module.capture(rule=
                "{user.phony_cursorfree_modifiers}"
                "| <user.cursorfree_hat>"
                "| <user.cursorfree_quoted_char>"
                "| <user.cursorfree_quoted_number>"
                "| <user.cursorfree_quoted_word>"
                )
def cursorfree_nonterminator(m) -> list[str]:
    return m[0]

@module.capture(rule=
                "<user.cursorfree_nonterminator>+"
                )
def cursorfree_nonterminators(m) -> list[str]:
    return " ".join(m.cursorfree_nonterminator_list)

@module.capture(rule=
                "<user.cursorfree_nonterminators> "
                "{user.phony_cursorfree_actions}")
def cursorfree_command(m) -> list[str]:
    return f"(list {m.cursorfree_nonterminators} {m.phony_cursorfree_actions})";