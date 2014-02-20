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
# --------------------------------------------------------------
def parse(sourceText):
    global scanner
    scanner.initialize(sourceText)
    getToken()
    systemGoal()

def getToken():
	global token 
	token = scanner.getToken()
	print ( ("  " * indent) + " * " + token.show())

# --------------------------------------------------------------

def error(msg):
    sys.exit("Parse Error " + token.getErrorMsg(msg))

def matchOneOf(tempTokenTypes):
	for tempTokenType in tempTokenTypes:
		print "matchOneOf", tempTokenType, token.type
		if token.type == tempTokenType:
			return True
	return False

def match(tempTokenType):
    if token.type == tempTokenType:
        getToken()
        return True
    else:
        return False

def expect(*args):
	for tempTokenType in args:
		if token.type == tempTokenType:
			getToken()
			return True
	error("Expected to find "
		+ dq(str(args))
		+ " but instead found: "
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
    program()
    expect(types.MP_EOF)
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
    expect(types.MP_PERIOD)
"""
Rule 3:
ProgramHeading -> "program" ProgramIdentifier
"""
def programHeading():
    if match(types.MP_PROGRAM):
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
    elif match(EPSILON):
        pass
"""
Rule 7 and 8:
VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail
                        -> epsilon
"""
def variableDeclarationTail():
    variableDeclaration()
    expect(types.MP_SCOLON)
    variableDeclarationTail()
    if match(EPSILON):
        pass
"""
Rule 9:
VariableDeclaration -> IdentifierList ":" Type
"""
def variableDeclaration():
    identifierList()
    expect(types.MP_COLON)
    Type()
"""
Rule 10, 11, 12 and 13:
Type -> "Integer"
     -> "Float"
     -> "String"
     -> "Boolean"
"""
def Type():
    if match(types.MP_INTEGER_LIT):
        pass
    elif match(types.MP_FLOAT_LIT):
        pass
    elif match(types.MP_STRING_LIT):
        pass
    elif match(types.MP_BOOLEAN):
        pass
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
    expect(types.MP_SCOLON)
    block()
    expect(types.MP_SCOLON)
"""
Rule 18:
FunctionDeclaration -> FunctionHeading ";" Block ";"
"""
def functionDeclaration():
    functionHeading()
    expect(types.MP_SCOLON)
    block()
    expect(types.MP_SCOLON)
"""
Rule 19:
ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
"""
def procedureHeading():
    if match(types.MP_PROCEDURE):
        procedureIdentifier()
        optionalFormalParameterList()
"""
Rule 20:
FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList Type
"""
def functionHeading():
    if match(types.MP_FUNCTION):
        functionIdentifier()
        optionalFormalParameterList()
        type()

"""
Rule 21 and 22:
OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                            -> epsilon
"""
def optionalFormalParameterList():
    if match(types.MP_LPAREN):
        formalParameterSection()
        formalParameterSectionTail()
        expect(types.MP_RPAREN)
    elif match(EPSILON):
        pass
"""
Rule 23 and 24:
FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                           -> epsilon
"""
def formalParameterSectionTail():
    if match(types.MP_SCOLON):
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
    expect(types.MP_COLON)
    Type()

"""
Rule 28:
VariableParameterSection -> "var" IdentifierList ":" Type
"""
def variableParameterSection():
    if match(types.MP_VAR):
        identifierList()
        expect(types.MP_COLON)
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
    if match(types.MP_BEGIN):
        statementSequence()
        expect(types.MP_END)
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
    if match(types.MP_SCOLON):
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
    if match(types.MP_READ):
        expect(types.MP_LPAREN)
        readParameter()
        readParameterTail()
        expect(types.MP_RPAREN)
"""
Rule 46 and 47:
ReadParameterTail -> "," ReadParameter ReadParameterTail
                  -> epsilon
"""
def readParameterTail():
    if match(types.MP_COMMA):
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
    if match(types.MP_WRITE):
        expect(types.MP_LPAREN)
        writeParameter()
        writeParameterTail()
        expect(types.MP_RPAREN)
    elif match(types.MP_WRITELN):
        expect(types.MP_LPAREN)
        writeParameter()
        writeParameterTail()
        expect(types.MP_RPAREN)
"""
Rule 51 and 52:
WriteParameterTail -> "," WriteParameter WriteParameterTail
                   -> epsilon
"""
def writeParameterTail():
    if match(types.MP_COMMA):
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
    expect(types.MP_ASSIGN)
    expression()
    functionIdentifier()
    expect(types.MP_ASSIGN)
    expression()

#-----------------------------------
# Section from Justin
#-----------------------------------
"""
Rule 56:
IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
"""
def ifStatement():
    if match(types.MP_IF):
        booleanExpression()
        expect(types.MP_THEN)
        statement()
        optionalElsePart()

"""
Rule 57 and 58:
OptionalElsePart -> "else" Statement
                 -> epsilon
"""
def optionalElsePart():
    if match(types.MP_ELSE):
        statement()
    elif match(EPSILON):
        pass
"""
Rule 59:
RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
"""
def repeatStatement():
    if match(types.MP_REPEAT):
        statementSequence()
        expect(types.MP_UNTIL)
        booleanExpression()
"""
Rule 60:
WhileStatement -> "while" BooleanExpression "do" Statement
"""
def whileStatement():
    if match(types.MP_WHILE):
        booleanExpression()
        expect(types.MP_DO)
        statement()

"""
Rule 61:
ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
"""
def forStatement():
    if match(types.MP_FOR):
        controlVariable()
        expect(types.MP_ASSIGN)
        initialValue()
        stepValue()
        finalValue()
        expect(types.MP_DO)
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
    if match(types.MP_TO):
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
    if match(types.MP_LPAREN):
        actualParameter()
        actualParameterTail()
        expect(types.MP_RPAREN)
    elif match(EPSILON):
        pass
"""
Rule 70 and 71:
ActualParameterTail -> ","  ActualParameter ActualParameterTail
"""
def actualParameterTail():
    if match(types.MP_COMMA):
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
    if match(types.MP_PLUS):
        pass
    elif match(types.MP_MINUS):
        pass
    elif match(EPSILON):
        pass

"""
Rule 88, 89 and 90:
AddingOperator -> "+"
               -> "-"
               -> "or"
"""
def addingOperator():
    if match(types.MP_PLUS):
        pass
    elif match(types.MP_MINUS):
        pass
    elif match(types.MP_OR):
        pass

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
    if match(types.MP_TRUE):
        pass
    elif match(types.MP_FALSE):
        pass
    elif match(types.MP_NOT):
        factor()
    elif match(types.MP_LPAREN):
        expression()
        expect(types.MP_RPAREN)
    functionIdentifier()
    optionalactualparameterlist()
"""
Rule 107:
ProgramIdentifier -> Identifier
"""
def programIdentifier():
    expect(types.MP_IDENTIFIER)
"""
Rule 108:
VariableIdentifier -> Identifier
"""
def variableIdentifier():
    expect(types.MP_IDENTIFIER)
"""
Rule 109:
ProcedureIdentifier -> Identifier
"""
def procedureIdentifier():
    expect(types.MP_IDENTIFIER)
"""
Rule 110:
FunctionIdentifier -> Identifier
"""
def functionIdentifier():
    expect(types.MP_IDENTIFIER)
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
    expect(types.MP_IDENTIFIER)
    identifierTail()

"""
Rule 114 and 115:
IdentifierList -> "," Identifier IdentifierTail
               -> epsilon
"""
def identifierTail():
    if match(types.MP_COMMA):
        expect(types.MP_IDENTIFIER)
        identifierTail()
    elif match(EPSILON):
        pass
