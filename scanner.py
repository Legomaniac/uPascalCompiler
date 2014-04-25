from token import *
from tokens import *
from tokenTypes import *
import fsa as fsa

# a hack I found for printing a single char as a string representation
def dq(s): return '"%s"' %s

#Auxiliary Regular Expressions
IDENTIFIER_CHARS = string.letters + "_"
NUMBER_CHARS = string.digits
LITERAL_CHAR = "\'"
SYMBOL_CHARS = "." + "," + ";" + "(" + ")" + "=" + "<" + ">" + "+" + "-" + "*" + "/" + ":"
WHITESPACE_CHARS = " \t\n"
COMMENT_CHAR = "{"
  
def initialize(sourceTextArg): 
    global sourceText, lastIndex, sourceIndex, lineIndex, colIndex 
    sourceText = str(sourceTextArg) 
    lastIndex    = len(sourceText) - 1
    sourceIndex  = -1
    lineIndex    =  0
    colIndex     = -1
    fsa.getChar()

def checkScanError(curToken):
    """Check for Run on Comment"""
    if curToken.getType() == types.MP_RUN_COMMENT:
        print "SCAN ERROR: Run on comment found @ line:" + str(curToken.getLineNumber()) + ", column: " + str(curToken.getColNumber())
    elif curToken.getType() == types.MP_RUN_STRING:
        print "SCAN ERROR: Run on string found.. lex: " + str(curToken.getLexeme()) + " @ line:" + str(curToken.getLineNumber()) + ", column: " + str(curToken.getColNumber())
    elif curToken.getType() == types.MP_ERROR:
        print "SCAN ERROR: Invalid character (" + str(curToken.getLexeme()) + ") found @ line:" + str(curToken.getLineNumber()) + ", column: " + str(curToken.getColNumber())

def getToken():
    nextToken = getNextToken()
    while nextToken.getType() == types.MP_WHITESPACE or nextToken.getType() == types.MP_COMMENT:
        nextToken = getNextToken()
    checkScanError(nextToken)
    return nextToken

def getNextToken():
    '''char1 is the next char, char2 is the char after char1 (looks two ahead)'''
    foundToken = None
    if lookahead(1) is types.MP_EOF:
        foundToken = Token(types.MP_EOF, "EOF", lineIndex, colIndex)
    else:
        nextChar = getNextChar()
        if nextChar['lexeme'] in IDENTIFIER_CHARS:
            foundToken = fsa.IdentifierFSA(nextChar)
        elif nextChar['lexeme'] in NUMBER_CHARS:
            foundToken = fsa.NumbersFSA(nextChar)
        elif nextChar['lexeme'] in LITERAL_CHAR:
            foundToken = fsa.LiteralFSA(nextChar)
        elif nextChar['lexeme'] in SYMBOL_CHARS:
            foundToken = fsa.SymbolFSA(nextChar)
        elif nextChar['lexeme'] in WHITESPACE_CHARS:
            foundToken = fsa.WhitespaceFSA(nextChar)
        elif nextChar['lexeme'] in COMMENT_CHAR:
            foundToken = fsa.CommentFSA(nextChar)
        else:
            foundToken = Token(types.MP_ERROR, str(nextChar['lexeme']), nextChar['lineIndex'], nextChar['colIndex'])
        return foundToken
#-------------------------------------------
def getNextChar(): 
    """ 
    Return the next character in sourceText. 
    """
    global lastIndex, sourceIndex, lineIndex, colIndex
    
    sourceIndex += 1 # increment the index in sourceText 
    # maintain the line count 
    if sourceIndex > 0: 
        if sourceText[sourceIndex - 1] == "\n":
            lineIndex += 1
            colIndex  = -1
    
    colIndex += 1
    lex = sourceText[sourceIndex] 
    char = {'lexeme':lex, 'lineIndex':lineIndex, 'colIndex':colIndex, 'sourceIndex':sourceIndex, 'sourceText':sourceText}
    return char 
  
def lookahead(offset=1): 
    index = sourceIndex + offset
    #Check for index at eof
    if index > lastIndex: 
        return types.MP_EOF
    else: 
        return sourceText[index]

def hasNextChar():
    if sourceText[sourceIndex - 1] == "\n":
        return False
    else:
        return True

def setColumnIndex(index):
    colIndex = index