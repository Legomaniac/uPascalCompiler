#This class makes the Enum concept possible with older version of Python
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

#All the different classification types in microPascal
classification = Enum([
    VARIABLE,
    PARAMETER,
    FUNCTION,
    PROCEDURE,
    DISREG,
    RETADDR
    ])