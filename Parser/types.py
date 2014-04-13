#This class makes the Enum concept possible with older version of Python
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

#All the different variable types in microPascal
varTypes = Enum([
    INTEGER,
    FLOAT,
    BOOLEAN,
    STRING
    ])