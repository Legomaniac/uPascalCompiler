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
WHITESPACE_CHARS = " " + "\t"
COMMENT_CHAR = "{"
  
def initialize(sourceTextArg): 
    global sourceText, lastIndex, sourceIndex, lineIndex, colIndex 
    sourceText = str(sourceTextArg)
    lastIndex = len(sourceText)
    sourceIndex = 0
    lineIndex = 0
    colIndex = 0

def checkScanError(curToken):
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
    foundToken = None
    if eof() and hasNextChar() is False:
        foundToken = Token(types.MP_EOF, "EOF", lineIndex, colIndex)
    else:
        nextChar = getCurChar()
        #print "SourceIndex: " + str(sourceIndex) + ", LastIndex: " + str(lastIndex) + ", Char: " + str(sourceText[sourceIndex])
        if nextChar['lexeme'] in IDENTIFIER_CHARS:
            foundToken = fsa.IdentifierFSA()
        elif nextChar['lexeme'] in NUMBER_CHARS:
            foundToken = fsa.NumbersFSA()
        elif nextChar['lexeme'] in LITERAL_CHAR:
            foundToken = fsa.LiteralFSA()
        elif nextChar['lexeme'] in SYMBOL_CHARS:
            foundToken = fsa.SymbolFSA()
        elif nextChar['lexeme'] in WHITESPACE_CHARS:
            foundToken = fsa.WhitespaceFSA()
        elif nextChar['lexeme'] in COMMENT_CHAR:
            foundToken = fsa.CommentFSA()
        if foundToken is None:
            nextChar = getNextChar()
            foundToken = Token(types.MP_ERROR, str(nextChar['lexeme']), nextChar['lineIndex'], nextChar['colIndex'] -1)
        #print "Token found: " + foundToken.getLexeme() + ", type: " + str(foundToken.getType())
    return foundToken
#--------------------------------------------------
#Always have to look one ahead of current position
#--------------------------------------------------
def getNextChar(): 
    """ 
    Return the current character in sourceText and set the next one. 
    """
    global lastIndex, sourceIndex, lineIndex, colIndex
    char = getCurChar()
    sourceIndex += 1
    colIndex += 1
    while hasNextChar() and sourceText[sourceIndex] == "\n":
        lineIndex += 1
        colIndex  = 0
        sourceIndex += 1
    return char

def getCurChar():
    """ 
    Return the current character in sourceText. 
    """
    lex = sourceText[sourceIndex]
    char = {'lexeme':lex, 'lineIndex':lineIndex, 'colIndex':colIndex, 'sourceIndex':sourceIndex}
    return char

def eof():
    if sourceIndex == lastIndex:
        return True
    else:
        return False

def hasNextChar():
    if sourceIndex < lastIndex:
        return True
    else:
        return False

def setIndexes(col, src):
    global colIndex, sourceIndex
    colIndex = col
    sourceIndex += src