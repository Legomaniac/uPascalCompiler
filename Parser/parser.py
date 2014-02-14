#parser.py
import sys
from leaf import Leaf
sys.path.insert(0, '../')
from tokens import *
import scanner as scanner

class ParsingError(Exception): pass

token = None
indent = 0

def dq(s): return '"%s"' %s

def push(s):
	global indent
	indent += 1
	if verbose: print((" >"*indent) + " " + s)

def pop(s):
	global indent
	if verbose: print((" <"*indent) + " " + s)
	indent -= 1

# --------------------------------------------------------------

def parse(sourceText):
    global scanner 
	# create a Lexer object & pass it the sourceText
    scanner.initialize(sourceText)
    getToken()
    program()

def getToken():
	global token 
	token  = scanner.getToken()
	print ( ("  " * indent) + " * " + token.show())
    
# --------------------------------------------------------------

def error(msg):
    print msg
    
def matchOneOf(tempTokenTypes):
	for tempTokenType in tempTokenTypes:
		print "matchOneOf", tempTokenType, token.type
		if token.type == tempTokenType:
			return True
	return False

def match(tempTokenType):
	if token.type == tempTokenType:
		return True
	return False

def expect(*args):
	for tempTokenType in args:
		if token.type == tempTokenType:
			getToken()
			return True
	error("Expected to find "
		+ dq(str(args))
		+ " but instead match " 
		+ token.show()
		)

#----- CFG Definitions -------------  
#-----------------------------------
#Section from James

def systemGoal():
    if match(types.MP_EOF):
        pass

def program():
    programHeading()
    expect(types.MP_SCOLON)
    block()
    expect(types.MP_PERIOD)

def programHeading():
    expect(types.MP_PROGRAM)
    programIdentifier()

def block():
    variableDeclarationPart()
    procedureAndFunctionDeclarationPart()
    statementPart()

def variableDeclarationPart():
    if match(types.MP_VAR):
        variableDeclaration()
        expect(types.MP_SCOLON)
        variableDeclarationTail()
    elif match(types.EPSILON):
        pass

def variableDeclarationTail():
    pass

def variableDeclaration():
    pass
    
def Type():
    pass

def procedureAndFunctionDeclarationPart():
    pass

def procedureDeclaration():
    pass

def functionDeclaration():
    pass

def procedureHeading():
    pass

def functionHeading():
    pass

def optionalFormalParameterList():
    pass

def formalParameterSectionTail():
    pass

def formalParameterSection():
    pass

def valueParameterSection():
    pass

def variableParameterSection():
    pass

def statementPart():
    pass

def compoundStatement():
    pass

def statementSequence():
    pass

def statementTail():
    pass

def statement():
    pass

def emptyStatement():
    pass

def readStatement():
    pass

def readParameterTail():
    pass

def readParameter():
    pass

def writeStatement():
    pass

def writeParameterTail():
    pass

def writeParameter():
    pass

def assignmentStatement():
    pass

#-----------------------------------
# Section from Justin
def ifstatement():
    """ ifstatement -> "if" BooleanExpression "then" Statement OptionalElsePart """
    if match(types.MP_IF):
        booleanexpression()
        expect(types.MP_THEN)
        statement()
        optionalelsepart()
        
def optionalelsepart():
    if match(types.MP_ELSE):
        statement()
    elif match(types.EPSILON):
        pass
    
def repeatstatement():
    if match(types.MP_REPEAT):
        statementsequence()
        expect(types.MP_UNTIL)
        booleanexpression()
        
def whilestatement():
    if match(types.MP_WHILE):
        booleanexpression()
        expect(types.MP_DO)
        statement()
        
def forstatement():
    if match(types.MP_FOR):
        controlvariable()
        expect(types.MP_ASSIGN)
        initialvalue()
        stepvalue()
        finalvalue()
        expect(types.MP_DO)
        statement()
        
def controlvariable():
    variableidentifier()
    
def initialvalue():
    ordinalexpression()
    
def stepvalue():
    if match(types.MP_TO):
        pass
    elif match(types.MP_DOWNTO):
        pass
        
def finalvalue():
    ordinalexpression()
    
def procedurestatement():
    procedureidentifier()
    optionalactualparameterlist()
    
def optionalactualparameterlist():
    if match(types.MP_LPAREN):
        actualparameter()
        actualparametertail()
        expect(types.MP_RPAREN)
    elif match(types.EPSILON):
        pass
        
def actualparametertail():
    if match(types.MP_COMMA):
        actualparameter()
        actualparametertail()

def actualparameter():
    ordinalexpression()
    
def expression():
    simpleexpression()
    optionalrelationalpart()
    
def optionalrelationalpart():
    relationaloperator()
    simpleexpression()
    if match(types.EPSILON):
        pass
    
def relationaloperator():
    if match(types.MP_EQUAL):
        pass
    elif match(types.MP_LTHAN):
        pass
    elif match(types.MP_GTHAN):
        pass
    elif match(types.MP_LEQUAL):
        pass
    elif match(types.MP_GEQUAL):
        pass
    elif match(types.MP_NEQUAL):
        pass
        
def simpleexpression():
    optionalsign()
    term()
    termtail()
    
def termtail():
    addingoperator()
    term()
    termtail()
    if match(types.EPSILON):
        pass
    
def optionalsign():
    if match(types.MP_PLUS):
        pass
    elif match(types.MP_MINUS):
        pass
    
def addingoperator():
    if match(types.MP_PLUS):
        pass
    elif match(types.MP_MINUS):
        pass
    elif match(types.MP_OR):
        pass
        
def term():
    factor()
    factortail()
    
def factortail():
    multiplyingoperator()
    factor()
    factortail()
    
def multiplyingoperator():
    if match(types.MP_TIMES):
        pass
    elif match(types.MP_FLOAT_DIVIDE):
        pass
    elif match(types.MP_DIV):
        pass
    elif match(types.MP_MOD):
        pass
    elif match(types.MP_AND):
        pass
        
def factor():
    unsignedinteger()
    unsignedfloat()
    stringliteral()
    if match(types.MP_TRUE):
        pass
    elif match(types.MP_FALSE):
        pass
    elif match(types.MP_NOT):
        factor()
    elif match(types.MP_LPAREN):
        expression()
        expect(types.MP_RPAREN)
    functionidentifier()
    optionalactualparameterlist()
    
def programidentifier():
    expect(types.IDENTIFIER_CHARS)
    
def variableidentifier():
    expect(types.IDENTIFIER_CHARS)
    
def procedureidentifier():
    expect(types.IDENTIFIER_CHARS)
    
def functionidentifier():
    expect(types.IDENTIFIER_CHARS)
    
def booleanexpression():
    expression()
    
def ordinalexpression():
    expression()
    
def identifierlist():
    expect(types.IDENTIFIER_CHARS)
    identifiertail()
    
def identifiertail():
    if match(types.MP_COMMA):
        expect(types.IDENTIFIER_CHARS)
        identifiertail()
    elif match(types.EPSILON):
        pass
