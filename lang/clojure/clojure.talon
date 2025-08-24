code.language: clojure
-
tag(): user.code_comment_line
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_keywords
tag(): user.code_libraries
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_math
tag(): user.code_operators_lambda

settings():
    user.code_private_function_formatter = "DASH_SEPARATED"
    user.code_protected_function_formatter = "DASH_SEPARATED"
    user.code_public_function_formatter = "DASH_SEPARATED"
    user.code_private_variable_formatter = "DASH_SEPARATED"
    user.code_protected_variable_formatter = "DASH_SEPARATED"
    user.code_public_variable_formatter = "DASH_SEPARATED"

# Clojure-specific grammars
state def: "def "
state def n: "defn "
state def macro: "defmacro "
state let: "let "
state if: "if "
state when: "when "
state cond: "cond "
state case: "case "
state loop: "loop "
state recur: "recur"
state try: "try "
state catch: "catch "
state finally: "finally "
state throw: "throw "
state do: "do "
state f n: "fn "

# Clojure parentheses and data structures
paren: "()"
left paren: "("
right paren: ")"
square: "[]"
left square: "["
right square: "]"
brace: "{}"
left brace: "{"
right brace: "}"

# Clojure-specific symbols
hash: "#"
caret: "^"
quote: "'"
back quote: "`"
tilde: "~"
at sign: "@"
percent: "%"

# Threading macros
thread first: "-> "
thread last: "->> "
thread as: "as-> "

# Clojure collection operations
op first: "(first "
op rest: "(rest "
op cons: "(cons "
op conj: "(conj "
op assoc: "(assoc "
op dissoc: "(dissoc "
op merge: "(merge "
op concat: "(concat "
op map: "(map "
op filter: "(filter "
op reduce: "(reduce "
op take: "(take "
op drop: "(drop "
op count: "(count "

# Clojure predicates
is nil: "nil?"
is empty: "empty?"
is some: "some?"
is even: "even?"
is odd: "odd?"
is vector: "vector?"
is map: "map?"
is set: "set?"
is list: "list?"
is seq: "seq?"
is string: "string?"
is number: "number?"
is keyword: "keyword?"
is symbol: "symbol?"

# REPL commands
require namespace: "(require '"
use namespace: "(use '"
import namespace: "(import '"
in namespace: "(in-ns '"

# Namespace declaration
namespace: "ns "