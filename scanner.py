from token import *
from tokens import *
import fsa as fsa

# a hack I found for printing a single char as a string representation
def dq(s): return '"%s"' %s
  
def initialize(sourceTextArg): 
    global sourceText, lastIndex, sourceIndex, lineIndex, colIndex 
    sourceText = str(sourceTextArg) 
    lastIndex    = len(sourceText) - 1
    sourceIndex  = -1
    lineIndex    =  0
    colIndex     = -1
    fsa.getChar()

def getToken():
    '''char1 is the next char, char2 is the char after char1 (looks two ahead)'''
    # Process whitespace and comments
    while fsa.char1 in WHITESPACE_CHARS or fsa.char2 == "/*":
        fsa.process_whitespace()
 
    # Create a new token. Token gets line/col num from the character.
    token = Token(fsa.character)

    # If EOF, just return that token
    if fsa.char1 == "\0":
        token.type = types.MP_EOF
        return token
    # Identifier FSA
    if fsa.char1 in IDENTIFIER_START:
        token = fsa.identifier_fsa(token)
        return token
    # Integer FSA
    if fsa.char1 in INTEGER:
        token = fsa.integer_fsa(token)
        return token

    if fsa.char1 in STRING_STARTCHARS:
        token = fsa.string_fsa(token)
        return token
 
    if fsa.char1 in SingleCharacterSymbols:
        token = fsa.symbols_fsa(token)
        return token
    
    # If this was reached, we know that we found a char that is not in our defined language
    print "Found a character or symbol that I do not recognize: " + token.getErrorMsg(str(fsa.char1))
    return None
    

#-------------------------------------------
def getNextChar(): 
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
        c = sourceText[sourceIndex] 
        char = Character(c, lineIndex, colIndex, sourceIndex, sourceText) 
  
    return char 
  
def lookahead(offset=1): 
    index = sourceIndex + offset
    #Check for index at eof
    if index > lastIndex: 
        return ENDMARK 
    else: 
        return sourceText[index]
        
#-------------------------------------------
ENDMARK = "\0"  # "lowvalues"   
class Character: 
    def __init__(self, c, lineIndex, colIndex, sourceIndex, sourceText): 
        self.lexeme = c 
        self.sourceIndex = sourceIndex 
        self.lineIndex = lineIndex 
        self.colIndex = colIndex 
        self.sourceText = sourceText 
  
  
    def __str__(self): 
        lexeme = self.lexeme 
        if   lexeme == " " : lexeme = "   space"
        elif lexeme == "\n" : lexeme = "   newline"
        elif lexeme == "\t" : lexeme = "   tab"
        elif lexeme == ENDMARK : lexeme = "   eof"
  
        return (str(self.lineIndex).rjust(6) + str(self.colIndex).rjust(4) + "  " + lexeme)