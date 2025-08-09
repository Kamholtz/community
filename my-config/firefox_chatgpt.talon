app: firefox_chatgpt
-

greet:
    insert("Hello, ChatGPT!")

explain paste enter:
    insert("Concisely explain the following: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

improve paste enter:
    insert("Fact check the following and provide concise improvements: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

custom paste enter [<user.text>]:
    insert(user.text or "")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

# You can add other ChatGPT-specific voice commands here
