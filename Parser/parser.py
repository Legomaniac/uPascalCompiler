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

<<<<<<< HEAD
def parse(sourceText):
    global scanner 
=======
 def parse(sourceText):
	global scanner
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
	# create a Lexer object & pass it the sourceText
    scanner.initialize(sourceText)
    getToken()
    program()

def getToken():
<<<<<<< HEAD
	global token 
	token  = scanner.getToken()
=======
	global token
	token  = scanner.get()
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
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
<<<<<<< HEAD
    if match(types.MP_EOF):
        pass

=======
    program()
    expect(MP_EOF)
"""
Rule 2:
Program -> ProgramHeading ";" Block "."
"""
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
def program():
    programHeading()
    expect(types.MP_SCOLON)
    block()
<<<<<<< HEAD
    expect(types.MP_PERIOD)

def programHeading():
    expect(types.MP_PROGRAM)
    programIdentifier()
=======
    expect(MP_PERIOD)
"""
Rule 3:
ProgramHeading -> "program" ProgramIdentifier
"""
def programHeading():
    if match(MP_PROGRAM):
         programIdentifier()
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

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
<<<<<<< HEAD
    pass
=======
    variableDeclaration()
    expect("MP_SCOLON")
    variableDeclarationTail()
    if match(EPSILON):
        pass
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 9:
VariableDeclaration -> IdentifierList ":" Type
"""
def variableDeclaration():
<<<<<<< HEAD
    pass
    
def Type():
    pass

def procedureAndFunctionDeclarationPart():
    pass
=======
    identifierList()
    expect(MP_COLON)
    type()
"""
Rule 10, 11, 12 and 13:
Type -> "Integer"
     -> "Float"
     -> "String"
     -> "Boolean"
"""
def type():
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 17:
ProcedureDeclaration -> ProcedureHeading ";" Block ";"
"""
def procedureDeclaration():
<<<<<<< HEAD
    pass
=======
    procedureHeading()
    expect(MP_SCOLON)
    block()
    expect(MP_SCOLON)
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 18:
FunctionDeclaration -> FunctionHeading ";" Block ";"
"""
def functionDeclaration():
<<<<<<< HEAD
    pass
=======
    functionHeading()
    expect(MP_SCOLON)
    block()
    expect(MP_SCOLON)
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 19:
ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
"""
def procedureHeading():
<<<<<<< HEAD
    pass

def functionHeading():
    pass

def optionalFormalParameterList():
    pass
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 23 and 24:
FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                           -> epsilon
"""
def formalParameterSectionTail():
<<<<<<< HEAD
    pass
=======
    if match(MP_SCOLON):
        formalParameterSection()
        formalParameterSectionTail()
    elif match(EPSILON):
        pass
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 25 and 26:
FormalParameterSection -> ValueParameterSection
                       -> VariableParameterSection
"""
def formalParameterSection():
<<<<<<< HEAD
    pass
=======
    valueParameterSection()
    variableParameterSection()
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 27:
ValueParameterSection -> IdentifierList ":" Type
"""
def valueParameterSection():
<<<<<<< HEAD
    pass

def variableParameterSection():
    pass

def statementPart():
    pass
=======
    identifierList()
    expect(MP_COLON)
    type()

"""
Rule 28:
VariableParameterSection -> "var" IdentifierList ":" Type
"""
def variableParameterSection():
    if match(MP_VAR):
        identifierList()
        expect(MP_COLON)
        type()

"""
Rule 29:
StatementPart -> CompoundStatement
"""
def statementPart():
    compoundStatement()
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 30:
CompoundStatement -> "begin" StatementSequence "end"
"""
def compoundStatement():
<<<<<<< HEAD
    pass

def statementSequence():
    pass

def statementTail():
    pass
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

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
<<<<<<< HEAD
    pass

=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
def emptyStatement():
    pass

"""
Rule 45:
ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
"""
def readStatement():
<<<<<<< HEAD
    pass
=======
    if match(MP_READ):
        expect(MP_LPAREN)
        readParameter()
        readParameterTail()
        expect(MP_RPAREN)
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 46 and 47:
ReadParameterTail -> "," ReadParameter ReadParameterTail
                  -> epsilon
"""
def readParameterTail():
<<<<<<< HEAD
    pass
=======
    if match(MP_COMMA):
        readParameter()
        readParameterTail()
    elif match(EPSILON):
        pass
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 48:
ReadParameter -> VariableIdentifier
"""
def readParameter():
<<<<<<< HEAD
    pass
=======
    variableIdentifier()
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 49 and 50:
WriteStatement -> "write"  "(" WriteParameter WriteParameterTail ")"
               -> "writeln" "(" WriteParameter WriteParameterTail ")"
"""
def writeStatement():
<<<<<<< HEAD
    pass
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 51 and 52:
WriteParameterTail -> "," WriteParameter WriteParameterTail
                   -> epsilon
"""
def writeParameterTail():
<<<<<<< HEAD
    pass

def writeParameter():
    pass
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a

"""
Rule 54 and 55:
AssignmentStatement -> VariableIdentifier ":=" Expression
                    -> FunctionIdentifier ":=" Expression
"""
def assignmentStatement():
<<<<<<< HEAD
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
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
        statement()
    elif match(types.EPSILON):
        pass
<<<<<<< HEAD
    
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
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
        pass
    elif match(types.MP_DOWNTO):
        pass
<<<<<<< HEAD
        
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
=======

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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
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
<<<<<<< HEAD
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
        
=======
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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
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
<<<<<<< HEAD
    
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
=======

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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
    expression()

"""
Rule 112:
OrdinalExpression -> Expression
"""
def ordinalExpression():
    expression()
<<<<<<< HEAD
    
def identifierlist():
    expect(types.IDENTIFIER_CHARS)
    identifiertail()
    
def identifiertail():
    if match(types.MP_COMMA):
        expect(types.IDENTIFIER_CHARS)
        identifiertail()
    elif match(types.EPSILON):
=======

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
>>>>>>> 5cb4f159e5068305fa319777ad5dcd72b151a31a
        pass
