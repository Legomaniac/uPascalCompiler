from token import *
  
def initialize(sourceTextArg): 
    global sourceText, lastIndex, sourceIndex, lineIndex, colIndex 
    sourceText = str(sourceTextArg) 
    lastIndex    = len(sourceText) - 1
    sourceIndex  = -1
    lineIndex    =  0
    colIndex     = -1

  
def get(): 
    """ 
    Return the next character in sourceText. 
    """
    global lastIndex, sourceIndex, lineIndex, colIndex 
  
    sourceIndex += 1    # increment the index in sourceText 
  
    # maintain the line count 
    if sourceIndex > 0: 
        if sourceText[sourceIndex - 1] == "\n": 
            lineIndex += 1
            colIndex  = -1
  
    colIndex += 1
    
    #Check for index at eof
    if sourceIndex > lastIndex:
        char = Character(ENDMARK, lineIndex, colIndex, sourceIndex,sourceText) 
    else: 
        c    = sourceText[sourceIndex] 
        char = Character(c, lineIndex, colIndex, sourceIndex, sourceText) 
  
    return char 
  
  
def lookahead(offset=1): 
    index = sourceIndex + offset
    #Check for index at eof
    if index > lastIndex: 
        return ENDMARK 
    else: 
        return sourceText[index]
        
        
ENDMARK = "\0"  # aka "lowvalues"   
class Character: 
    def __init__(self, c, lineIndex, colIndex, sourceIndex, sourceText): 
        self.lexeme = c 
        self.sourceIndex = sourceIndex 
        self.lineIndex = lineIndex 
        self.colIndex = colIndex 
        self.sourceText = sourceText 
  
  
    def __str__(self): 
        lexeme = self.lexeme 
        if   lexeme == " "     : lexeme = "   space"
        elif lexeme == "\n"    : lexeme = "   newline"
        elif lexeme == "\t"    : lexeme = "   tab"
        elif lexeme == ENDMARK : lexeme = "   eof"
  
        return (str(self.lineIndex).rjust(6) + str(self.colIndex).rjust(4) + "  " + lexeme)
