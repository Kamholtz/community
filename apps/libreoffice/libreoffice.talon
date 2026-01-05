app: libreoffice
-
# Navigation commands
(go | jump) next paragraph: user.libreoffice_next_paragraph()
(go | jump) (previous | last) paragraph: user.libreoffice_previous_paragraph()
(go | jump) paragraph <number>:
    user.libreoffice_start_of_document()
    repeat(number - 1)
        user.libreoffice_next_paragraph()

(go | jump) next sentence: user.libreoffice_next_sentence()
(go | jump) (previous | last) sentence: user.libreoffice_previous_sentence()

(go | jump) start [of] document: user.libreoffice_start_of_document()
(go | jump) end [of] document: user.libreoffice_end_of_document()

# Selection commands
select paragraph: user.libreoffice_select_paragraph()
select sentence: user.libreoffice_select_sentence()
select word: user.libreoffice_select_word()

select to start: user.libreoffice_select_to_start()
select to end: user.libreoffice_select_to_end()

# Standard keyboard shortcuts for navigation
(go | jump) line up: key(up)
(go | jump) line down: key(down)
(go | jump) word left: key(ctrl-left)
(go | jump) word right: key(ctrl-right)
(go | jump) line start: key(home)
(go | jump) line end: key(end)

# Selection shortcuts
select line up: key(shift-up)
select line down: key(shift-down)
select word left: key(ctrl-shift-left)
select word right: key(ctrl-shift-right)
select line: key(home shift-end)
select cycle: key(f8)

# Formatting commands
format bold: key(ctrl-b)
format italic: key(ctrl-i)
format underline: key(ctrl-u)
format double underline: key(ctrl-d)
format strikethrough: key(alt-shift-5)
format superscript: key(ctrl-shift-p)
format subscript: key(ctrl-shift-b)
format clear: key(ctrl-m)

# Text alignment
align left: key(ctrl-l)
align center: key(ctrl-e)
align right: key(ctrl-r)
align justify: key(ctrl-j)

# Paragraph styles
style body: key(ctrl-0)
style heading one: key(ctrl-1)
style heading two: key(ctrl-2)
style heading three: key(ctrl-3)
style heading four: key(ctrl-4)
style heading five: key(ctrl-5)

# Special characters and breaks
insert soft hyphen: key(ctrl--)
insert non breaking hyphen: key(ctrl-shift--)
insert non breaking space: key(ctrl-shift-space)
insert line break: key(shift-enter)
insert page break: key(ctrl-enter)

# List management
toggle ordered list: key(f12)
toggle bullet list: key(shift-f12)
toggle unordered list: key(shift-f12)
increase indent: key(tab)
decrease indent: key(shift-tab)

# Table operations
insert table: key(ctrl-f12)
edit table: key(ctrl-f12)

# Find and replace
find: key(ctrl-f)
find next: key(ctrl-g)
find previous: key(ctrl-shift-g)
find replace: key(ctrl-h)

# Spelling and language
check spelling: key(f7)
open thesaurus: key(ctrl-f7)

# Field operations
show formula bar: key(f2)
insert field: key(ctrl-f2)
update fields: key(f9)
show field contents: key(ctrl-f9)

# View and navigation
toggle navigator: key(f5)
next suggestion: key(ctrl-tab)
previous suggestion: key(ctrl-shift-tab)

# Standard editing
undo: key(ctrl-z)
redo: key(ctrl-y)
cut: key(ctrl-x)
copy: key(ctrl-c)
paste: key(ctrl-v)
paste special: key(ctrl-shift-v)
select all: key(ctrl-a)

# Document operations
new document: key(ctrl-n)
open document: key(ctrl-o)
save document: key(ctrl-s)
save as: key(ctrl-shift-s)
print: key(ctrl-p)
close document: key(ctrl-w)
