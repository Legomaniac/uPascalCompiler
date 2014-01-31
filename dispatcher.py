import scanner as scanner
from token import *
from tokens import *
 
class ScanError(Exception): pass
 
# enclose string s in double quotes
def dq(s): return '"%s"' %s

def initialize(sourceText):
    global scanner
    # initialize the scanner with the sourceText
    scanner.initialize(sourceText)
 
    # use the scanner to read the first character from the sourceText
    getChar()
 

def getToken():
    # read past and ignore any whitespace characters or any comments
    while c1 in WHITESPACE_CHARS or c2 == "/*":
 
        # process whitespace
        while c1 in WHITESPACE_CHARS:
            token = Token(character)
            token.type = WHITESPACE
            getChar() 
 
            while c1 in WHITESPACE_CHARS:
                token.lexeme += c1
                getChar()
 
        # process comments
        while c2 == "/*":
            # we found comment start
            token = Token(character)
            token.type = COMMENT
            token.lexeme = c2
 
            # getChar()
            # getChar()
 
            while not (c2 == "*/"):
                if c1 == EOF:
                    token.abort("Found end of file before end of comment")
                token.lexeme += c1
                getChar()
 
            token.lexeme += c2 # append the */ to the token lexeme
 
            # getChar()
            # getChar()
 
    # Create a new token.  The token will pick up
    # its line and column information from the character.
    token = Token(character)
 
    if c1 == EOF:
        token.type = EOF
        return token
 
    if c1 in IDENTIFIER_START:
        token.type = IDENTIFIER
        getChar() 
 
        while c1 in IDENTIFIER_CHARS:
            token.lexeme += c1
            getChar() 
 
        if token.lexeme in ReservedWords: token.type = token.lexeme
        return token
 
    if c1 in INTEGER:
        token.type = NUMBER
        getChar() 
         
        while c1 in INTEGER:
            token.lexeme += c1
            getChar() 
        return token
 
    if c1 in STRING_STARTCHARS:
        # remember the quoteChar (single or double quote)
        # so we can look for the same character to terminate the quote.
        quoteChar   = c1
 
        getChar() 
 
        while c1 != quoteChar:
            if c1 == EOF:
                token.abort("Found end of file before end of string literal")
 
            token.lexeme += c1  # append quoted character to text
            getChar()      
 
        token.lexeme += c1      # append close quote to text
        getChar()          
        token.type = STRING
        return token
 
    if c1 in SingleCharacterSymbols:
        token.type  = token.lexeme  # for symbols, the token type is same as the lexeme
        getChar() # read past the symbol
        return token
 
    # else.... We have encountered something that we don't recognize.
    token.abort("Found a character or symbol that I do not recognize: " + dq(c1))
 
#-------------------------------------------------------------------
#
#-------------------------------------------------------------------
def getChar():
    global c1, c2, character
    character = scanner.get()
    c1 = character.lexeme
    #---------------------------------------------------------------
    # Every time we get a character from the scanner, we also  
    # lookahead to the next character and save the results in c2.
    # This makes it easy to lookahead 2 characters.
    #---------------------------------------------------------------
    c2    = c1 + scanner.lookahead(1)