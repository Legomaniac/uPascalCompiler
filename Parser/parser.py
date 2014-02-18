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
# Section from James
#-----------------------------------

"""
Rule 1:
SystemGoal -> Program EOF
"""
def systemGoal():
    if match(types.MP_EOF):
        pass

=======
    program()
    expect(MP_EOF)
"""
Rule 2:
Program -> ProgramHeading ";" Block "."
"""
def program():
    programHeading()
    expect(types.MP_SCOLON)
    block()
    expect(types.MP_PERIOD)

def programHeading():
    expect(types.MP_PROGRAM)
    programIdentifier()
    expect(MP_PERIOD)
"""
Rule 3:
ProgramHeading -> "program" ProgramIdentifier
"""
def programHeading():
    if match(MP_PROGRAM):
         programIdentifier()

"""
Rule 4:
Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
"""
def block():
    variableDeclarationPart()
    procedureAndFunctionDeclarationPart()
    statementPart()

"""
Rule 5 and 6:
VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
                        -> epsilon
"""
def variableDeclarationPart():
    if match(types.MP_VAR):
        variableDeclaration()
        expect(types.MP_SCOLON)
        variableDeclarationTail()
    elif match(types.EPSILON):
        pass
"""
Rule 7 and 8:
VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail
                        -> epsilon
"""
def variableDeclarationTail():
    variableDeclaration()
    expect("MP_SCOLON")
    variableDeclarationTail()
    if match(EPSILON):
        pass
"""
Rule 9:
VariableDeclaration -> IdentifierList ":" Type
"""
def variableDeclaration():
    identifierList()
    expect(MP_COLON)
    Type()
"""
Rule 10, 11, 12 and 13:
Type -> "Integer"
     -> "Float"
     -> "String"
     -> "Boolean"
"""
def Type():
    if match(MP_INTEGER_LIT):
    elif match(MP_FLOAT_LIT):
    elif match(MP_STRING_LIT):
    elif match(MP_BOOLEAN):
"""
Rule 14, 15 and 16:
ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
                                    -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
                                    -> epsilon
"""
def procedureAndFunctionDeclarationPart():
    procedureDeclaration()
    procedureAndFunctionDeclarationPart()
    functionDeclaration()
    procedureAndFunctionDeclarationPart()
    if match(EPSILON):
        pass
"""
Rule 17:
ProcedureDeclaration -> ProcedureHeading ";" Block ";"
"""
def procedureDeclaration():
    procedureHeading()
    expect(MP_SCOLON)
    block()
    expect(MP_SCOLON)
"""
Rule 18:
FunctionDeclaration -> FunctionHeading ";" Block ";"
"""
def functionDeclaration():
    functionHeading()
    expect(MP_SCOLON)
    block()
    expect(MP_SCOLON)
"""
Rule 19:
ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
"""
def procedureHeading():
    if match(MP_PROCEDURE):
        procedureIdentifier()
        optionalFormalParameterList()
"""
Rule 20:
FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList Type
"""
def functionHeading():
    if match(MP_FUNCTION):
        functionIdentifier()
        optionalFormalParameterList()
        type()

"""
Rule 21 and 22:
OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                            -> epsilon
"""
def optionalFormalParameterList():
    if match(MP_LPAREN):
        formalParameterSection()
        formalParameterSectionTail()
        expect(MP_RPAREN)
    elif match(EPSILON):
        pass
"""
Rule 23 and 24:
FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                           -> epsilon
"""
def formalParameterSectionTail():
    if match(MP_SCOLON):
        formalParameterSection()
        formalParameterSectionTail()
    elif match(EPSILON):
        pass
"""
Rule 25 and 26:
FormalParameterSection -> ValueParameterSection
                       -> VariableParameterSection
"""
def formalParameterSection():
    valueParameterSection()
    variableParameterSection()
"""
Rule 27:
ValueParameterSection -> IdentifierList ":" Type
"""
def valueParameterSection():
    identifierList()
    expect(MP_COLON)
    Type()

"""
Rule 28:
VariableParameterSection -> "var" IdentifierList ":" Type
"""
def variableParameterSection():
    if match(MP_VAR):
        identifierList()
        expect(MP_COLON)
        Type()
"""
Rule 29:
StatementPart -> CompoundStatement
"""
def statementPart():
    compoundStatement()
"""
Rule 30:
CompoundStatement -> "begin" StatementSequence "end"
"""
def compoundStatement():
    if match(MP_BEGIN):
        statementSequence()
        expect(MP_END)
"""
Rule 31:
StatementSequence -> Statement StatementTail
"""
def statementSequence():
    statement()
    statementTail()

"""
Rule 32 and 33:
StatementTail -> ";" Statement StatementTail
              -> epsilon
"""
def statementTail():
    if match(MP_SCOLON):
        statement()
        statementTail()
    elif match(EPSILON):
        pass
"""
Rule 34, 35, 36, 37, 38, 39, 40, 41, 42, and 43:
Statement -> EmptyStatement
          -> CompoundStatement
          -> ReadStatement
          -> WriteStatement
          -> AssignmentStatement
          -> IfStatement
          -> WhileStatement
          -> RepeatStatement
          -> ForStatement
          -> ProcedureStatement
"""
def statement():
    emptyStatement()
    compoundStatement()
    readStatement()
    writeStatement()
    assignmentStatement()
    ifStatement()
    whileStatement()
    repeatStatement()
    forStatement()
    procedureStatement()
"""
Rule 44:
EmptyStatement -> epsilon
"""
def emptyStatement():
    pass

"""
Rule 45:
ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
"""
def readStatement():
    if match(MP_READ):
        expect(MP_LPAREN)
        readParameter()
        readParameterTail()
        expect(MP_RPAREN)
"""
Rule 46 and 47:
ReadParameterTail -> "," ReadParameter ReadParameterTail
                  -> epsilon
"""
def readParameterTail():
    if match(MP_COMMA):
        readParameter()
        readParameterTail()
    elif match(EPSILON):
        pass
"""
Rule 48:
ReadParameter -> VariableIdentifier
"""
def readParameter():
    variableIdentifier()
"""
Rule 49 and 50:
WriteStatement -> "write"  "(" WriteParameter WriteParameterTail ")"
               -> "writeln" "(" WriteParameter WriteParameterTail ")"
"""
def writeStatement():
    if match(MP_WRITE):
        expect(MP_LPAREN)
        writeParameter()
        writeParameterTail()
        expect(MP_RPAREN)
    elif match(MP_WRITELN):
        expect(MP_LPAREN)
        writeParameter()
        writeParameterTail()
        expect(MP_RPAREN)
"""
Rule 51 and 52:
WriteParameterTail -> "," WriteParameter WriteParameterTail
                   -> epsilon
"""
def writeParameterTail():
    if match(MP_COMMA):
        writeParameter()
        writeParameterTail()
    elif match(EPSILON):
        pass
"""
Rule 53:
WriteParameter -> OrdinalExpression
"""
def writeParameter():
    ordinalExpression()
"""
Rule 54 and 55:
AssignmentStatement -> VariableIdentifier ":=" Expression
                    -> FunctionIdentifier ":=" Expression
"""
def assignmentStatement():
    variableIdentifier()
    expect(MP_ASSIGN)
    expression()
    functionIdentifier()
    expect(MP_ASSIGN)
    expression()

#-----------------------------------
# Section from Justin
#-----------------------------------
"""
Rule 56:
IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
"""
def ifStatement():
    if match(MP_IF):
        booleanExpression()
        expect(MP_THEN)
        statement()
        optionalElsePart()

"""
Rule 57 and 58:
OptionalElsePart -> "else" Statement
                 -> epsilon
"""
def optionalElsePart():
    if match(MP_ELSE):
        statement()
    elif match(types.EPSILON):
        pass
"""
Rule 59:
RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
"""
def repeatStatement():
    if match(MP_REPEAT):
        statementSequence()
        expect(MP_UNTIL)
        booleanExpression()
"""
Rule 60:
WhileStatement -> "while" BooleanExpression "do" Statement
"""
def whileStatement():
    if match(MP_WHILE):
        booleanExpression()
        expect(MP_DO)
        statement()

"""
Rule 61:
ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
"""
def forStatement():
    if match(MP_FOR):
        controlVariable()
        expect(MP_ASSIGN)
        initialValue()
        stepValue()
        finalValue()
        expect(MP_DO)
        statement()

"""
Rule 62:
ControlVariable -> VariableIdentifier
"""
def controlVariable():
    variableIdentifier()

"""
Rule 63:
InitialValue -> OrdinalExpression
"""
def initialValue():
    ordinalExpression()

"""
Rule 64 and 65:
StepValue -> "to"
          -> "downto"
"""
def stepValue():
    if match(MP_TO):
        pass
    elif match(types.MP_DOWNTO):
        pass
"""
Rule 66:
FinalValue -> OrdinalExpression
"""
def finalValue():
    ordinalExpression()

"""
Rule 67:
ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
"""
def procedureStatement():
    procedureIdentifier()
    optionalActualParameterList()

"""
Rule 68 and 69:
OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
                            -> epsilon
"""
def optionalActualParameterList():
    if match(MP_LPAREN):
        actualParameter()
        actualParameterTail()
        expect(MP_RPAREN)
    elif match(EPSILON):
        pass
"""
Rule 70 and 71:
ActualParameterTail -> ","  ActualParameter ActualParameterTail
"""
def actualParameterTail():
    if match(MP_COMMA):
        actualParameter()
        actualParameterTail()

"""
Rule 72:
ActualParameter -> OrdinalExpression
"""
def actualParameter():
    ordinalExpression()

"""
Rule 73:
Expression -> SimpleExpression OptionalRelationalPart
"""
def expression():
    simpleExpression()
    optionalRelationalPart()
"""
Rule 74 and 75:
OptionalRelationalPart -> RelationalOperator SimpleExpression
                       -> epsilon
"""
def optionalRelationalPart():
    relationalOperator()
    simpleExpression()
    if match(EPSILON):
        pass

"""
Rule 76, 77, 78, 79, 80 and 81:
RelationalOperator -> "="
                   -> "<"
                   -> ">"
                   -> "<="
                   -> ">="
                   -> "<>"
"""
def relationalOperator():
    if match(MP_EQUAL):
    elif match(MP_LTHAN):
    elif match(MP_GTHAN):
    elif match(MP_LEQUAL):
    elif match(MP_GEQUAL):
    elif match(MP_NEQUAL):

"""
Rule 82:
SimpleExpression -> OptionalSign Term TermTail
"""
def simpleExpression():
    optionalSign()
    term()
    termTail()

"""
Rule 83 and 84:
TermTail -> AddingOperator Term TermTail
         -> epsilon
"""
def termTail():
    addingOperator()
    term()
    termTail()
    if match(EPSILON):
        pass

"""
Rule 85, 86 and 87:
OptionalSign -> "+"
             -> "-"
             -> epsilon
"""
def optionalSign():
    if match(MP_PLUS):
    elif match(MP_MINUS):

"""
Rule 88, 89 and 90:
AddingOperator -> "+"
               -> "-"
               -> "or"
"""
def addingOperator():
    if match(MP_PLUS):
    elif match(MP_MINUS):
    elif match(MP_OR):

"""
Rule 91:
Term -> Factor FactorTail
"""
def term():
    factor()
    factorTail()
"""
Rule 92 and 93:
FactorTail -> MultiplyingOperator Factor FactorTail
           -> epsilon
"""
def factorTail():
    multiplyingOperator()
    factor()
    factortail()
"""
Rule 94, 95, 96, 97 and 98:
MultiplyingOperator -> "*"
                    -> "/"
                    -> "div"
                    -> "mod"
                    -> "and"
"""
def multiplyingOperator():
    if match(MP_TIMES):
    elif match(MP_FLOAT_DIVIDE):
    elif match(MP_DIV):
    elif match(MP_MOD):
    elif match(MP_AND):
"""
Rule 99, 100, 101, 102, 103, 104, 105 and 106:
Factor -> UnsignedInteger
       -> UnsignedFloat
       -> StringLiteral
       -> "True"
       -> "False"
       -> "not" Factor
       -> "("Expression ")"
       -> FunctionIdentifier OptionalActualParameterList
"""
def factor():
    unsignedInteger()
    unsignedFloat()
    stringLiteral()
    if match(MP_TRUE):
    elif match(MP_FALSE):
    elif match(MP_NOT):
        factor
    elif match(MP_LPAREN):
        expression
        expect(MP_RPAREN)
    functionIdentifier()
    optionalactualparameterlist()
"""
Rule 107:
ProgramIdentifier -> Identifier
"""
def programIdentifier():
    expect(IDENTIFIER_CHARS)
"""
Rule 108:
VariableIdentifier -> Identifier
"""
def variableIdentifier():
    expect(IDENTIFIER_CHARS)
"""
Rule 109:
ProcedureIdentifier -> Identifier
"""
def procedureIdentifier():
    expect(IDENTIFIER_CHARS)
"""
Rule 110:
FunctionIdentifier -> Identifier
"""
def functionIdentifier():
    expect(IDENTIFIER_CHARS)
"""
Rule 111:
BooleanExpression -> Expression
"""
def booleanExpression():
    expression()
"""
Rule 112:
OrdinalExpression -> Expression
"""
def ordinalExpression():
    expression()

"""
Rule 113:
IdentifierList -> Identifier IdentifierTail
"""
def identifierList():
    expect(IDENTIFIER_CHARS)
    identifierTail()

"""
Rule 114 and 115:
IdentifierList -> "," Identifier IdentifierTail
               -> epsilon
"""
def identifierTail():
    if match(MP_COMMA):
        expect(IDENTIFIER_CHARS)
        identifierTail()
    elif match(EPSILON):
        pass
