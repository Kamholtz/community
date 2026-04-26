from contextlib import suppress

from talon import Context, Module, actions, settings

from ...core.described_functions import create_described_insert_between
from ..tags.operators import Operators

ctx = Context()
mod = Module()
ctx.matches = r"""
code.language: go
"""

ctx.lists["user.code_type"] = {
    "any": "any",
    "boolean": "bool",
    "bool": "bool",
    "byte": "byte",
    "byte slice": "[]byte",
    "complex sixty four": "complex64",
    "complex one twenty eight": "complex128",
    "error": "error",
    "float": "float64",
    "float thirty two": "float32",
    "float sixty four": "float64",
    "int": "int",
    "int eight": "int8",
    "int sixteen": "int16",
    "int thirty two": "int32",
    "int sixty four": "int64",
    "integer": "int",
    "interface": "interface{}",
    "rune": "rune",
    "string": "string",
    "string slice": "[]string",
    "uint": "uint",
    "uint eight": "uint8",
    "uint sixteen": "uint16",
    "uint thirty two": "uint32",
    "uint sixty four": "uint64",
}

ctx.lists["user.code_keyword"] = {
    "break": "break",
    "case": "case ",
    "chan": "chan ",
    "const": "const ",
    "continue": "continue",
    "default": "default",
    "defer": "defer ",
    "else": "else ",
    "fallthrough": "fallthrough",
    "for": "for ",
    "func": "func ",
    "go": "go ",
    "goto": "goto ",
    "if": "if ",
    "import": "import ",
    "interface": "interface ",
    "map": "map ",
    "package": "package ",
    "range": "range ",
    "return": "return ",
    "select": "select ",
    "struct": "struct ",
    "switch": "switch ",
    "type": "type ",
    "var": "var ",
}

ctx.lists["user.code_libraries"] = {
    "archive tar": "archive/tar",
    "archive zip": "archive/zip",
    "bufio": "bufio",
    "bytes": "bytes",
    "context": "context",
    "crypto": "crypto",
    "crypto aes": "crypto/aes",
    "crypto hmac": "crypto/hmac",
    "database sql": "database/sql",
    "encoding base64": "encoding/base64",
    "encoding json": "encoding/json",
    "errors": "errors",
    "fmt": "fmt",
    "html template": "html/template",
    "io": "io",
    "io utilities": "io/ioutil",
    "log": "log",
    "math": "math",
    "math rand": "math/rand",
    "net": "net",
    "net http": "net/http",
    "net http httptest": "net/http/httptest",
    "net url": "net/url",
    "os": "os",
    "path": "path",
    "path filepath": "path/filepath",
    "runtime": "runtime",
    "sort": "sort",
    "strconv": "strconv",
    "strings": "strings",
    "sync": "sync",
    "sync atomic": "sync/atomic",
    "testing": "testing",
    "text template": "text/template",
    "time": "time",
}

operators = Operators(
    # code_operators_array
    SUBSCRIPT=create_described_insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_INCREMENT="++",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_lambda
    LAMBDA=" func() ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_OR=" || ",
    MATH_AND=" && ",
    MATH_EXPONENT=" ^ ",
    MATH_GREATER_THAN=" > ",
    MATH_LESS_THAN=" < ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    # code_operators_pointer
    POINTER_ADDRESS_OF="&",
    POINTER_INDIRECTION="*",
)

mod.list("float_type_bit_width", desc="Float type bit widths")
mod.list("complex_type_bit_width", desc="Complex type bit widths")


@mod.capture(rule="[{user.stdint_signed}] int {user.c_type_bit_width}")
def go_int_type(m) -> str:
    """fixed-width integer types (e.g. "uint32")"""
    prefix = ""
    with suppress(AttributeError):
        prefix = m.stdint_signed
    return f"{prefix}int{m.c_type_bit_width}"


@mod.capture(rule="float {user.float_type_bit_width}")
def go_float_type(m) -> str:
    """fixed-width float types (e.g. "float32")"""
    return f"float{m.float_type_bit_width}"


@mod.capture(rule="complex {user.complex_type_bit_width}")
def go_complex_type(m) -> str:
    """fixed-width complex types (e.g. "complex64")"""
    return f"complex{m.complex_type_bit_width}"


@ctx.capture(
    "user.code_type",
    rule="{user.code_type} | <user.go_int_type> | <user.go_float_type> | <user.go_complex_type>",
)
def code_type(m) -> str:
    """All go types"""
    return "".join(list(m))


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.insert("this")

    def code_operator_object_accessor():
        actions.insert(".")

    def code_insert_null():
        actions.insert("nil")

    def code_insert_is_null():
        actions.insert(" == nil")

    def code_insert_is_not_null():
        actions.insert(" != nil")

    def code_insert_true():
        actions.insert("true")

    def code_insert_false():
        actions.insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""
        formatter = settings.get("user.code_private_function_formatter")
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(f"func {function_name}", None)

        actions.user.code_insert_function(result, None)

    def code_private_static_function(text: str):
        actions.user.code_private_function(text)

    def code_protected_function(text: str):
        """Go does not have protected visibility; treat it as exported."""
        actions.user.code_public_function(text)

    def code_protected_static_function(text: str):
        actions.user.code_protected_function(text)

    def code_public_function(text: str):
        formatter = settings.get("user.code_public_function_formatter")
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(f"func {function_name}", None)

    def code_public_static_function(text: str):
        actions.user.code_public_function(text)

    def code_insert_type_annotation(type: str):
        actions.insert(f" {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" {type}")

    def code_insert_library(text: str, selection: str):
        library = text
        if not (library.startswith('"') or library.startswith("'")):
            library = f"\"{library}\""
        actions.user.insert_snippet_by_name("importStatement", {"0": library})



@mod.action_class
class Actions:
    def go_cast_wrap(type: str):
        """Wraps the selected text in a cast"""
        current_selected = actions.edit.selected_text()
        actions.insert(f"{type}({current_selected})")
