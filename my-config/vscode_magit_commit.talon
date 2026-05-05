app: vscode
code.language: gitcommit
-

commit finish: user.vscode("magit.save-and-close-editor")
commit done: user.vscode("magit.save-and-close-editor")
commit abort: user.vscode("magit.clear-and-abort-editor")
commit cancel: user.vscode("magit.clear-and-abort-editor")

commit body: key(end enter enter)

commit feature [<user.text>]:
    insert("feat: ")
    insert(text or "")

commit fix [<user.text>]:
    insert("fix: ")
    insert(text or "")

commit refactor [<user.text>]:
    insert("refactor: ")
    insert(text or "")

commit format [<user.text>]:
    insert("format: ")
    insert(text or "")

commit docs [<user.text>]:
    insert("docs: ")
    insert(text or "")

commit test [<user.text>]:
    insert("test: ")
    insert(text or "")

commit chore [<user.text>]:
    insert("chore: ")
    insert(text or "")

commit work in progress [<user.text>]:
    insert("wip: ")
    insert(text or "")
