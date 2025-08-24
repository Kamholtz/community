from talon import Context, Module, actions, settings

from ..tags.operators import Operators

mod = Module()
ctx = Context()
ctx.matches = r"""
code.language: clojure
"""

ctx.lists["user.code_common_function"] = {
    "apply": "apply",
    "concat": "concat",
    "count": "count",
    "def": "def",
    "defn": "defn",
    "filter": "filter",
    "first": "first",
    "get": "get",
    "let": "let",
    "map": "map",
    "print": "print",
    "println": "println",
    "reduce": "reduce",
    "rest": "rest",
    "str": "str",
    "take": "take",
    "vector": "vector",
}

ctx.lists["user.code_keyword"] = {
    "def": "def ",
    "def n": "defn ",
    "def macro": "defmacro ",
    "def protocol": "defprotocol ",
    "def record": "defrecord ",
    "def type": "deftype ",
    "let": "let ",
    "if": "if ",
    "when": "when ",
    "cond": "cond ",
    "case": "case ",
    "loop": "loop ",
    "recur": "recur ",
    "try": "try ",
    "catch": "catch ",
    "finally": "finally ",
    "throw": "throw ",
    "do": "do ",
    "fn": "fn ",
    "true": "true",
    "false": "false",
    "nil": "nil",
    "quote": "quote ",
    "unquote": "unquote ",
    "require": "require ",
    "import": "import ",
    "use": "use ",
    "in namespace": "in-ns ",
    "namespace": "ns ",
}

ctx.lists["user.code_type"] = {
    "string": "String",
    "number": "Number",
    "integer": "Integer",
    "long": "Long",
    "double": "Double",
    "boolean": "Boolean",
    "keyword": "Keyword",
    "symbol": "Symbol",
    "list": "List",
    "vector": "Vector",
    "map": "Map",
    "set": "Set",
    "seq": "Seq",
    "atom": "Atom",
    "ref": "Ref",
    "agent": "Agent",
    "var": "Var",
}

operators = Operators(
    # code_operators_array - using get for accessing
    SUBSCRIPT=lambda: actions.user.insert_between("(get ", " )"),
    # code_operators_assignment - no traditional assignment in Clojure
    ASSIGNMENT=" ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" mod ",
    MATH_EQUAL=" = ",
    MATH_NOT_EQUAL=" not= ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" and ",
    MATH_OR=" or ",
    MATH_NOT=" not ",
    # code_operators_lambda
    LAMBDA=lambda: actions.user.insert_between("(fn [", "] )"),
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    def code_self():
        actions.auto_insert("this")

    def code_operator_object_accessor():
        actions.auto_insert(".")

    def code_insert_null():
        actions.auto_insert("nil")

    def code_insert_is_null():
        actions.auto_insert(" nil?")

    def code_insert_is_not_null():
        actions.auto_insert(" (not (nil? ")
        actions.edit.right()
        actions.auto_insert("))")

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    def code_insert_function(text: str, selection: str):
        text += f"({selection or ''})"
        actions.user.paste(text)
        actions.edit.left()

    def code_default_function(text: str):
        """Inserts function declaration"""
        result = "(defn {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_public_function_formatter")
            )
        )
        actions.user.code_insert_function(result, " [])")

    def code_public_function(text: str):
        """Inserts public function declaration"""
        actions.user.code_default_function(text)

    def code_private_function(text: str):
        """Inserts private function declaration"""
        result = "(defn- {}".format(
            actions.user.formatted_text(
                text, settings.get("user.code_private_function_formatter")
            )
        )
        actions.user.code_insert_function(result, " [])")

    def code_break():
        # Clojure doesn't have traditional break statement
        actions.insert("(recur)")

    def code_state_if():
        actions.user.insert_between("(if ", " )")

    def code_state_else():
        # In Clojure, else is part of if expression
        pass

    def code_insert_comment_line():
        actions.auto_insert("; ")

    def code_toggle_comment():
        actions.edit.line_start()
        actions.insert("; ")