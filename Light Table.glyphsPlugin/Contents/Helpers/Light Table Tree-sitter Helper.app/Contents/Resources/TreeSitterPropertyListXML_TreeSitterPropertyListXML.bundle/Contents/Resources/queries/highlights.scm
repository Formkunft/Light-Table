; ============================================================================
; Boolean — must come before generic delimiters so that <, />, and the tag
; name inside <true/> and <false/> are captured as @boolean, not as
; @punctuation.delimiter or @tag.
; ============================================================================

(true) @constant.builtin
(true "<" @constant.builtin)
(true "true" @constant.builtin)
(true "/>" @constant.builtin)

(false) @constant.builtin
(false "<" @constant.builtin)
(false "false" @constant.builtin)
(false "/>" @constant.builtin)

; ============================================================================
; Delimiters
; ============================================================================

[
  "<?" "?>"
  "<!"
  "<" ">"
  "</" "/>"
] @punctuation.delimiter

; ============================================================================
; XML declaration
; ============================================================================

(xml_declaration "xml" @keyword)

(xml_attribute
  name: (xml_attribute_name) @property)

(xml_attribute
  value: (attribute_value) @string)

(attribute_value ["\"" "'"] @punctuation.delimiter)

; ============================================================================
; DOCTYPE
; ============================================================================

(doctype "DOCTYPE" @keyword)

(doctype "plist" @type)

[ "SYSTEM" "PUBLIC" ] @keyword

(pubid_literal) @string.special

(system_literal) @string.special

; ============================================================================
; <plist> root element
; ============================================================================

(plist "plist" @tag)

(plist_attribute "version" @property)

(plist_attribute (attribute_value) @string)

; ============================================================================
; Container elements
; ============================================================================

(array "array" @tag)

(dict "dict" @tag)

; ============================================================================
; Key — no special token for content
; ============================================================================

(key "key" @tag)

(key_content) @property.key

; ============================================================================
; String — content is @string
; ============================================================================

(string "string" @tag)

(string_content) @string

; ============================================================================
; Integer — content is @number
; ============================================================================

(integer "integer" @tag)

(integer_content) @number

; ============================================================================
; Real — content is @number
; ============================================================================

(real "real" @tag)

(real_content) @number

; ============================================================================
; Date — content is @constant
; ============================================================================

(date "date" @tag)

(date_content) @constant

; ============================================================================
; Data — no special token for content
; ============================================================================

(data "data" @tag)

; ============================================================================
; Comments
; ============================================================================

(comment) @comment
