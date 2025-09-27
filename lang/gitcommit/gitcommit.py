from talon import Context, Module, actions

mod = Module()
ctx = Context()

fallback_ctx = Context()
fallback_ctx.matches = r"""
app: vscode
and win.title: /^COMMIT_EDITMSG\b/
and win.title: /focus:\[Text Editor\]/
"""


@fallback_ctx.action_class("code")
class FallbackCodeActions:
    def language():
        return "gitcommit"

ctx.matches = r"""
code.language: gitcommit
"""

ctx.lists["user.code_common_function"] = {
    "add": "add",
    "fix": "fix",
    "update": "update",
    "remove": "remove",
    "refactor": "refactor",
    "docs": "docs",
    "style": "style",
    "test": "test",
    "chore": "chore",
    "feat": "feat",
    "perf": "perf",
    "revert": "revert",
}

# Git commit message keywords and prefixes
ctx.lists["user.code_keyword"] = {
    "add": "add ",
    "fix": "fix ",
    "update": "update ",
    "remove": "remove ",
    "delete": "delete ",
    "refactor": "refactor ",
    "docs": "docs ",
    "style": "style ",
    "test": "test ",
    "chore": "chore ",
    "feature": "feat ",
    "performance": "perf ",
    "revert": "revert ",
    "breaking": "BREAKING CHANGE: ",
    "closes": "closes ",
    "fixes": "fixes ",
    "resolves": "resolves ",
}

# Common git commit actions
@ctx.action_class("user")
class UserActions:
    def code_insert_function(text: str, selection: str):
        # For git commits, just insert the text
        actions.insert(text)

    def code_insert_comment_line():
        actions.auto_insert("# ")

    def code_toggle_comment():
        actions.edit.line_start()
        actions.insert("# ")
