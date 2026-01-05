app: libreoffice
-
# Implementation of LibreOffice-specific actions
action(user.libreoffice_next_paragraph):
    key(ctrl-down)

action(user.libreoffice_previous_paragraph):
    key(ctrl-up)

action(user.libreoffice_select_paragraph):
    # Triple-click selects paragraph in LibreOffice
    mouse_click(0)
    mouse_click(0)
    mouse_click(0)

action(user.libreoffice_next_sentence):
    # Move to end of sentence (period + space)
    key(ctrl-f)
    insert(". ")
    key(enter)
    key(escape)

action(user.libreoffice_previous_sentence):
    # Move to start of previous sentence
    key(ctrl-f)
    insert(". ")
    key(shift-enter)
    key(escape)
    key(left left)

action(user.libreoffice_select_sentence):
    # Select from cursor to next period
    key(shift-ctrl-f)
    insert(".")
    key(enter)
    key(escape)

action(user.libreoffice_select_word):
    # Double-click selects word in LibreOffice
    mouse_click(0)
    mouse_click(0)

action(user.libreoffice_start_of_document):
    key(ctrl-home)

action(user.libreoffice_end_of_document):
    key(ctrl-end)

action(user.libreoffice_select_to_start):
    key(ctrl-shift-home)

action(user.libreoffice_select_to_end):
    key(ctrl-shift-end)
