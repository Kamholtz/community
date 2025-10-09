tag: terminal
and tag: user.zoxide
-

jump <user.text>:
    insert("z ")
    insert(user.text or "")
    key(enter)

jump $:
    insert("z ")
