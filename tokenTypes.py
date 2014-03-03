#This class makes the Enum concept possible with older version of Python
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

#All the different types of tokens in microPascal
types = Enum([
    #Reserved Words
    "MP_AND",
    "MP_BEGIN",
    "MP_DIV",
    "MP_DO",
    "MP_DOWNTO",
    "MP_ELSE",
    "MP_END",
    "MP_FIXED",
    "MP_FLOAT",
    "MP_FOR",
    "MP_FUNCTION",
    "MP_IF",
    "MP_INTEGER",
    "MP_MOD",
    "MP_NOT",
    "MP_OR",
    "MP_PROCEDURE",
    "MP_PROGRAM",
    "MP_READ",
    "MP_REPEAT",
    "MP_THEN",
    "MP_TO",
    "MP_UNTIL",
    "MP_VAR",
    "MP_WHILE",
    "MP_WRITELN",
    "MP_WRITE",
    "MP_TRUE",
    "MP_FALSE",
    "MP_BOOLEAN",
    "MP_STRING",
    #Identifiers and literals
    "MP_IDENTIFIER",
    "MP_INTEGER_LIT",
    "MP_FIXED_LIT",
    "MP_FLOAT_LIT",
    "MP_STRING_LIT",
    #Symbols
    "MP_PERIOD",
    "MP_COMMA",
    "MP_SCOLON",
    "MP_LPAREN",
    "MP_RPAREN",
    "MP_EQUAL",
    "MP_GTHAN",
    "MP_GEQUAL",
    "MP_LTHAN",
    "MP_LEQUAL",
    "MP_NEQUAL",
    "MP_ASSIGN",
    "MP_PLUS",
    "MP_MINUS",
    "MP_TIMES",
    "MP_COLON",
    "MP_FLOAT_DIVIDE",
    #End of file
    "MP_EOF",
    #Errors
    "MP_RUN_COMMENT",
    "MP_RUN_STRING",
    "MP_ERROR",
    #Whitespace
    "MP_WHITESPACE",
    #Comments
    "MP_COMMENT"])