#parser.py
from tokens import *
import scanner as scanner

token = None

def dq(s): return '"%s"' %s

def error(msg):
    print msg
    
def getToken():
    global token
    token = scanner.getToken()

#Checks to see if the parameter matches what the token actually is
def match(tempToken):
    if (token == tempToken):
        getToken()
        return True
    return False

def consume(tempTokenType):
    if token.type == tempTokenType:
        getToken()
    else:
        error("Expected to find: " + dq(tempTokenType) + ", but found: " + token.show())
        
def parse(sourceText):
    global scanner
    scanner.initialize(sourceText)
    getToken()
    start()
    
def start():
    systemgoal() #This is not added yet...
    while not match(EOF):
        statement() #This is not added yet...
    consume(EOF)
    
#----- CFG Definitions -------------  
#-----------------------------------
#Section from James





#-----------------------------------
def ifstatement():
    """ ifstatement -> ["if" BooleanExpression "then" Statement OptionalElsePart] """
    if found(MP_IF):
        booleanexpression()
        consume(MP_THEN)
        statement()
        optionalelsepart()
        
def optionalelsepart():
    if found(MP_ELSE):
        statement()
    # then epsilon
    
def repeatstatement():
    if found(MP_REPEAT):
        statementsequence()
        consume(MP_UNTIL)
        booleanexpression()
        
def whilestatement():
    if found(MP_WHILE):
        booleanexpression()
        consume(MP_DO)
        statement()
        
def forstatement():
    if found(MP_FOR):
        controlvariable()
        consume(MP_ASSIGN)
        initialvalue()
        stepvalue()
        finalvalue()
        consume(MP_DO)
        statement()
        
def controlvariable():
    variableidentifier()
    
def initialvalue():
    ordinalexpression()
    
def stepvalue():
    if found(MP_TO):
        #not sure what else would happen after it is matched
    elif found(MP_DOWNTO):
        # "" "" 
        
def finalvalue():
    ordinalexpression()
    
def procedurestatement():
    procedureidentifier()
    optionalactualparameterlist()
    
def optionalactualparameterlist():
    if found(MP_LPAREN):
        actualparameter()
        actualparametertail()
        consume(MP_RPAREN)
    elif found(EPSILON):
        #something
        
def actualparametertail():
    if found(MP_COMMA):
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
    #epsilon
    
def relationaloperator():
    if found(MP_EQUAL):
    elif found(MP_LTHAN):
    elif found(MP_GTHAN):
    elif found(MP_LEQUAL):
    elif found(MP_GEQUAL):
    elif found(MP_NEQUAL):
        
def simpleexpression():
    optionalsign()
    term()
    termtail()
    
def termtail():
    addingoperator()
    term()
    termtail()
    #epsilon
    
def optionalsign():
    if found(MP_PLUS):
    elif found(MP_MINUS):
    
def addingoperator():
    if found(MP_PLUS):
    elif found(MP_MINUS):
    elif found(MP_OR):
        
def term():
    factor()
    factortail()
    
def factortail():
    multiplyingoperator()
    factor()
    factortail()
    
def multiplyingoperator():
    if found(MP_TIMES):
    elif found(MP_FLOAT_DIVIDE):
    elif found(MP_DIV):
    elif found(MP_MOD):
    elif found(MP_AND):
        
def factor():
    unsignedinteger()
    unsignedfloat()
    stringliteral()
    if found(MP_TRUE):
    elif found(MP_FALSE):
    elif found(MP_NOT):
        factor
    elif found(MP_LPAREN):
        expression
        consume(MP_RPAREN)
    functionidentifier()
    optionalactualparameterlist()
    
def programidentifier():
    consume(IDENTIFIER_CHARS)
    
def variableidentifier():
    consume(IDENTIFIER_CHARS)
    
def procedureidentifier():
    consume(IDENTIFIER_CHARS)
    
def functionidentifier():
    consume(IDENTIFIER_CHARS)
    
def booleanexpression():
    expression()
    
def ordinalexpression():
    expression()
    
def identifierlist():
    consume(IDENTIFIER_CHARS)
    identifiertail()
    
def identifiertail():
    if found(MP_COMMA):
        consume(IDENTIFIER_CHARS)
        identifiertail()
    elif found(ESPILON):
        #something
        

        
        





        