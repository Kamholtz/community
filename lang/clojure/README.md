# Adding Language Support to Talon

This document explains the steps required to add support for a new programming language in Talon, using Clojure as an example.

## Required Files and Changes

### 1. Language Module (`clojure.py`)

Create a Python module at `community/lang/clojure/clojure.py` that defines:

- **Context matching** - Match the language identifier:
  ```python
  ctx.matches = r"""
  code.language: clojure
  """
  ```

- **Common functions** - Language-specific function names for voice commands:
  ```python
  ctx.lists["user.code_common_function"] = {
      "map": "map",
      "filter": "filter",
      "reduce": "reduce",
      # ... more functions
  }
  ```

- **Keywords** - Language keywords and constructs:
  ```python
  ctx.lists["user.code_keyword"] = {
      "def": "def ",
      "def n": "defn ",
      "let": "let ",
      # ... more keywords
  }
  ```

- **Operators** - Define how operators work in the language:
  ```python
  operators = Operators(
      ASSIGNMENT=" = ",
      MATH_ADD=" + ",
      LAMBDA=lambda: actions.user.insert_between("(fn [", "] )"),
      # ... more operators
  )
  ```

- **Actions** - Language-specific behaviors for common operations:
  ```python
  @ctx.action_class("user")
  class UserActions:
      def code_insert_null():
          actions.auto_insert("nil")
      
      def code_default_function(text: str):
          result = "(defn {}".format(formatted_text)
          actions.user.code_insert_function(result, " [])")
  ```

### 2. Grammar File (`clojure.talon`)

Create a Talon grammar file at `community/lang/clojure/clojure.talon` that includes:

- **Language context** - Match when the language is active:
  ```talon
  code.language: clojure
  -
  ```

- **Tags** - Enable relevant functionality:
  ```talon
  tag(): user.code_comment_line
  tag(): user.code_functions
  tag(): user.code_operators_math
  # ... more tags
  ```

- **Settings** - Configure code formatters:
  ```talon
  settings():
      user.code_private_function_formatter = "SNAKE_CASE"
      user.code_public_function_formatter = "SNAKE_CASE"
  ```

- **Voice commands** - Language-specific grammar rules:
  ```talon
  state def: "def "
  state def n: "defn "
  op map: "(map "
  is nil: "nil?"
  ```

### 3. File Extensions (`community/settings/file_extensions.csv`)

Add the language's file extensions for voice recognition:
```csv
.clj,dot clojure
.cljs,dot clojure script
.cljc,dot clojure common
.edn,dot edn
```

### 4. Language Registry (`community/core/modes/code_languages.py`)

Register the language in the main language list:
```python
Language("clojure", "clojure", ["clj", "cljs", "cljc", "edn"]),
```

## Key Considerations

- **Study existing implementations** - Look at similar languages (especially functional ones like Elixir for Clojure)
- **Language paradigm** - Adapt operators and actions to fit the language's paradigm (e.g., immutable data, prefix notation for Clojure)
- **Common patterns** - Include frequently used patterns and idioms specific to the language
- **File types** - Include all relevant file extensions (source files, config files, etc.)
- **Naming conventions** - Follow the language's standard naming and formatting conventions

## Testing

After implementation:
1. Test Python syntax: `python3 -m py_compile clojure.py`
2. Verify Talon can load the grammar without errors
3. Test voice commands in a Clojure file to ensure proper language detection and functionality