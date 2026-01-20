code.language: go
-

tag(): user.code_imperative

tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_comment_documentation
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_keywords
tag(): user.code_libraries
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math
tag(): user.code_operators_pointer

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_public_variable_formatter = "PRIVATE_CAMEL_CASE"

(variadic | spread): "..."
declare: " := "
channel (receive | send): " <- "

[state] if (err | error):
    insert("if err != nil {")
    key("enter")

[state] if not (err | error):
    insert("if err == nil {")
    key("enter")

import <user.code_libraries>:
    user.code_insert_library(code_libraries, "")
    key(end enter)

dock string: user.code_comment_documentation()

state (package | pack age) <user.text>:
    insert("package ")
    insert(user.formatted_text(text, "ALL_LOWERCASE"))

state (struct | structure) <user.text>:
    name = user.formatted_text(text, "PUBLIC_CAMEL_CASE")
    insert("type ")
    insert(name)
    user.insert_between(" struct {\n\t", "\n}")

state (interface | interface type) <user.text>:
    name = user.formatted_text(text, "PUBLIC_CAMEL_CASE")
    insert("type ")
    insert(name)
    user.insert_between(" interface {\n\t", "\n}")

state (type alias | alias type) <user.text> (for | of) <user.code_type>:
    name = user.formatted_text(text, "PUBLIC_CAMEL_CASE")
    insert("type ")
    insert(name)
    insert(" ")
    insert(code_type)

state (defer | defers): "defer "

state (go | goroutine | go routine): "go "

state select: user.insert_between("select {\n\t", "\n}")

state panic: user.insert_between("panic(", ")")

state recover: user.insert_between("recover(", ")")
