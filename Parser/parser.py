#parser.py
from tokens import *
import scanner as scanner
from leaf import Leaf

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
	token  = scanner.get()
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
    if match(MP_EOF):

def program():
    programHeading()
    expect(MP_SCOLON)
    block()
    expect(MP_PERIOD)

def programHeading():
    expect(MP_PROGRAM)
    programIdentifier()

def block():
    variableDeclarationPart()
    procedureAndFunctionDeclarationPart()
    statementPart()

def variableDeclarationPart():
    if match(MP_VAR):
        variableDeclaration()
        expect(MP_SCOLON)
        variableDeclarationTail()
    elif match(EPSILON):
        pass

def variableDeclarationTail():

def variableDeclaration():

def type():

def procedureAndFunctionDeclarationPart():

def procedureDeclaration():

def functionDeclaration():

def procedureHeading():

def functionHeading():

def optionalFormalParameterList():

def formalParameterSectionTail():

def formalParameterSection():

def valueParameterSection():

def variableParameterSection():

def statementPart():

def compoundStatement():

def statementSequence():

def statementTail():

def statement():

def emptyStatement():

def readStatement():

def readParameterTail():

def readParameter():

def writeStatement():

def writeParameterTail():

def writeParameter():

def assignmentStatement():

#-----------------------------------
# Section from Justin
def ifstatement():
    """ ifstatement -> "if" BooleanExpression "then" Statement OptionalElsePart """
    if match(MP_IF):
        booleanexpression()
        expect(MP_THEN)
        statement()
        optionalelsepart()
        
def optionalelsepart():
    if match(MP_ELSE):
        statement()
    elif match(EPSILON):
        pass
    
def repeatstatement():
    if match(MP_REPEAT):
        statementsequence()
        expect(MP_UNTIL)
        booleanexpression()
        
def whilestatement():
    if match(MP_WHILE):
        booleanexpression()
        expect(MP_DO)
        statement()
        
def forstatement():
    if match(MP_FOR):
        controlvariable()
        expect(MP_ASSIGN)
        initialvalue()
        stepvalue()
        finalvalue()
        expect(MP_DO)
        statement()
        
def controlvariable():
    variableidentifier()
    
def initialvalue():
    ordinalexpression()
    
def stepvalue():
    if match(MP_TO):
        pass
    elif match(MP_DOWNTO):
        pass
        
def finalvalue():
    ordinalexpression()
    
def procedurestatement():
    procedureidentifier()
    optionalactualparameterlist()
    
def optionalactualparameterlist():
    if match(MP_LPAREN):
        actualparameter()
        actualparametertail()
        expect(MP_RPAREN)
    elif match(EPSILON):
        pass
        
def actualparametertail():
    if match(MP_COMMA):
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
    if match(EPSILON):
        pass
    
def relationaloperator():
    if match(MP_EQUAL):
    elif match(MP_LTHAN):
    elif match(MP_GTHAN):
    elif match(MP_LEQUAL):
    elif match(MP_GEQUAL):
    elif match(MP_NEQUAL):
        
def simpleexpression():
    optionalsign()
    term()
    termtail()
    
def termtail():
    addingoperator()
    term()
    termtail()
    if match(EPSILON):
        pass
    
def optionalsign():
    if match(MP_PLUS):
    elif match(MP_MINUS):
    
def addingoperator():
    if match(MP_PLUS):
    elif match(MP_MINUS):
    elif match(MP_OR):
        
def term():
    factor()
    factortail()
    
def factortail():
    multiplyingoperator()
    factor()
    factortail()
    
def multiplyingoperator():
    if match(MP_TIMES):
    elif match(MP_FLOAT_DIVIDE):
    elif match(MP_DIV):
    elif match(MP_MOD):
    elif match(MP_AND):
        
def factor():
    unsignedinteger()
    unsignedfloat()
    stringliteral()
    if match(MP_TRUE):
    elif match(MP_FALSE):
    elif match(MP_NOT):
        factor
    elif match(MP_LPAREN):
        expression
        expect(MP_RPAREN)
    functionidentifier()
    optionalactualparameterlist()
    
def programidentifier():
    expect(IDENTIFIER_CHARS)
    
def variableidentifier():
    expect(IDENTIFIER_CHARS)
    
def procedureidentifier():
    expect(IDENTIFIER_CHARS)
    
def functionidentifier():
    expect(IDENTIFIER_CHARS)
    
def booleanexpression():
    expression()
    
def ordinalexpression():
    expression()
    
def identifierlist():
    expect(IDENTIFIER_CHARS)
    identifiertail()
    
def identifiertail():
    if match(MP_COMMA):
        expect(IDENTIFIER_CHARS)
        identifiertail()
    elif match(EPSILON):
        pass
