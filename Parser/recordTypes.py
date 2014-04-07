#This class makes the Enum concept possible with older version of Python
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

#All the different semantic record types in microPascal
recTypes = Enum([
    "IDENTIFIER",
    "LITERAL",
    "REL_OP",
    "OPTIONAL_SIGN",
    "ADD_OP",
    "MUL_OP",
    "SYMBOL_TABLE",
    "WRITE_STATEMENT",
    "LABEL",
    "FOR_DIRECTION",
    "BLOCK",
    "FORMAL_PARAM"])