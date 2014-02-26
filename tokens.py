import string
from tokenTypes import types

# The list of reserved words
ReservedWords = {
"and" : types.MP_AND,
"begin" : types.MP_BEGIN,
"Boolean" : types.MP_BOOLEAN,
"div" : types.MP_DIV,
"do" : types.MP_DO,
"downto" : types.MP_DOWNTO,
"else" : types.MP_ELSE,
"end" : types.MP_END,
"false" : types.MP_FALSE,
"fixed" : types.MP_FIXED,
"float" : types.MP_FLOAT,
"for" : types.MP_FOR,
"function" : types.MP_FUNCTION,
"if" : types.MP_IF,
"integer" : types.MP_INTEGER,
"mod" : types.MP_MOD,
"not" : types.MP_NOT,
"or" : types.MP_OR,
"procedure" : types.MP_PROCEDURE,
"program" : types.MP_PROGRAM,
"read" : types.MP_READ,
"repeat" : types.MP_REPEAT,
"string" : types.MP_STRING,
"then" : types.MP_THEN,
"true" : types.MP_TRUE,
"to" : types.MP_TO,
"type" : types.MP_TYPE,
"until" : types.MP_UNTIL,
"var" : types.MP_VAR,
"while" : types.MP_WHILE,
"write" : types.MP_WRITE,
"writeln" : types.MP_WRITELN
}
 
# The list of single string types
SingleCharacterSymbols = {
":=" : types.MP_ASSIGN,
":" : types.MP_COLON,
"," : types.MP_COMMA,
"=" : types.MP_EQUAL,
"/" : types.MP_FLOAT_DIVIDE,
">=" : types.MP_GEQUAL,
">" : types.MP_GTHAN,
"<=" : types.MP_LEQUAL,
"(" : types.MP_LPAREN,
")" : types.MP_RPAREN,
"<" : types.MP_LTHAN,
"-" : types.MP_MINUS,
"<>" : types.MP_NEQUAL,
"." : types.MP_PERIOD,
"+" : types.MP_PLUS,
";" : types.MP_SCOLON,
"*" : types.MP_TIMES
}

"""
tokenTypes not defined above:
MP_IDENTIFIER
MP_INTEGER_LIT
MP_FIXED_LIT
MP_FLOAT_LIT
MP_STRING_LIT
MP_EOF
MP_RUN_COMMENT
MP_RUN_STRING
MP_ERROR
"""

#Auxiliary Regular Expressions
IDENTIFIER_START = string.letters
IDENTIFIER_CHARS = string.letters + string.digits + "_"
INTEGER = string.digits
FIXED = string.digits + "."
FLOAT = string.digits + "." + "e" + "E" + "+" + "-"
STRING_STARTCHARS = "'" + '"'
WHITESPACE_CHARS = " \t\n"
EPSILON = ""