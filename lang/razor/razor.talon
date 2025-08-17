code.language: razor
-
tag(): user.code_imperative
tag(): user.code_object_oriented

tag(): user.code_block_c_like
tag(): user.code_comment_line
tag(): user.code_comment_block_c_like
tag(): user.code_data_bool
tag(): user.code_data_null
tag(): user.code_functions
tag(): user.code_functions_common
tag(): user.code_libraries
tag(): user.code_operators_array
tag(): user.code_operators_assignment
tag(): user.code_operators_bitwise
tag(): user.code_operators_lambda
tag(): user.code_operators_math
tag(): user.code_operators_pointer

settings():
    user.code_private_function_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_function_formatter = "PUBLIC_CAMEL_CASE"
    user.code_private_variable_formatter = "PRIVATE_CAMEL_CASE"
    user.code_protected_variable_formatter = "PUBLIC_CAMEL_CASE"
    user.code_public_variable_formatter = "PUBLIC_CAMEL_CASE"

# Razor-specific commands
at block: user.razor_at_block()
at expression: user.razor_at_expression()
razor if: user.razor_if_block()
razor for each: user.razor_foreach_block()
razor using: user.razor_using_block()
razor model: user.razor_model_directive()
razor section: user.razor_section()

# HTML helpers
html begin form: "@using (Html.BeginForm()) {}"
html action link: "Html.ActionLink(\"\", \"\")"
html partial: "Html.Partial(\"\")"
html render partial: "Html.RenderPartial(\"\")"

# Model and ViewBag
model dot: "@Model."
view bag: "@ViewBag."
view data: "@ViewData[\"\"]"

# Layout and sections
render body: "@RenderBody()"
render section: "@RenderSection(\"\", required: false)"

# Razor directives
model directive: "@model "
layout directive: "@{ Layout = \"\"; }"
using directive: "@using "
inherits directive: "@inherits "

# Common Razor patterns
if model: "@if (Model != null) {}"
if view bag: "@if (ViewBag. != null) {}"
display for: "@Html.DisplayFor(m => m.)"
editor for: "@Html.EditorFor(m => m.)"
label for: "@Html.LabelFor(m => m.)"

# URL helpers
url action: "@Url.Action(\"\", \"\")"
url content: "@Url.Content(\"~/\")"