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

# You can add other ChatGPT-specific voice commands here
