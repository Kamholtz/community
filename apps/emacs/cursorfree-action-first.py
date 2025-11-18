"""Cursorfree action-first grammar for Cursorless compatibility.

This module implements the action-first grammar:
    <action> [<modifiers>] <target>
    
Examples:
    "chuck gust"              -> chuck (action) + gust (hat target)
    "chuck line gust"         -> chuck + line (modifier) + gust
    "chuck inside line gust"  -> chuck + inside + line + gust
    "bring gust to bat"       -> bring + gust (source) + bat (destination)
    "chuck gust and bat"      -> chuck + list(gust, bat)
"""

from talon import Context, Module

module = Module()

# ============================================================================
# Target captures (no modifiers yet)
# ============================================================================

@module.capture(rule="[{user.phony_cursorfree_colors}] [{user.phony_cursorfree_shapes}] <user.any_alphanumeric_key>")
def cursorfree_target_hat_raw(m) -> str:
    """Hat target: [color] [shape] letter -> IR structure."""
    color = f"'{m.phony_cursorfree_colors}" if hasattr(m, "phony_cursorfree_colors") else "nil"
    shape = f"'{m.phony_cursorfree_shapes}" if hasattr(m, "phony_cursorfree_shapes") else "nil"
    
    # Escape special elisp characters
    escape = {"\\": "\\\\", "(": "\\(", ")": "\\)", "[": "\\[", "]": "\\]"}
    character = escape.get(m.any_alphanumeric_key, m.any_alphanumeric_key)
    
    return f"(cursorfree-ir-make-hat-target :character ?{character} :color {color} :shape {shape})"

@module.capture(rule="car <user.any_alphanumeric_key>")
def cursorfree_target_literal_char(m) -> str:
    """Literal character: car X -> character."""
    return f"(cursorfree-ir-make-literal-target ?{m.any_alphanumeric_key})"

@module.capture(rule="numb <number>")
def cursorfree_target_literal_number(m) -> str:
    """Literal number: numb 42 -> number."""
    return f"(cursorfree-ir-make-literal-target {m.number})"

@module.capture(rule="word <word>")
def cursorfree_target_literal_word(m) -> str:
    """Literal word: word foo -> string."""
    return f'(cursorfree-ir-make-literal-target "{m.word}")'

@module.capture(rule="selection")
def cursorfree_target_selection(m) -> str:
    """Selection target: current selection."""
    return "(cursorfree-ir-make-selection-target)"

@module.capture(rule=
                "<user.cursorfree_target_hat_raw>"
                "| <user.cursorfree_target_literal_char>"
                "| <user.cursorfree_target_literal_number>"
                "| <user.cursorfree_target_literal_word>"
                "| <user.cursorfree_target_selection>"
                )
def cursorfree_target_atomic(m) -> str:
    """Atomic target without modifiers or connectors."""
    return m[0]

# ============================================================================
# Target connectors (and, through, past)
# ============================================================================

@module.capture(rule="<user.cursorfree_target_atomic> and <user.cursorfree_target_composite>")
def cursorfree_target_list(m) -> str:
    """List target: target and target [and target ...]"""
    # If second target is already a list, append to it
    # Otherwise create new list with both targets
    return f"(cursorfree-ir-make-list-target (cons {m.cursorfree_target_atomic} (if (eq :list (cursorfree-ir-target-type {m.cursorfree_target_composite})) (cursorfree-ir-target-value {m.cursorfree_target_composite}) (list {m.cursorfree_target_composite}))))"

@module.capture(rule="<user.cursorfree_target_atomic> (through | past) <user.cursorfree_target_atomic>")
def cursorfree_target_range(m) -> str:
    """Range target: target through/past target."""
    connector = "past" if m[1] == "past" else "through"
    return f"(cursorfree-ir-make-range-target {m.cursorfree_target_atomic_1} {m.cursorfree_target_atomic_2} :connector :{connector})"

@module.capture(rule=
                "<user.cursorfree_target_list>"
                "| <user.cursorfree_target_range>"
                "| <user.cursorfree_target_atomic>"
                )
def cursorfree_target_composite(m) -> str:
    """Target that may include connectors (and/through/past)."""
    return m[0]

# ============================================================================
# Modifiers + Targets
# ============================================================================

@module.capture(rule="{user.phony_cursorfree_modifiers}+ <user.cursorfree_target_composite>")
def cursorfree_target_with_modifiers(m) -> str:
    """Target with modifiers: modifier+ target."""
    # Build modifier list: '("modifier1" "modifier2" ...)
    modifiers = " ".join(f'"{mod}"' for mod in m.phony_cursorfree_modifiers_list)
    return f"(cursorfree-ir-target-add-modifiers {m.cursorfree_target_composite} '({modifiers}))"

@module.capture(rule=
                "<user.cursorfree_target_with_modifiers>"
                "| <user.cursorfree_target_composite>"
                )
def cursorfree_target(m) -> str:
    """Any target, with or without modifiers."""
    return m[0]

# ============================================================================
# Commands
# ============================================================================

@module.capture(rule="{user.phony_cursorfree_actions} <user.cursorfree_target>")
def cursorfree_command_simple(m) -> str:
    """Simple action-first command: action target."""
    return f'(cursorfree-ir-make-command :action "{m.phony_cursorfree_actions}" :targets (list {m.cursorfree_target}))'

@module.capture(rule="{user.phony_cursorfree_actions} <user.cursorfree_target> to <user.cursorfree_target>")
def cursorfree_command_bring(m) -> str:
    """Bring/move command: action source to destination."""
    return f'(cursorfree-ir-make-command :action "{m.phony_cursorfree_actions}" :targets (list {m.cursorfree_target_1}) :destination {m.cursorfree_target_2})'

@module.capture(rule="{user.phony_cursorfree_actions} <user.cursorfree_target> <user.cursorfree_target>")
def cursorfree_command_swap(m) -> str:
    """Swap command: action target1 target2."""
    return f'(cursorfree-ir-make-command :action "{m.phony_cursorfree_actions}" :targets (list {m.cursorfree_target_1} {m.cursorfree_target_2}))'

@module.capture(rule=
                "<user.cursorfree_command_bring>"
                "| <user.cursorfree_command_swap>"
                "| <user.cursorfree_command_simple>"
                )
def cursorfree_command(m) -> str:
    """Any cursorfree command in action-first grammar."""
    return m[0]
