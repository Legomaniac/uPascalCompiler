#parser.py
import sys
from leaf import Leaf
sys.path.insert(0, '../')
from tokens import *
from recordTypes import recTypes
import scanner as scanner
sys.path.insert(0, '/Symbol/')
import Symbol.symbolTable as SymbolTable
import Analyzer.analyzer as analyzer

class ParsingError(Exception): pass

# Use 2 look aheads for parsing
branch = 1
lookAhead = None
lookAhead2 = None
indent = 0
SymbolStack = []

def dq(s): return '"%s"' %s
# --------------------------------------------------------------
# Parser Functions
# --------------------------------------------------------------
def parse(sourceText):
    global scanner, lookAhead, lookAhead2, branch
    scanner.initialize(sourceText)
    lookAhead = getToken()
    lookAhead2 = getToken()
    systemGoal()

def getToken():
	lookAhead = lookAhead2
    lookAhead2 = scanner.getToken()

def semError(msg):
    sys.exit("Semantic Error: " + str(msg))

def matchError(expToken):
    print "Match error found on line: " + lookAhead.getLineNumber() + ", column: "
        + lookAhead.getColumnNumber() + ":: expected '" + expToken
        + "', instead found '" + lookAhead.getLexeme() + "'"

def syntaxError(expToken):
    sys.exit("Syntax error found on line: " + lookAhead.getLineNumber() + ", column: "
        + lookAhead.getColumnNumber() + ":: expected '" + expToken
        + "', instead found '" + lookAhead.getLexeme() + "'")
    
def semanticError(msg):
    sys.exit("Semantic Error: " + str(msg))

def match(tempTokenType):
    if lookAhead.type == tempTokenType:
        getToken()
    else:
        matchError(str(tempTokenType))

def Lambda():
    #Dummy function to extend lambda rules
    #print "Extending lambda rule."
# --------------------------------------------------------------
# Symbol Table Stack Stuff
# --------------------------------------------------------------
def getBranch():
    num = branch
    branch += 1
    return "L" + num

def addSymbolTable(scopeName, branchLabel):
    exists = false
    for t in SymbolStack:
        if t.getScopeName() == scopeName:
            exists = true
            break
    
    if not exists:
        SymbolStack.append(symbolTable(scopeName, branchLabel))
        return true
    else:
        semanticError("Symbol table with name: " + scopeName + " already exists")
        return false
    
def removeSymbolTable():
    SymbolStack.pop()
    SymbolTable.decrementNestingLevel()
    
def printSymbolTables():
    for t in SymbolStack:
        t.printTable()

#-----------------------------------
# CFG Definitions
#-----------------------------------

"""
Rule 1:
SystemGoal -> Program EOF
"""
def systemGoal():
    if lookAhead.getType == types.MP_PROGRAM:
        program()
        match(types.MP_EOF)
    else:
        syntaxError("program")
"""
Rule 2:
Program -> ProgramHeading ";" Block "."
"""
def program():
    if lookAhead.getType == types.MP_PROGRAM:
        scopeName = programHeading()
        branch = getBranch()
        record = {'type':recTypes.LABEL, 'label':branch}
        addSymbolTable(scopeName, branch)
        SymbolStack[-1].addDataSymbolsToTable("DISREG", "Old Disreg value", {'type':types.MP_STRING, 'mode':"VALUE"})
        match(types.MP_SCOLON)
        analyzer.genBR(record)
        #The whole thing
        block(scopeName, {'type':recTypes.BLOCK, 'block':"program"}, record)
        #Last token before EOF
        match(types.MP_PERIOD)
    else:
        syntaxError("program")
"""
Rule 3:
ProgramHeading -> "program" ProgramIdentifier
"""
def programHeading():
    if lookAhead.getType == types.MP_PROGRAM:
        match(types.MP_PROGRAM)
        name = programIdentifier()
        return name
    else:
        syntaxError("program")
"""
Rule 4:
Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
"""
def block(scope, blockType, label):
    if lookAhead.getType == types.MP_VAR:
        variableDeclarationPart()
        nameRecord = {'type':recTypes.SYMBOL_TABLE, 'scope':scope, 'nestingLevel':SymbolStack[-1].getNestingLevel(), 'size':SymbolStack[-1].getTableSize()}
        procedureAndFunctionDeclarationPart()
        analyzer.genLabel(label)
        statementPart()
    else:
        syntaxError("var, begin, function, procedure")
"""
Rule 5 and 6:
VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
                        -> Lambda
"""
def variableDeclarationPart():
    if lookAhead.getType == types.MP_VAR:
        match(types.MP_VAR)
        variableDeclaration()
        match(types.MP_SCOLON)
        variableDeclarationTail()
    elif lookAhead.getType == types.MP_BEGIN or \
        lookAhead.getType == types.MP_FUNCTION or \
        lookAhead.getType == types.MP_PROCEDURE:
            Lambda()
    else:
        syntaxError("var, begin, function, procedure")
"""
Rule 7 and 8:
VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail
                        -> Lambda
"""
def variableDeclarationTail():
    if lookAhead.getType == types.MP_VAR:
        variableDeclaration()
        match(types.MP_SCOLON)
        variableDeclarationTail()
    elif lookAhead.getType == types.MP_BEGIN or \
        lookAhead.getType == types.MP_FUNCTION or \
        lookAhead.getType == types.MP_PROCEDURE:
            Lambda()
    else:
        syntaxError("identifier, begin, procedure, function")
"""
Rule 9:
VariableDeclaration -> IdentifierList ":" Type
"""
def variableDeclaration():
    if lookAhead.getType == types.MP_IDENTIFIER:
        idList = identifierList()
        match(types.MP_COLON)
        Type()
        SymbolStack[-1].addDataSymbolsToTable("VARIABLE", idList, {'type':"t", 'mode':None})
    else:
        syntaxError("identifier")
"""
Rule 10, 11, 12 and 13:
Type -> "Integer"
     -> "Float"
     -> "String"
     -> "Boolean"
"""
def Type():
    if lookAhead.getType == types.MP_INTEGER:
        match(types.MP_INTEGER)
        curType = types.MP_INTEGER
    elif lookAhead.getType == types.MP_FLOAT:
        match(types.MP_FLOAT)
        curType = types.MP_FLOAT
    elif lookAhead.getType == types.MP_STRING:
        match(types.MP_STRING)
        curType = types.MP_STRING
    elif lookAhead.getType == types.MP_BOOLEAN:
        match(types.MP_BOOLEAN)
        curType = types.MP_BOOLEAN
    else:
        syntaxError("integer, float, string, boolean")
    return curType
"""
Rule 14, 15 and 16:
ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
                                    -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
                                    -> Lambda
"""
def procedureAndFunctionDeclarationPart():
    if lookAhead.getType == types.MP_PROCEDURE:
        procedureDeclaration()
        procedureAndFunctionDeclarationPart()
    elif lookAhead.getType == types.MP_FUNCTION:
        functionDeclaration()
        procedureAndFunctionDeclarationPart()
    elif lookAhead.getType == types.MP_BEGIN:
        Lambda()
    else:
        syntaxError("procedure, function")
"""
Rule 17:
ProcedureDeclaration -> ProcedureHeading ";" Block ";"
"""
def procedureDeclaration():
    branch = getBranch()
    if lookAhead.getType == types.MP_PROCEDURE:
        procedureID = procedureHeading(branch)
        match(types.MP_SCOLON)
        block(procedureID)
        match(types.MP_SCOLON)
        printSymbolTables()
        removeSymbolTable()
    else:
        sytaxError("procedure")
"""
Rule 18:
FunctionDeclaration -> FunctionHeading ";" Block ";"
"""
def functionDeclaration():
    branch = getBranch()
    if lookAhead.getType == types.MP_FUNCTION:
        functionID = functionHeading(branch)
        match(types.MP_SCOLON)
        block(functionID)
        match(types.MP_SCOLON)
        printSymbolTables()
        removeSymbolTable()
    else:
        syntaxError("function")
"""
Rule 19:
ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
"""
def procedureHeading(branchLbl):
    attributes = []
    ids = []
    if lookAhead.getType == types.MP_PROCEDURE:
        match(types.MP_PROCEDURE)
        procID = procedureIdentifier()
        parameters = optionalFormalParameterList()
        for p in parameters:
            attributes.append(p.getAttribute)
            ids.append(p.getLexeme)
        SymbolStack[0].addModuleSymbolsToTable("PROCEDURE", procID, null, attributes, branchLbl)
        addSymbolTable(procID, branchLbl)
        SymbolStack[0].addDataSymbolsToTable("DISREG", "Old Display Register Value", {type:"STRING", mode:"VALUE"})
        SymbolStack[0].addDataSymbolsToTable("PARAMETER", ids, attributes)
        SymbolStack[0].addDataSymbolsToTable("RETADDR", "Caller's Return Address", {type:"STRING", mode:"VALUE"})
    else:
        syntaxError("procedure")
    return procID
"""
Rule 20:
FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
"""
def functionHeading():
    attributes = []
    ids = []
    if lookAhead.getType == types.MP_FUNCTION:
        match(types.MP_FUNCTION)
        funcID = functionIdentifier()
        parameters = optionalFormalParameterList()
        for p in parameters:
            attributes.append(p.getAttribute)
            ids.append(p.getLexeme)
        match(types.MP_COLON)
        functionType = Type()
        SymbolStack[0].addModuleSymbolsToTable("FUNCTION", funcID, functionType, attributes, branchLbl)
        addSymbolTable(procID, branchLbl)
        SymbolStack[0].addDataSymbolsToTable("DISREG", "Old Display Register Value", {type:"STRING", mode:"VALUE"})
        SymbolStack[0].addDataSymbolsToTable("PARAMETER", ids, attributes)
        SymbolStack[0].addDataSymbolsToTable("RETADDR", "Caller's Return Address", {type:"STRING", mode:"VALUE"})
    else:
        syntaxError("function")
    return funcID
"""
Rule 21 and 22:
OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                            -> Lambda
"""
def optionalFormalParameterList():
    if lookAhead.getType == types.MP_LPAREN:
        match(types.MP_LPAREN)
        parameters = formalParameterSection()
        formalParameterSectionTail(parameters)
        match(types.MP_RPAREN)
    elif lookAhead.getType == types.MP_SCOLON or \
        lookAhead.getType == types.MP_COLON:
        Lambda()
    else:
        syntaxError("(, ;, :")
    return parameters
"""
Rule 23 and 24:
FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                           -> Lambda
"""
def formalParameterSectionTail(parameters):
    if lookAhead.getType == types.MP_SCOLON:
        match(types.MP_SCOLON)
        parameters.extend(formalParameterSection())
        formalParameterSectionTail(parameters)
    elif lookAhead.getType == types.MP_RPAREN:
        Lambda()
    else:
        syntaxError("function, )")
"""
Rule 25 and 26:
FormalParameterSection -> ValueParameterSection
                       -> VariableParameterSection
"""
def formalParameterSection():
    if lookAhead.getType == types.MP_IDENTIFIER:
        parameters = valueParameterSection()
    elif lookAhead.getType == types.MP_VAR:
        parameters = variableParameterSection()
    else:
        syntaxError("identifier, var")
    return parameters
"""
Rule 27:
ValueParameterSection -> IdentifierList ":" Type
"""
def valueParameterSection():
    parameters = []
    if lookAhead.getType == types.MP_IDENTIFIER:
        ids = identifierList()
        match(types.MP_COLON)
        Type = Type()
        for lex in ids:
            parameters.append({lexeme:lex, attribute:{type:Type, mode:"VALUE"}})
    else:
        syntaxError("identifier")
    return parameters
"""
Rule 28:
VariableParameterSection -> "var" IdentifierList ":" Type
"""
def variableParameterSection():
    parameters = []
    if lookAhead.getType == types.MP_VAR:
        match(types.MP_VAR)
        ids = identifierList()
        match(types.MP_COLON)
        Type = Type()
        for lex in ids:
            parameters.append({lexeme:lex, attribute:{type:Type, mode:"VALUE"}})
    else:
        syntaxError("var")
    return parameters
"""
Rule 29:
StatementPart -> CompoundStatement
"""
def statementPart():
    if lookAhead.getType == types.MP_BEGIN:
        compoundStatement()
    else:
        syntaxError("begin")
"""
Rule 30:
CompoundStatement -> "begin" StatementSequence "end"
"""
def compoundStatement():
    if lookAhead.getType == types.MP_BEGIN:
        match(types.MP_BEGIN)
        statementSequence()
        match(types.MP_END)
    else:
        syntaxError("begin")
"""
Rule 31:
StatementSequence -> Statement StatementTail
"""
def statementSequence():
    if lookAhead.getType == types.MP_IDENTIFIER or \
        lookAhead.getType == types.MP_FOR or \
        lookAhead.getType == types.MP_WHILE or \
        lookAhead.getType == types.MP_UNTIL or \
        lookAhead.getType == types.MP_REPEAT or \
        lookAhead.getType == types.MP_IF or \
        lookAhead.getType == types.MP_WRITELN or \
        lookAhead.getType == types.MP_WRITE or \
        lookAhead.getType == types.MP_READ or \
        lookAhead.getType == types.MP_SCOLON or \
        lookAhead.getType == types.MP_END or \
        lookAhead.getType == types.MP_BEGIN:
            statement()
            statementTail()
    else:
        syntaxError("identifier, for, while, until, repeat, if, write, writeln, read, ;, end, begin")
"""
Rule 32 and 33:
StatementTail -> ";" Statement StatementTail
              -> Lambda
"""
def statementTail():
    if lookAhead.getType == types.MP_SCOLON:
        match(types.MP_SCOLON)
        statement()
        statementTail()
    elif lookAhead.getType == types.MP_UNTIL or \
            lookAhead.getType == types.MP_END:
        Lambda()
    else:
        syntaxError(";, until, end")
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
    if lookAhead.getType == types.MP_UNTIL or \
        lookAhead.getType == types.MP_END or \
        lookAhead.getType == types.MP_ELSE or \
        lookAhead.getType == types.MP_SCOLON:
            emptyStatement()
    elif lookAhead.getType == types.MP_BEGIN:
        compoundStatement()
    elif lookAhead.getType == types.MP_READ:
        readStatement()
    elif lookAhead.getType == types.MP_WRITELN or \
        lookAhead.getType == types.MP_WRITE:
            writeStatement()
    elif lookAhead.getType == types.MP_IDENTIFIER:
        if lookAhead2.getType == types.MP_ASSIGN:
            assignmentStatement()
        else:
            procedureStatement()
    elif lookAhead.getType == types.MP_IF:
        ifStatement()
    elif lookAhead.getType == types.MP_WHILE:
        whileStatement()
    elif lookAhead.getType == types.MP_REPEAT:
        repeatStatement()
    elif lookAhead.getType == types.MP_FOR:
        forStatement()
    else:
        syntaxError("until, else, ;, end, begin, Read, Write, Writeln, identifier, if, while, repeat, for")
"""
Rule 44:
EmptyStatement -> Lambda
"""
def emptyStatement():
    if lookAhead.getType == types.MP_UNTIL or \
        lookAhead.getType == types.MP_END or \
        lookAhead.getType == types.MP_ELSE or \
        lookAhead.getType == types.MP_SCOLON:
            Lambda()
    else:
        syntaxError("until, else, ;, end")
"""
Rule 45:
ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
"""
def readStatement():
    if lookAhead.getType == types.MP_READ:
        match(types.MP_READ)
        match(types.MP_LPAREN)
        readParameter()
        readParameterTail()
        match(types.MP_RPAREN)
    else:
        syntaxError("read")
"""
Rule 46 and 47:
ReadParameterTail -> "," ReadParameter ReadParameterTail
                  -> Lambda
"""
def readParameterTail():
    if lookAhead.getType == types.MP_COMMA:
        match(types.MP_COMMA)
        readParameter()
        readParameterTail()
    elif lookAhead.getType == types.MP_RPAREN:
        Lambda()
    else:
        syntaxError("',',  )")
"""
Rule 48:
ReadParameter -> VariableIdentifier
"""
def readParameter():
    if lookAhead.getType == types.MP_IDENTIFIER:
        variableIdentifier()
        # sem analyzer stuff
    else:
        syntaxError("identifier")
"""
Rule 49 and 50:
WriteStatement -> "write"  "(" WriteParameter WriteParameterTail ")"
               -> "writeln" "(" WriteParameter WriteParameterTail ")"
"""
def writeStatement():
    if lookAhead.getType == types.MP_WRITE:
        match(types.MP_WRITE)
        match(types.MP_LPAREN)
        writeParameter()
        writeParameterTail()
        match(types.MP_RPAREN)
    elif lookAhead.getType == types.MP_WRITELN:
        match(types.MP_WRITELN)
        match(types.MP_LPAREN)
        writeParameter()
        writeParameterTail()
        match(types.MP_RPAREN)
    else:
        syntaxError("write, writeln")
"""
Rule 51 and 52:
WriteParameterTail -> "," WriteParameter WriteParameterTail
                   -> Lambda
"""
def writeParameterTail(writeStatement):
    if lookAhead.getType == types.MP_COMMA:
        match(types.MP_COMMA)
        writeParameter(writeStatement)
        writeParameterTail(writeStatement)
    elif lookAhead.getType == types.MP_RPAREN:
        Lambda()
    else:
        syntaxError("',', )")
"""
Rule 53:
WriteParameter -> OrdinalExpression
"""
def writeParameter(writeStatement):
    if lookAhead.getType == types.MP_IDENTIFIER or \
        lookAhead.getType == types.MP_FALSE or \
        lookAhead.getType == types.MP_TRUE or \
        lookAhead.getType == types.MP_STRING_LIT or \
        lookAhead.getType == types.MP_FLOAT_LIT or \
        lookAhead.getType == types.MP_LPAREN or \
        lookAhead.getType == types.MP_NOT or \
        lookAhead.getType == types.MP_INTEGER_LIT or \
        lookAhead.getType == types.MP_MINUS or \
        lookAhead.getType == types.MP_PLUS:
            ordinalExpression()
            # sem analyzer stuff
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
"""
Rule 54 and 55:
AssignmentStatement -> VariableIdentifier ":=" Expression
                    -> FunctionIdentifier ":=" Expression
"""
def assignmentStatement():
    if lookAhead.getType == MP_IDENTIFIER:
        assign = symbolTable.findSymbol(lookAhead.getLexeme())
        if assign == null:
            semanticError("Undeclared variable: " + lookAhead.getLexeme() + " found.")
        else:
            if assign.classification == "VARIABLE" or \
                assign.classification == "PARAMETER":
                varID = variableIdentifier()
                # sem analyzer stuff
                match(types.MP_ASSIGN)
                exp = expression(null)
                # sem analyzer stuff
            elif assign.classification == "FUNCTION":
                funcID = functionIdentifier()
                # sem analyzer stuff
                match(types.MP_ASSIGN)
                exp = expression(null)
                # sem analyzer stuff
            else:
                semanticError("Cannot assign value to a Procedure")
    else:
        syntaxError("identifier")
"""
Rule 56:
IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
"""
def ifStatement():
    if lookAhead.getType == types.MP_IF:
        match(types.MP_IF)
        booleanExpression()
        match(types.MP_THEN)
        # sem analyzer stuff
        statement()
        # sem analyzer stuff
        optionalElsePart()
        # sem analyzer stuff
    else:
        syntaxError("if")
"""
Rule 57 and 58:
OptionalElsePart -> "else" Statement
                 -> Lambda
"""
def optionalElsePart():
    if lookAhead.getType == types.MP_ELSE:
        match(types.MP_ELSE)
        statement()
    elif lookAhead.getType == types.MP_UNTIL or \
        lookAhead.getType == types.MP_SCOLON or \
        lookAhead.getType == types.MP_END:
            Lambda()
    else:
        syntaxError("else, until, ;, end")
"""
Rule 59:
RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
"""
def repeatStatement():
    if lookAhead.getType == types.MP_REPEAT:
        match(types.MP_REPEAT)
        # sem analyzer stuff
        statementSequence()
        match(types.MP_UNTIL)
        booleanExpression()
        # sem analyzer stuff
    else:
        syntaxError("repeat")
"""
Rule 60:
WhileStatement -> "while" BooleanExpression "do" Statement
"""
def whileStatement():
    if lookAhead.getType == types.MP_WHILE:
        match(types.MP_WHILE)
        # sem analyzer stuff
        booleanExpression()
        # sem analyzer stuff
        match(types.MP_DO)
        statement()
        # sem analyzer stuff
    else:
        syntaxError("while")
"""
Rule 61:
ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
"""
def forStatement():
    if lookAhead.getType == types.MP_FOR:
        match(types.MP_FOR)
        controlIdentifier = controlVariable()
        # sem analyzer stuff
        match(types.MP_ASSIGN)
        exp = initialValue()
        # sem analyzer stuff
        forDirection = stepValue()
        finalExpr = finalValue()
        # sem analyzer stuff
        match(types.MP_DO)
        statement()
        # sem analyzer stuff
    else:
        syntaxError("for")
"""
Rule 62:
ControlVariable -> VariableIdentifier
"""
def controlVariable():
    if lookAhead.getType == types.MP_IDENTIFIER:
        varID = variableIdentifier()
    else:
        syntaxError("identifier")
    return varID
"""
Rule 63:
InitialValue -> OrdinalExpression
"""
def initialValue():
    if lookAhead.getType == types.MP_IDENTIFIER or \
        lookAhead.getType == types.MP_FALSE or \
        lookAhead.getType == types.MP_TRUE or \
        lookAhead.getType == types.MP_STRING_LIT or \
        lookAhead.getType == types.MP_FLOAT_LIT or \
        lookAhead.getType == types.MP_LPAREN or \
        lookAhead.getType == types.MP_NOT or \
        lookAhead.getType == types.MP_INTEGER_LIT or \
        lookAhead.getType == types.MP_MINUS or \
        lookAhead.getType == types.MP_PLUS:
            expr = ordinalExpression(null)
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return expr
"""
Rule 64 and 65:
StepValue -> "to"
          -> "downto"
"""
def stepValue():
    # sem analyzer record
    if lookAhead.getType == types.MP_TO:
        match(types.MP_TO)
        # create new sem analyzer record
    elif lookAhead.getType == types.MP_DOWNTO:
        match(types.MP_DOWNTO)
        # create new sem analyzer record
    else:
        syntaxError("to, downto")
    # return sem analyzer record
"""
Rule 66:
FinalValue -> OrdinalExpression
"""
def finalValue():
    if lookAhead.getType == MP_IDENTIFIER or \
        lookAhead.getType == MP_FALSE or \
        lookAhead.getType == MP_TRUE or \
        lookAhead.getType == MP_STRING_LIT or \
        lookAhead.getType == MP_FLOAT_LIT or \
        lookAhead.getType == MP_LPAREN or \
        lookAhead.getType == MP_NOT or \
        lookAhead.getType == MP_INTEGER_LIT or \
        lookAhead.getType == MP_MINUS or \
        lookAhead.getType == MP_PLUS:
            expr = ordinalExpression()
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return expr
"""
Rule 67:
ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
"""
def procedureStatement():
    if lookAhead.getType == types.MP_IDENTIFIER:
        procID = procedureIdentifier()
        # sem analyzer stuff for checking scope
        # if in scope, run optionalActualParameterList with formal Params
        optionalActualParameterList()
    else:
        syntaxError("identifier")
"""
Rule 68 and 69:
OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
                            -> Lambda
"""
def optionalActualParameterList(formalParams):
    if lookAhead.getType == types.MP_COMMA or \
        lookAhead.getType == types.MP_RPAREN or \
        lookAhead.getType == types.MP_AND or \
        lookAhead.getType == types.MP_MOD or \
        lookAhead.getType == types.MP_DIV or \
        lookAhead.getType == types.MP_DIV_INT or \
        lookAhead.getType == types.MP_TIMES or \
        lookAhead.getType == types.MP_OR or \
        lookAhead.getType == types.MP_MINUS or \
        lookAhead.getType == types.MP_PLUS or \
        lookAhead.getType == types.MP_NEQUAL or \
        lookAhead.getType == types.MP_GEQUAL or \
        lookAhead.getType == types.MP_LEQUAL or \
        lookAhead.getType == types.MP_GTHAN or \
        lookAhead.getType == types.MP_LTHAN or \
        lookAhead.getType == types.MP_EQUAL or \
        lookAhead.getType == types.MP_DOWNTO or \
        lookAhead.getType == types.MP_TO or \
        lookAhead.getType == types.MP_DO or \
        lookAhead.getType == types.MP_UNTIL or \
        lookAhead.getType == types.MP_ELSE or \
        lookAhead.getType == types.MP_THEN or \
        lookAhead.getType == types.MP_SCOLON or \
        lookAhead.getType == types.MP_END:
            Lambda()
            # sem error checks
    elif lookAhead.getType == types.MP_LPAREN:
        match(types.MP_LPAREN)
        actualParameter(formalParams)
        actualParameterTail(formalParams)
        # sem error check
        match(types.MP_RPAREN)
    else:
        syntaxError("',', ), and, mod, div, / , *, 'or', -, +, <>, >=, <=, <, >, =, downto, to, do, until, else, then, ;, end")
"""
Rule 70 and 71:
ActualParameterTail -> ","  ActualParameter ActualParameterTail
                    -> Lambda
"""
def actualParameterTail(formalParams):
    if lookAhead.getType == types.MP_COMMA:
        match(types.MP_COMMA)
        actualParameter(formalParams)
        actualParameterTail(formalParams)
    elif lookAhead.getType == types.RPAREN:
        Lambda()
    else:
        syntaxError("',', )")
"""
Rule 72:
ActualParameter -> OrdinalExpression
"""
def actualParameter(formalParams):
    if lookAhead.getType == MP_IDENTIFIER or \
        lookAhead.getType == MP_FALSE or \
        lookAhead.getType == MP_TRUE or \
        lookAhead.getType == MP_STRING_LIT or \
        lookAhead.getType == MP_FLOAT_LIT or \
        lookAhead.getType == MP_LPAREN or \
        lookAhead.getType == MP_NOT or \
        lookAhead.getType == MP_INTEGER_LIT or \
        lookAhead.getType == MP_MINUS or \
        lookAhead.getType == MP_PLUS:
            # sem formal param check
            expr = ordinalExpression()
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
"""
Rule 73:
Expression -> SimpleExpression OptionalRelationalPart
"""
def expression(formalParam):
    if lookAhead.getType == MP_IDENTIFIER or \
        lookAhead.getType == MP_FALSE or \
        lookAhead.getType == MP_TRUE or \
        lookAhead.getType == MP_STRING_LIT or \
        lookAhead.getType == MP_FLOAT_LIT or \
        lookAhead.getType == MP_LPAREN or \
        lookAhead.getType == MP_NOT or \
        lookAhead.getType == MP_INTEGER_LIT or \
        lookAhead.getType == MP_MINUS or \
        lookAhead.getType == MP_PLUS:
            simpExpr = simpleExpression(formalParam)
            opt = optionalRelationalPart(simpExpr)
            if opt:
                expr = opt
            else:
                expr = simpExpr
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return expr
"""
Rule 74 and 75:
OptionalRelationalPart -> RelationalOperator SimpleExpression
                       -> Lambda
"""
def optionalRelationalPart():
    if lookAhead.getType == MP_COMMA or \
        lookAhead.getType == MP_RPAREN or \
        lookAhead.getType == MP_DOWNTO or \
        lookAhead.getType == MP_TO or \
        lookAhead.getType == MP_DO or \
        lookAhead.getType == MP_UNTIL or \
        lookAhead.getType == MP_ELSE or \
        lookAhead.getType == MP_THEN or \
        lookAhead.getType == MP_SCOLON or \
        lookAhead.getType == MP_END:
            Lambda()
    elif lookAhead.getType == MP_NEQUAL or \
        lookAhead.getType == MP_GEQUAL or \
        lookAhead.getType == MP_LEQUAL or \
        lookAhead.getType == MP_GTHAN or \
        lookAhead.getType == MP_LTHAN or \
        lookAhead.getType == MP_EQUAL:
            op = relationalOperator()
            right = simpleExpression(null)
            # sem analyzer stuff, create record
    else:
        syntaxError("',', ), downto, to, do, until, else, then, ;, end, <>, >=, <=, >, <, =")
    # return sem record
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
    if lookAhead.getType == types.MP_EQUAL:
        match(types.MP_EQUAL)
        # new semantic record
    elif lookAhead.getType == types.MP_NEQUAL:
        match(types.MP_NEQUAL)
        # new semantic record
    elif lookAhead.getType == types.MP_GEQUAL:
        match(types.MP_GEQUAL)
        # new semantic record
    elif lookAhead.getType == types.MP_LEQUAL:
        match(types.MP_LEQUAL)
        # new semantic record
    elif lookAhead.getType == types.MP_GTHAN:
        match(types.MP_GTHAN)
        # new semantic record
    elif lookAhead.getType == types.MP_LTHAN:
        match(types.MP_LTHAN)
        # new semantic record
    else:
        syntaxError("<>, >=, <= , >, <, =")
    # return semantic record
"""
Rule 82:
SimpleExpression -> OptionalSign Term TermTail
"""
def simpleExpression(formalParam):
    if lookAhead.getType == MP_IDENTIFIER or \
        lookAhead.getType == MP_FALSE or \
        lookAhead.getType == MP_TRUE or \
        lookAhead.getType == MP_STRING_LIT or \
        lookAhead.getType == MP_FLOAT_LIT or \
        lookAhead.getType == MP_LPAREN or \
        lookAhead.getType == MP_NOT or \
        lookAhead.getType == MP_INTEGER_LIT or \
        lookAhead.getType == MP_MINUS or \
        lookAhead.getType == MP_PLUS:
            opt = optionalSign()
            term = term(formalParam)
            # sem analyzer stuff
            termTail = termTail(term)
            if !termTail:
                termTail = term
            simpExpr = termTail
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return simpExpr
"""
Rule 83 and 84:
TermTail -> AddingOperator Term TermTail
         -> Lambda
"""
def termTail(left):
    if lookAhead.getType == MP_COMMA or \
        lookAhead.getType == MP_RPAREN or \
        lookAhead.getType == MP_NEQUAL or \
        lookAhead.getType == MP_GEQUAL or \
        lookAhead.getType == MP_LEQUAL or \
        lookAhead.getType == MP_GTHAN or \
        lookAhead.getType == MP_LTHAN or \
        lookAhead.getType == MP_EQUAL or \
        lookAhead.getType == MP_DOWNTO or \
        lookAhead.getType == MP_TO or \
        lookAhead.getType == MP_DO or \
        lookAhead.getType == MP_UNTIL or \
        lookAhead.getType == MP_ELSE or \
        lookAhead.getType == MP_THEN or \
        lookAhead.getType == MP_SCOLON or \
        lookAhead.getType == MP_END:
            Lambda()
    elif lookAhead.getType == MP_OR or \
        lookAhead.getType == MP_MINUS or \
        lookAhead.getType == MP_PLUS:
            addOp = addingOperator()
            term = term(null)
            # sem analyzer stuff
            termTail = termTail(term)
            if !termTail:
                termTail = term
    else:
        syntaxError("',', ), <>, >=, <=, >, <, =, downto, to, do, until, else, then, ;, end, or, -, +")
    return termTail
"""
Rule 85, 86 and 87:
OptionalSign -> "+"
             -> "-"
             -> Lambda
"""
def optionalSign():################### Return Here ############################
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
           -> Lambda
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
    if lookAhead.getType == types.MP_IDENTIFIER:
        progIdentString = lookAhead.getLexeme()
        match(types.MP_IDENTIFIER)
        return progIdentString
    else:
        syntaxError("progIdent")
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
    idList = []
    if lookAhead.getType == types.MP_IDENTIFIER:
        idList.append(lookAhead.getLexeme())
        match(types.MP_IDENTIFIER)
        identifierTail(idList)
        return idList
    else:
        syntaxError("identList")

"""
Rule 114 and 115:
IdentifierTail -> "," Identifier IdentifierTail
               -> Lambda
"""
def identifierTail(inList):
    if lookAhead.getType == types.MP_COMMA:
        match(types.MP_COMMA)
        inList.append(lookAhead.getLexeme())
        match(types.MP_IDENTIFIER)
        identifierTail(inList)
    elif lookAhead.getType == types.MP_COLON:
        Lambda()
    else:
        syntaxError("identTail")