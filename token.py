class Token:
    """
    A Token object contains {type, lexeme, line#, col#}
    """
    def __init__(self, Type, lex, line, col):
        self.Type = Type
        self.lexeme = lex
        self.lineIndex = line
        self.colIndex = col
    
    def getType(self):
        return self.Type
    
    def getLexeme(self):
        return self.lexeme
    
    def getLineNumber(self):
        return self.lineIndex
    
    def getColNumber(self):
        return self.colIndex