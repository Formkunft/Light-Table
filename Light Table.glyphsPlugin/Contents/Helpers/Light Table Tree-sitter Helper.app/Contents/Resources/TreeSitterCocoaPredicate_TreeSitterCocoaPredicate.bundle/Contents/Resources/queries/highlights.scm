(true_predicate) @constant.builtin
(false_predicate) @constant.builtin

(true_literal) @constant.builtin
(false_literal) @constant.builtin
(null_literal) @constant.builtin
(self) @variable.builtin

(number_literal) @number
(string_literal) @string
(escape_sequence) @constant.character.escape

(aggregate_qualifier) @keyword.operator
(comparison_operator) @operator
(not_operator) @keyword.operator
(and_operator) @keyword.operator
(or_operator) @keyword.operator

(string_comparison_option) @punctuation.special

(function_call name: (identifier) @function.call)
(subquery_keyword) @function.builtin

(variable) @variable
(predicate_argument) @constant.macro

(keypath_expression key: (aggregate_key) @property.builtin)
(keypath_expression key: (identifier) @property)
(comparison_predicate qualifier: (aggregate_qualifier) @keyword.operator)

[
  "("
  ")"
  "{"
  "}"
  "["
  "]"
] @punctuation.bracket

[
  ","
] @punctuation.delimiter

[
  "="
  "=="
  "!="
  "<>"
  "<"
  ">"
  "<="
  "=<"
  ">="
  "=>"
  "**"
  "*"
  "/"
  "+"
  "-"
] @operator
