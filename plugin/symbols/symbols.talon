new line: "\n"
double dash: "--"
triple quote: "'''"
triple grave | triple back tick | gravy: "```"
(dot dot | dotdot): ".."
ellipsis: "..."
(comma and | spamma): ", "
arrow: "->"
dub arrow: "=>"

# Insert delimiter pairs
<user.delimiter_pair>: user.delimiter_pair_insert(delimiter_pair)

# Wrap selection with delimiter pairs
<user.delimiter_pair> that: user.delimiter_pair_wrap_selection(delimiter_pair)

new line: "\n"
# double dash: "--"
# triple quote: "'''"
pebbles: "..."
# Add symbol at end of line and then insert line below
# From https://github.com/AndreasArvidsson/andreas-talon/blob/master/misc/keys/keys.talon#L28
patch {user.symbol_key}:
    edit.line_end()
    "{symbol_key}"
    edit.line_insert_down()
spam: ", "
pipe gap | wide pipe: " | "
big stack: ": "
boom|boomer: ". "
arrow: "->"
dub arrow: "=>"
empty round: "()"
empty square: "[]"
empty curly: "{}"
empty diamond: "<>"
empty quad: '""'
empty twin: "''"
empty escaped quad: '\\"\\"'
empty escaped twin: "\\'\\'"
empty escaped round: "\\(\\)"
empty escaped curly: "\\{{\\}}"
tween <user.symbol_key>: user.insert_between("{symbol_key}", "{symbol_key}")
quad: user.insert_between('"', '"')
twin: user.insert_between("'", "'")
ski: user.insert_between("`", "`")
escaped quad: user.insert_between('\\"', '\\"')
escaped twin: user.insert_between("\\'", "\\'")
round: user.insert_between("(", ")")
escaped round: user.insert_between("\\(", "\\)")
escaped curly: user.insert_between("\\{{", "\\}}")
square: user.insert_between("[", "]")
curly: user.insert_between("{", "}")
diamond: user.insert_between("<", ">")
(diamond | angle) that:
    text = edit.selected_text()
    user.paste("<{text}>")
(curly | lace) that:
    text = edit.selected_text()
    user.paste("{{{text}}}")
(round | leper) that:
    text = edit.selected_text()
    user.paste("({text})")
(double | quad) that:
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dub quote) that:
    text = edit.selected_text()
    user.paste('"{text}"')
(single | twin) that:
    text = edit.selected_text()
    user.paste("'{text}'")

big round:
    insert("()")
    key(left enter)
big square:
    insert("[]")
    key(left enter)
big curly:
    insert("{}")
    key(left enter)

slicer:
    edit.line_end()
    key(enter)
    insert("- ")

end gap:
    edit.line_end()
    key(space)

slider:
    edit.line_end()
    insert(",")
    key(enter)

breaker:
    edit.line_end()
    insert(" {")
    key(enter)

chronic:
    edit.line_end()
    insert(":")
    key(enter)