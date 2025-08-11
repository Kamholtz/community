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

# Quick Analysis Commands
summarize paste enter:
    insert("Summarize this in 3 bullet points: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

translate paste enter:
    insert("Translate this to English: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

debug paste enter:
    insert("Find and explain any bugs in this code: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

# Code-Specific Commands
refactor paste enter:
    insert("Refactor this code to be cleaner and more efficient: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

comment paste enter:
    insert("Add clear comments to this code: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

test paste enter:
    insert("Write unit tests for this code: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

# Writing Commands
proofread paste enter:
    insert("Proofread this text for grammar and clarity: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

simplify paste enter:
    insert("Rewrite this in simpler terms: ")
    key(shift-enter)
    key(shift-enter)
    edit.paste()
    key(enter)

# Quick Actions
continue chat:
    insert("Please continue")
    key(enter)

try again:
    insert("Try again with a different approach")
    key(enter)

be more specific:
    insert("Can you be more specific?")
    key(enter)
