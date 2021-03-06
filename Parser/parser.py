#parser.py
import sys
from leaf import Leaf
from recordTypes import recTypes
from classifications import classification
from modes import mode
from types import varTypes
sys.path.insert(0, '/Symbol/')
from Symbol.symbolTable import SymbolTable
from Analyzer.analyzer import Analyzer
sys.path.insert(0, '../../')
from tokens import *
from label import Label
import scanner as scanner

# Use 2 look aheads for parsing
lookAhead = None
lookAhead2 = None


labelCounter = 0
symbolTables = []

def dq(s): return '"%s"' %s
# --------------------------------------------------------------
# Parser Functions
# --------------------------------------------------------------
def getToken():
    global lookAhead, lookAhead2
    lookAhead = lookAhead2
    lookAhead2 = scanner.getToken()

def matchError(expToken):
    print "Match error found on line: " + str(lookAhead.getLineNumber()) + ", column: " + str(lookAhead.getColNumber()) + "... Expected '" + str(expToken) + "', instead found '" + str(lookAhead.getLexeme()) + "'"

def syntaxError(expToken):
    sys.exit("Syntax error found on line: " + str(lookAhead.getLineNumber()) + ", column: " + str(lookAhead.getColNumber()) + " ... Expected '" + str(expToken) + "', instead found '" + str(lookAhead.getLexeme()) + "'")

def semanticError(msg):
    sys.exit("Semantic Error: " + str(msg))

def match(tempTokenType):
    if lookAhead.Type == tempTokenType:
        getToken()
    else:
        matchError(str(tempTokenType))

def Lambda():
    ## Dummy function to extend lambda rules
    pass

def parse(sourceText):
    global scanner, labelCounter, lookAhead, lookAhead2, symbolTables, analyzer, label
    scanner.initialize(sourceText)
    labelCounter = 1
    lookAhead = scanner.getToken()
    lookAhead2 = scanner.getToken()
    symbolTables = []
    analyzer = Analyzer(symbolTables)
    label = Label()
    systemGoal()
# --------------------------------------------------------------
# Symbol Table Stack Stuff
# --------------------------------------------------------------
def addSymbolTable(scopeName, branchLabel):
    exists = False
    for t in symbolTables:
        if t.getScopeName() == scopeName:
            exists = True
            break
    
    if not exists:
        symbolTables.append(SymbolTable(scopeName, branchLabel))
        analyzer.updateTables(symbolTables)
        return True
    else:
        semanticError("Symbol table with name: " + scopeName + " already exists")
        return False
    
def removeSymbolTable(rule):
    symbolTables[-1].decrementNestingLevel()
    symbolTables.pop()
    analyzer.updateTables(symbolTables)
    
def printSymbolTables():
    for t in symbolTables:
        t.printTable()
#-----------------------------------
# CFG Definitions
#-----------------------------------

"""
Rule 1:
SystemGoal -> Program EOF
"""
def systemGoal():
    if lookAhead.getType() == types.MP_PROGRAM:
        #print "Extending Rule 1: SystemGoal -> Program EOF"
        program()
        match(types.MP_EOF)
    else:
        syntaxError("program")
"""
Rule 2:
Program -> ProgramHeading ";" Block "."
"""
def program():
    if lookAhead.getType() == types.MP_PROGRAM:
        #print "Extending Rule 2: Program -> ProgramHeading ';' Block '.'"
        scopeName = programHeading()
        branch = label.getNextLabel()
        record = {'type':recTypes.LABEL, 'label':branch}
        addSymbolTable(scopeName, branch)
        symbolTables[-1].addDataSymbolsToTable(classification.DISREG, ["Old Display Register Value"], [{'type':varTypes.STRING, 'mode':mode.VALUE}])
        match(types.MP_SCOLON)
        analyzer.genBR(record)
        block(scopeName, {'type':recTypes.BLOCK, 'label':'program'}, record)
        match(types.MP_PERIOD)
        nameRecord = {'type':recTypes.SYMBOL_TABLE, 'scope':str(symbolTables[-1].getScopeName()), 'nestinglvl':str(symbolTables[-1].getNestingLevel()), 'tblsize':str(symbolTables[-1].getTableSize())}
        analyzer.genProgDR(nameRecord)
        printSymbolTables()
        removeSymbolTable("program")
        analyzer.genHLT()
    else:
        syntaxError("program")
"""
Rule 3:
ProgramHeading -> "program" ProgramIdentifier
"""
def programHeading():
    if lookAhead.getType() == types.MP_PROGRAM:
        #print "Extending Rule 3: ProgramHeading -> 'program' ProgramIdentifier"
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
    if lookAhead.getType() == types.MP_BEGIN or \
        lookAhead.getType() == types.MP_FUNCTION or \
        lookAhead.getType() == types.MP_PROCEDURE or \
        lookAhead.getType() == types.MP_VAR:
            #print "Extending Rule 4: Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart"
            variableDeclarationPart()
            nameRecord = {'type':recTypes.SYMBOL_TABLE, 'scope':str(scope), 'nestinglvl':str(symbolTables[-1].getNestingLevel()), 'tblsize':str(symbolTables[-1].getTableSize())}
            procedureAndFunctionDeclarationPart()
            analyzer.genSpecLabel(label)
            analyzer.genActRec(nameRecord, blockType)
            statementPart()
    else:
        syntaxError("var, begin, function, procedure")
"""
Rule 5 and 6:
VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
                        -> Lambda
"""
def variableDeclarationPart():
    if lookAhead.getType() == types.MP_VAR:
        #print "Extending Rule 5: VariableDeclarationPart -> 'var' VariableDeclaration ';' VariableDeclarationTail"
        match(types.MP_VAR)
        variableDeclaration()
        match(types.MP_SCOLON)
        variableDeclarationTail()
    elif lookAhead.getType() == types.MP_BEGIN or \
        lookAhead.getType() == types.MP_FUNCTION or \
        lookAhead.getType() == types.MP_PROCEDURE:
            #print "Extending Rule 6: Lambda"
            Lambda()
    else:
        syntaxError("var, begin, function, procedure")
"""
Rule 7 and 8:
VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail
                        -> Lambda
"""
def variableDeclarationTail():
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 7: VariableDeclarationTail -> VariableDeclaration ';' VariableDeclarationTail"
        variableDeclaration()
        match(types.MP_SCOLON)
        variableDeclarationTail()
    elif lookAhead.getType() == types.MP_BEGIN or \
        lookAhead.getType() == types.MP_FUNCTION or \
        lookAhead.getType() == types.MP_PROCEDURE:
            #print "Extending Rule 8: VariableDeclarationTail -> Lambda"
            Lambda()
    else:
        syntaxError("identifier, begin, procedure, function")
"""
Rule 9:
VariableDeclaration -> IdentifierList ":" Type
"""
def variableDeclaration():
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 9: VariableDeclaration -> IdentifierList ':' Type"
        idList = identifierList()
        match(types.MP_COLON)
        t = Type()
        symbolTables[-1].addDataSymbolsToTable(classification.VARIABLE, idList, [{'type':t, 'mode':mode.VARIABLE}])
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
    if lookAhead.getType() == types.MP_INTEGER:
        #print "Extending Rule 10: Type -> 'Integer'"
        match(types.MP_INTEGER)
        curType = varTypes.INTEGER
    elif lookAhead.getType() == types.MP_FLOAT:
        #print "Extending Rule 11: Type -> 'Float'"
        match(types.MP_FLOAT)
        curType = varTypes.FLOAT
    elif lookAhead.getType() == types.MP_STRING:
        #print "Extending Rule 12: Type -> 'String'"
        match(types.MP_STRING)
        curType = varTypes.STRING
    elif lookAhead.getType() == types.MP_BOOLEAN:
        #print "Extending Rule 13: Type -> 'Boolean'"
        match(types.MP_BOOLEAN)
        curType = varTypes.BOOLEAN
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
    if lookAhead.getType() == types.MP_PROCEDURE:
        #print "Extending Rule 14: ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart"
        procedureDeclaration()
        procedureAndFunctionDeclarationPart()
    elif lookAhead.getType() == types.MP_FUNCTION:
        #print "Extending Rule 15: ProcedureAndFunctionDeclarationPart -> FunctionDeclaration ProcedureAndFunctionDeclarationPart"
        functionDeclaration()
        procedureAndFunctionDeclarationPart()
    elif lookAhead.getType() == types.MP_BEGIN:
        #print "Extending Rule 16: ProcedureAndFunctionDeclarationPart -> Lambda"
        Lambda()
    else:
        syntaxError("procedure, function")
"""
Rule 17:
ProcedureDeclaration -> ProcedureHeading ";" Block ";"
"""
def procedureDeclaration():
    lbl = label.getNextLabel()
    branchLbl = {'type':recTypes.LABEL, 'label':lbl}
    if lookAhead.getType() == types.MP_PROCEDURE:
        #print "Extending Rule 17: ProcedureDeclaration -> ProcedureHeading ';' Block ';'"
        procedureID = procedureHeading(branchLbl)
        match(types.MP_SCOLON)
        block(procedureID, {'type':recTypes.BLOCK, 'label':"procedure"}, branchLbl)
        match(types.MP_SCOLON)
        nameRecord = {'type':recTypes.SYMBOL_TABLE, 'scope':str(symbolTables[-1].getScopeName()), 'nestinglvl':str(symbolTables[-1].getNestingLevel()), 'tblsize':str(symbolTables[-1].getTableSize())}
        analyzer.genProcDR(nameRecord)
        print "Popping Procedure Table..."
        printSymbolTables()
        removeSymbolTable("procedure")
    else:
        syntaxError("procedure")
"""
Rule 18:
FunctionDeclaration -> FunctionHeading ";" Block ";"
"""
def functionDeclaration():
    lbl = label.getNextLabel()
    branchLbl = {'type':recTypes.LABEL, 'label':lbl}
    if lookAhead.getType() == types.MP_FUNCTION:
        #print "Extending Rule 18: FunctionDeclaration -> FunctionHeading ';' Block ';'"
        functionID = functionHeading(branchLbl)
        match(types.MP_SCOLON)
        block(functionID, {'type':recTypes.BLOCK, 'label':"function"}, branchLbl)
        match(types.MP_SCOLON)
        nameRecord = {'type':recTypes.SYMBOL_TABLE, 'scope':str(symbolTables[-1].getScopeName()), 'nestinglvl':str(symbolTables[-1].getNestingLevel()), 'tblsize':str(symbolTables[-1].getTableSize())}
        analyzer.genFuncDR(nameRecord)
        print "Popping Function Table..."
        printSymbolTables()
        removeSymbolTable("function")
        row = analyzer.findSymbol(functionID, classification.FUNCTION)
        if row['returnValue'] is False:
            semanticError("Function: " + str(functionID) + " is missing return value")
    else:
        syntaxError("function")
"""
Rule 19:
ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
"""
def procedureHeading(branchLbl):
    procID = None
    attributes = []
    ids = []
    if lookAhead.getType() == types.MP_PROCEDURE:
        #print "Extending Rule 19: ProcedureHeading -> 'procedure' procedureIdentifier OptionalFormalParameterList"
        match(types.MP_PROCEDURE)
        procID = procedureIdentifier()
        parameters = optionalFormalParameterList()
        for p in parameters:
            attributes.append(p['attribute'])
            ids.append(p['lexeme'])
        symbolTables[-1].addModuleSymbolsToTable(classification.PROCEDURE, procID, None, attributes, branchLbl)
        addSymbolTable(procID, branchLbl['label'])
        symbolTables[-1].addDataSymbolsToTable(classification.DISREG, ["Old Display Register Value"], [{'type':varTypes.STRING, 'mode':mode.VALUE}])
        symbolTables[-1].addDataSymbolsToTable(classification.PARAMETER, ids, attributes)
        symbolTables[-1].addDataSymbolsToTable(classification.RETADDR, ["Caller's Return Address"], [{'type':varTypes.STRING, 'mode':mode.VALUE}])
    else:
        syntaxError("procedure")
    return procID
"""
Rule 20:
FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
"""
def functionHeading(branchLbl):
    funcID = None
    attributes = []
    ids = []
    if lookAhead.getType() == types.MP_FUNCTION:
        #print "Extending Rule 20: FunctionHeading -> 'function' functionIdentifier OptionalFormalParameterList ':'Type"
        match(types.MP_FUNCTION)
        funcID = functionIdentifier()
        parameters = optionalFormalParameterList()
        for p in parameters:
            attributes.append(p['attribute'])
            ids.append(p['lexeme'])
        match(types.MP_COLON)
        t = Type()
        symbolTables[-1].addModuleSymbolsToTable(classification.FUNCTION, funcID, t, attributes, branchLbl)
        addSymbolTable(funcID, branchLbl['label'])
        symbolTables[-1].addDataSymbolsToTable(classification.DISREG, ["Old Display Register Value"], [{'type':varTypes.STRING, 'mode':mode.VALUE}])
        symbolTables[-1].addDataSymbolsToTable(classification.PARAMETER, ids, attributes)
        symbolTables[-1].addDataSymbolsToTable(classification.RETADDR, ["Caller's Return Address"], [{'type':varTypes.STRING, 'mode':mode.VALUE}])
    else:
        syntaxError("function")
    return funcID
"""
Rule 21 and 22:
OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                            -> Lambda
"""
def optionalFormalParameterList():
    parameters = {}
    if lookAhead.getType() == types.MP_LPAREN:
        #print "Extending Rule 21: OptionalFormalParameterList -> '(' FormalParameterSection FormalParameterSectionTail ')'"
        match(types.MP_LPAREN)
        parameters = formalParameterSection()
        formalParameterSectionTail(parameters)
        match(types.MP_RPAREN)
    elif lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_COLON:
        #print "Extending Rule 22: OptionalFormalParameterList -> Lambda"
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
    if lookAhead.getType() == types.MP_SCOLON:
        #print "Extending Rule 23: FormalParameterSectionTail -> ';' FormalParameterSection FormalParameterSectionTail"
        match(types.MP_SCOLON)
        parameters.extend(formalParameterSection())
        formalParameterSectionTail(parameters)
    elif lookAhead.getType() == types.MP_RPAREN:
        #print "Extending Rule 24: FormalParameterSectionTail -> Lambda"
        Lambda()
    else:
        syntaxError("function, )")
"""
Rule 25 and 26:
FormalParameterSection -> ValueParameterSection
                       -> VariableParameterSection
"""
def formalParameterSection():
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 25: FormalParameterSection -> ValueParameterSection"
        parameters = valueParameterSection()
    elif lookAhead.getType() == types.MP_VAR:
        #print "Extending Rule 26: FormalParameterSection -> VariableParameterSection"
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
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 27: ValueParameterSection -> IdentifierList ':' Type"
        ids = identifierList()
        match(types.MP_COLON)
        thisType = Type()
        for lex in ids:
            parameters.append({'lexeme':lex, 'attribute':{'type':thisType, 'mode':mode.VALUE}})
    else:
        syntaxError("identifier")
    return parameters
"""
Rule 28:
VariableParameterSection -> "var" IdentifierList ":" Type
"""
def variableParameterSection():
    parameters = []
    if lookAhead.getType() == types.MP_VAR:
        #print "Extending Rule 28: VariableParameterSection -> 'var' IdentifierList ':' Type"
        match(types.MP_VAR)
        ids = identifierList()
        match(types.MP_COLON)
        thisType = Type()
        for lex in ids:
            parameters.append({'lexeme':lex, 'attribute':{'type':thisType, 'mode':mode.VARIABLE}})
    else:
        syntaxError("var")
    return parameters
"""
Rule 29:
StatementPart -> CompoundStatement
"""
def statementPart():
    if lookAhead.getType() == types.MP_BEGIN:
        #print "Extending Rule 29: StatementPart -> CompoundStatement"
        compoundStatement()
    else:
        syntaxError("begin")
"""
Rule 30:
CompoundStatement -> "begin" StatementSequence "end"
"""
def compoundStatement():
    if lookAhead.getType() == types.MP_BEGIN:
        #print "Extending Rule 30: CompoundStatement -> 'begin' StatementSequence 'end'"
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
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FOR or \
        lookAhead.getType() == types.MP_WHILE or \
        lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_REPEAT or \
        lookAhead.getType() == types.MP_IF or \
        lookAhead.getType() == types.MP_WRITELN or \
        lookAhead.getType() == types.MP_WRITE or \
        lookAhead.getType() == types.MP_READ or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END or \
        lookAhead.getType() == types.MP_BEGIN:
            #print "Extending Rule 31: StatementSequence -> Statement StatementTail"
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
    if lookAhead.getType() == types.MP_SCOLON:
        #print "Extending Rule 32: StatementTail -> ';' Statement StatementTail"
        match(types.MP_SCOLON)
        statement()
        statementTail()
    elif lookAhead.getType() == types.MP_UNTIL or \
            lookAhead.getType() == types.MP_END:
            #print "Extending Rule 33: StatementTail -> Lambda"
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
    if lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_END or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_SCOLON:
            #print "Extending Rule 34: Statement -> EmptyStatement"
            emptyStatement()
    elif lookAhead.getType() == types.MP_BEGIN:
        #print "Extending Rule 35: Statement -> CompoundStatement"
        compoundStatement()
    elif lookAhead.getType() == types.MP_READ:
        #print "Extending Rule 36: Statement -> ReadStatement"
        readStatement()
    elif lookAhead.getType() == types.MP_WRITELN or \
        lookAhead.getType() == types.MP_WRITE:
            #print "Extending Rule 37: Statement -> WriteStatement"
            writeStatement()
    elif lookAhead.getType() == types.MP_IDENTIFIER:
        if lookAhead2.getType() == types.MP_ASSIGN:
            #print "Extending Rule 38: Statement -> AssignmentStatement"
            assignmentStatement()
        else:
            #print "Extending Rule 43: Statement -> ProcedureStatement"
            procedureStatement()
    elif lookAhead.getType() == types.MP_IF:
        #print "Extending Rule 39: Statement -> IfStatement"
        ifStatement()
    elif lookAhead.getType() == types.MP_WHILE:
        #print "Extending Rule 40: Statement -> WhileStatement"
        whileStatement()
    elif lookAhead.getType() == types.MP_REPEAT:
        #print "Extending Rule 41: Statement -> RepeatStatement"
        repeatStatement()
    elif lookAhead.getType() == types.MP_FOR:
        #print "Extending Rule 42: Statement -> ForStatement"
        forStatement()
    else:
        syntaxError("until, else, ;, end, begin, Read, Write, Writeln, identifier, if, while, repeat, for")
"""
Rule 44:
EmptyStatement -> Lambda
"""
def emptyStatement():
    if lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_END or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_SCOLON:
            #print "Extending Rule 44: EmptyStatement -> Lambda"
            Lambda()
    else:
        syntaxError("until, else, ;, end")
"""
Rule 45:
ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
"""
def readStatement():
    if lookAhead.getType() == types.MP_READ:
        #print "Extending Rule 45: ReadStatement -> 'read' '(' ReadParameter ReadParameterTail ')'"
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
    if lookAhead.getType() == types.MP_COMMA:
        #print "Extending Rule 46: ReadParameterTail -> ',' ReadParameter ReadParameterTail"
        match(types.MP_COMMA)
        readParameter()
        readParameterTail()
    elif lookAhead.getType() == types.MP_RPAREN:
        #print "Extending Rule 47: ReadParameterTail -> Lambda"
        Lambda()
    else:
        syntaxError("',',  )")
"""
Rule 48:
ReadParameter -> VariableIdentifier
"""
def readParameter():
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 48: ReadParameter -> VariableIdentifier"
        iden = variableIdentifier()
        symbolvar = analyzer.findSymbol(iden, None)
        readRecord = {'type':recTypes.IDENTIFIER, 'classification':symbolvar['classification'], 'controlId':iden}
        if symbolvar['classification'] == classification.VARIABLE:
            analyzer.genRead(readRecord, True)
        else:
            if symbolvar['mode'] == mode.VARIABLE:
                analyzer.genRead(readRecord, False)
            else:
                analyzer.genRead(readRecord, True)
    else:
        syntaxError("identifier")
"""
Rule 49 and 50:
WriteStatement -> "write"  "(" WriteParameter WriteParameterTail ")"
               -> "writeln" "(" WriteParameter WriteParameterTail ")"
"""
def writeStatement():
    if lookAhead.getType() == types.MP_WRITE:
        #print "Extending Rule 49: WriteStatement -> 'write'  '(' WriteParameter WriteParameterTail ')'"
        match(types.MP_WRITE)
        match(types.MP_LPAREN)
        writeRecord = {'type':recTypes.WRITE_STATEMENT, 'tokenType':types.MP_WRITE}
        writeParameter(writeRecord)
        writeParameterTail(writeRecord)
        match(types.MP_RPAREN)
    elif lookAhead.getType() == types.MP_WRITELN:
        #print "Extending Rule 50: WriteStatement -> 'writeln'  '(' WriteParameter WriteParameterTail ')'"
        match(types.MP_WRITELN)
        match(types.MP_LPAREN)
        writeRecord = {'type':recTypes.WRITE_STATEMENT, 'tokenType':types.MP_WRITELN}
        writeParameter(writeRecord)
        writeParameterTail(writeRecord)
        match(types.MP_RPAREN)
    else:
        syntaxError("write, writeln")
"""
Rule 51 and 52:
WriteParameterTail -> "," WriteParameter WriteParameterTail
                   -> Lambda
"""
def writeParameterTail(writeRec):
    if lookAhead.getType() == types.MP_COMMA:
        #print "Extending Rule 51: WriteParameterTail -> ',' WriteParameter WriteParameterTail"
        match(types.MP_COMMA)
        writeParameter(writeRec)
        writeParameterTail(writeRec)
    elif lookAhead.getType() == types.MP_RPAREN:
        #print "Extending Rule 52: WriteParameterTail -> Lambda"
        Lambda()
    else:
        syntaxError("',', )")
"""
Rule 53:
WriteParameter -> OrdinalExpression
"""
def writeParameter(writeRec):
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 53: WriteParameter -> OrdinalExpression"
            expRec = ordinalExpression(None)
            analyzer.genWrite(writeRec, expRec)
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
"""
Rule 54 and 55:
AssignmentStatement -> VariableIdentifier ":=" Expression
                    -> FunctionIdentifier ":=" Expression
"""
def assignmentStatement():
    symTableRec = {'type':recTypes.SYMBOL_TABLE, 'scope':str(symbolTables[-1].getScopeName()), 'nestinglvl':str(symbolTables[-1].getNestingLevel()), 'tblsize':str(symbolTables[-1].getTableSize())}
    if lookAhead.getType() == types.MP_IDENTIFIER:
        assign = analyzer.findSymbol(lookAhead.getLexeme(), None)
        if assign == None:
            semanticError("Undeclared variable: " + lookAhead.getLexeme() + " found.")
        else:
            if assign['classification'] == classification.VARIABLE or assign['classification'] == classification.PARAMETER:
                #print "Extending Rule 54: AssignmentStatement -> VariableIdentifier ':=' Expression"
                varId = variableIdentifier()
                varRec = {'type':recTypes.IDENTIFIER, 'classification':assign['classification'], 'lexeme':varId}
                match(types.MP_ASSIGN)
                exp = expression(None)
                analyzer.genAssign(varRec, exp, symTableRec)
            elif assign['classification'] == classification.FUNCTION:
                #print "Extending Rule 55: AssignmentStatement -> FunctionIdentifier ':=' Expression"
                funcID = functionIdentifier()
                funcRec = {'type':recTypes.IDENTIFIER, 'classification':assign['classification'], 'lexeme':funcID}
                match(types.MP_ASSIGN)
                exp = expression(None)
                analyzer.genAssign(funcRec, exp, symTableRec)
            else:
                semanticError("Cannot assign value to a Procedure")
    else:
        syntaxError("identifier")
"""
Rule 56:
IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
"""
def ifStatement():
    if lookAhead.getType() == types.MP_IF:
        #print "Extending Rule 56: IfStatement -> 'if' BooleanExpression 'then' Statement OptionalElsePart"
        match(types.MP_IF)
        booleanExpression()
        match(types.MP_THEN)
        analyzer.genComment('if')
        elseLabel = analyzer.genBranchFalse() # BRFS to else lbl
        statement()
        analyzer.genComment('skip else part')
        endLabel = analyzer.genBranchUncond() # BR to end of if statement
        analyzer.genComment('else part')
        analyzer.genSpecLabel(elseLabel)
        optionalElsePart()
        analyzer.genComment('if end label')
        analyzer.genSpecLabel(endLabel)
    else:
        syntaxError("if")
"""
Rule 57 and 58:
OptionalElsePart -> "else" Statement
                 -> Lambda
"""
def optionalElsePart():
    if lookAhead.getType() == types.MP_ELSE:
        #print "Extending Ruel 57: OptionalElsePart -> 'else' Statement"
        match(types.MP_ELSE)
        statement()
    elif lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END:
            #print "Extending Ruel 58: OptionalElsePart -> Lambda"
            Lambda()
    else:
        syntaxError("else, until, ;, end")
"""
Rule 59:
RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
"""
def repeatStatement():
    if lookAhead.getType() == types.MP_REPEAT:
        #print "Extending Rule 59: RepeatStatement -> 'repeat' StatementSequence 'until' BooleanExpression"
        match(types.MP_REPEAT)
        analyzer.genComment('begin repeat')
        repeatLabel = analyzer.genLabel()
        statementSequence()
        match(types.MP_UNTIL)
        booleanExpression()
        analyzer.genComment('evaluate bool expr and jump to beginning of repeat (if necessary)')
        analyzer.genBranchFalseTo(repeatLabel)
    else:
        syntaxError("repeat")
"""
Rule 60:
WhileStatement -> "while" BooleanExpression "do" Statement
"""
def whileStatement():
    if lookAhead.getType() == types.MP_WHILE:
        #print "Extending Rule 60: WhileStatement -> 'while' BooleanExpression 'do' Statement"
        match(types.MP_WHILE)
        analyzer.genComment('while')
        whileLabel = analyzer.genLabel()
        booleanExpression()
        endLabel = analyzer.genBranchFalse()
        match(types.MP_DO)
        statement()
        analyzer.genBranchUncondTo(whileLabel)
        analyzer.genSpecLabel(endLabel)
    else:
        syntaxError("while")
"""
Rule 61:
ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
"""
def forStatement():
    if lookAhead.getType() == types.MP_FOR:
        #print "Extending Rule 61: ForStatement -> 'for' ControlVariable ':=' InitialValue StepValue FinalValue 'do' Statement"
        match(types.MP_FOR)
        controlIdentifier = controlVariable()
        controlSymbol = analyzer.findSymbol(controlIdentifier, None)
        controlRec = {'type':recTypes.IDENTIFIER, 'classification':controlSymbol['classification'], 'controlId':controlIdentifier}
        match(types.MP_ASSIGN)
        exp = initialValue()
        analyzer.genComment("assign controlVar to init val")
        analyzer.genAssignFor(controlRec,exp)
        forLabel = analyzer.genLabel() # drop for label
        analyzer.genPushVar(controlRec)
        forDirection = stepValue()
        finalExpr = finalValue()
        analyzer.genAssignCast(controlRec, finalExpr)
        analyzer.genComment("comparing controlVar to finalVal")
        analyzer.genForComp(forDirection)
        endForLabel = analyzer.genBranchFalse() # drop end label
        match(types.MP_DO)
        statement()
        analyzer.genComment("inc/dec controlVar")
        analyzer.genForController(controlRec, forDirection)
        analyzer.genBranchUncondTo(forLabel)
        analyzer.genSpecLabel(endForLabel)
    else:
        syntaxError("for")
"""
Rule 62:
ControlVariable -> VariableIdentifier
"""
def controlVariable():
    varID = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 62: ControlVariable -> VariableIdentifier"
        varID = variableIdentifier()
    else:
        syntaxError("identifier")
    return varID
"""
Rule 63:
InitialValue -> OrdinalExpression
"""
def initialValue():
    expr = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 63: InitialValue -> OrdinalExpression"
            expr = ordinalExpression(None)
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return expr
"""
Rule 64 and 65:
StepValue -> "to"
          -> "downto"
"""
def stepValue():
    forDirection = None
    if lookAhead.getType() == types.MP_TO:
        #print "Extending Rule 64: StepValue -> 'to'"
        match(types.MP_TO)
        forDirection = {'type':recTypes.FOR_DIRECTION, 'tokenType':types.MP_TO}
    elif lookAhead.getType() == types.MP_DOWNTO:
        #print "Extending Rule 65: StepValue -> 'downto'"
        match(types.MP_DOWNTO)
        forDirection = {'type':recTypes.FOR_DIRECTION, 'tokenType':types.MP_DOWNTO}
    else:
        syntaxError("to, downto")
    return forDirection
"""
Rule 66:
FinalValue -> OrdinalExpression
"""
def finalValue():
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 66: FinalValue -> OrdinalExpression"
            expr = ordinalExpression(None)
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return expr
"""
Rule 67:
ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
"""
def procedureStatement():
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 67: ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList"
        procID = procedureIdentifier()
        row = analyzer.findSymbol(procID, classification.PROCEDURE)
        if row is not None:
            formalParams = {'name':procID, 'attributes':row['attributes'], 'pointer':0}
            procRec = {'type':recTypes.IDENTIFIER, 'classification':classification.PROCEDURE, 'controlId':procID}
            analyzer.genComment("call to " + procID + " start")
            analyzer.genSPslot()
            optionalActualParameterList(formalParams)
            analyzer.genProcCall(procRec)
            analyzer.genComment("call to " + procID + " end")
        else:
            semanticError(str(procID) + " is not in scope")
    else:
        syntaxError("identifier")
"""
Rule 68 and 69:
OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
                            -> Lambda
"""
def optionalActualParameterList(formalParams):
    if lookAhead.getType() == types.MP_COMMA or \
        lookAhead.getType() == types.MP_RPAREN or \
        lookAhead.getType() == types.MP_AND or \
        lookAhead.getType() == types.MP_MOD or \
        lookAhead.getType() == types.MP_FLOAT_DIVIDE or \
        lookAhead.getType() == types.MP_DIV or \
        lookAhead.getType() == types.MP_TIMES or \
        lookAhead.getType() == types.MP_OR or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS or \
        lookAhead.getType() == types.MP_NEQUAL or \
        lookAhead.getType() == types.MP_GEQUAL or \
        lookAhead.getType() == types.MP_LEQUAL or \
        lookAhead.getType() == types.MP_GTHAN or \
        lookAhead.getType() == types.MP_LTHAN or \
        lookAhead.getType() == types.MP_EQUAL or \
        lookAhead.getType() == types.MP_DOWNTO or \
        lookAhead.getType() == types.MP_TO or \
        lookAhead.getType() == types.MP_DO or \
        lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_THEN or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END:
            #print "Extending Rule 69: OptionalActualParameterList -> Lambda"
            Lambda()
            if formalParams['pointer'] != len(formalParams['attributes']):
                semanticError("Invalid call, actual parameter list size of " + formalParams['name'] + " doesn't equal formal param count")
    elif lookAhead.getType() == types.MP_LPAREN:
        #print "Extending Rule 68: OptionalActualParameterList -> '(' ActualParameter ActualParameterTail ')'"
        match(types.MP_LPAREN)
        actualParameter(formalParams)
        actualParameterTail(formalParams)
        if formalParams['pointer'] != len(formalParams['attributes']):
            semanticError("Invalid call, actual parameter list size of " + formalParams['name'] + " doesn't equal formal param count")
        match(types.MP_RPAREN)
    else:
        syntaxError("',', ), and, mod, div, / , *, 'or', -, +, <>, >=, <=, <, >, =, downto, to, do, until, else, then, ;, end")
"""
Rule 70 and 71:
ActualParameterTail -> ","  ActualParameter ActualParameterTail
                    -> Lambda
"""
def actualParameterTail(formalParams):
    if lookAhead.getType() == types.MP_COMMA:
        #print "Extending Rule 70: ActualParameterTail -> ','  ActualParameter ActualParameterTail"
        match(types.MP_COMMA)
        actualParameter(formalParams)
        actualParameterTail(formalParams)
    elif lookAhead.getType() == types.MP_RPAREN:
        #print "Extending Rule 71: ActualParameterTail -> Lambda"
        Lambda()
    else:
        syntaxError("',', )")
"""
Rule 72:
ActualParameter -> OrdinalExpression
"""
def actualParameter(formalParams):
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 72: ActualParameter -> OrdinalExpression"
            pointer = formalParams['pointer']### get the current Attribute and Increment the pointer
            if formalParams['attributes'][pointer]:
                formalParam = formalParams['attributes'][pointer]
                formalParams['pointer'] = pointer + 1
            else:
                formalParam = None
            if formalParam is not None:
                expr = ordinalExpression(formalParam)
                analyzer.genParamCast(expr, {'type':recTypes.FORMAL_PARAM, 'formalType':formalParam['type'], 'formalMode':formalParam['mode']})
            else:
                semanticError("Too many parameters for: " + formalParams['name'])
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
"""
Rule 73:
Expression -> SimpleExpression OptionalRelationalPart
"""
def expression(formalParam):
    expr = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 73: Expression -> SimpleExpression OptionalRelationalPart"
            simpExpr = simpleExpression(formalParam)
            optPt = optionalRelationalPart(simpExpr)
            if optPt:
                expr = optPt
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
def optionalRelationalPart(left):
    optPt = {}
    if lookAhead.getType() == types.MP_COMMA or \
        lookAhead.getType() == types.MP_RPAREN or \
        lookAhead.getType() == types.MP_DOWNTO or \
        lookAhead.getType() == types.MP_TO or \
        lookAhead.getType() == types.MP_DO or \
        lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_THEN or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END:
            #print "Extending Rule 75: OptionalRelationalPart -> Lambda"
            Lambda()
    elif lookAhead.getType() == types.MP_NEQUAL or \
        lookAhead.getType() == types.MP_GEQUAL or \
        lookAhead.getType() == types.MP_LEQUAL or \
        lookAhead.getType() == types.MP_GTHAN or \
        lookAhead.getType() == types.MP_LTHAN or \
        lookAhead.getType() == types.MP_EQUAL:
            #print "Extending Rule 74: OptionalRelationalPart -> RelationalOperator SimpleExpression"
            opt = relationalOperator()
            right = simpleExpression(None)
            analyzer.genOptRelPart(left, opt, right)
            optPt = {'type':recTypes.LITERAL, 'varType':varTypes.BOOLEAN}
    else:
        syntaxError("',', ), downto, to, do, until, else, then, ;, end, <>, >=, <=, >, <, =")
    return optPt
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
    relOp = {}
    if lookAhead.getType() == types.MP_EQUAL:
        #print "Extending Rule 76: RelationalOperator -> '='"
        match(types.MP_EQUAL)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_EQUAL}
    elif lookAhead.getType() == types.MP_NEQUAL:
        #print "Extending Rule 81: RelationalOperator -> '<>'"
        match(types.MP_NEQUAL)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_NEQUAL}
    elif lookAhead.getType() == types.MP_GEQUAL:
        #print "Extending Rule 80: RelationalOperator -> '>='"
        match(types.MP_GEQUAL)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_GEQUAL}
    elif lookAhead.getType() == types.MP_LEQUAL:
        #print "Extending Rule 79: RelationalOperator -> '<='"
        match(types.MP_LEQUAL)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_LEQUAL}
    elif lookAhead.getType() == types.MP_GTHAN:
        #print "Extending Rule 78: RelationalOperator -> '>'"
        match(types.MP_GTHAN)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_GTHAN}
    elif lookAhead.getType() == types.MP_LTHAN:
        #print "Extending Rule 77: RelationalOperator -> '<'"
        match(types.MP_LTHAN)
        relOp = {'type':recTypes.REL_OP, 'token':types.MP_LTHAN}
    else:
        syntaxError("<>, >=, <= , >, <, =")
    return relOp
"""
Rule 82:
SimpleExpression -> OptionalSign Term TermTail
"""
def simpleExpression(formalParam):
    simpExpr = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 82: SimpleExpression -> OptionalSign Term TermTail"
            opt = optionalSign()
            thisTerm = term(formalParam)
            analyzer.genOptSimNeg(opt, thisTerm)
            thisTermTail = termTail(thisTerm)
            if thisTermTail is None:
                thisTermTail = thisTerm
            simpExpr = thisTermTail
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return simpExpr
"""
Rule 83 and 84:
TermTail -> AddingOperator Term TermTail
         -> Lambda
"""
def termTail(left):
    thisTermTail = None
    if lookAhead.getType() == types.MP_COMMA or \
        lookAhead.getType() == types.MP_RPAREN or \
        lookAhead.getType() == types.MP_NEQUAL or \
        lookAhead.getType() == types.MP_GEQUAL or \
        lookAhead.getType() == types.MP_LEQUAL or \
        lookAhead.getType() == types.MP_GTHAN or \
        lookAhead.getType() == types.MP_LTHAN or \
        lookAhead.getType() == types.MP_EQUAL or \
        lookAhead.getType() == types.MP_DOWNTO or \
        lookAhead.getType() == types.MP_TO or \
        lookAhead.getType() == types.MP_DO or \
        lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_THEN or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END:
            #print "Extending Rule 84: TermTail -> Lambda"
            Lambda()
    elif lookAhead.getType() == types.MP_OR or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 83: TermTail -> AddingOperator Term TermTail"
            addOp = addingOperator()
            thisTerm = term(None)
            analyzer.genAddOp(left, addOp, thisTerm)
            thisTermTail = termTail(thisTerm)
            if thisTermTail is None:
                thisTermTail = thisTerm
    else:
        syntaxError("',', ), <>, >=, <=, >, <, =, downto, to, do, until, else, then, ;, end, or, -, +")
    return thisTermTail
"""
Rule 85, 86 and 87:
OptionalSign -> "+"
             -> "-"
             -> Lambda
"""
def optionalSign():
    optSign = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT:
            #print "Extending Rule 87: OptionalSign -> : Lambda"
            Lambda()
    elif lookAhead.getType() == types.MP_MINUS:
        #print "Extending Rule 86: OptionalSign -> '-'"
        match(types.MP_MINUS)
        optSign = {'type':recTypes.OPTIONAL_SIGN, 'tokenType':types.MP_MINUS}
    elif lookAhead.getType() == types.MP_PLUS:
        #print "Extending Rule 85: OptionalSign -> '+'"
        match(types.MP_PLUS)
        optSign = {'type':recTypes.OPTIONAL_SIGN, 'tokenType':types.MP_PLUS}
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return optSign
"""
Rule 88, 89 and 90:
AddingOperator -> "+"
               -> "-"
               -> "or"
"""
def addingOperator():
    addOp = None
    if lookAhead.getType() == types.MP_OR:
        #print "Extending Rule 90: AddingOperator -> 'or'"
        match(types.MP_OR)
        addOp = {'type':recTypes.ADD_OP, 'tokenType':types.MP_OR}
    elif lookAhead.getType() == types.MP_MINUS:
        #print "Extending Rule 89: AddingOperator -> '-'"
        match(types.MP_MINUS)
        addOp = {'type':recTypes.ADD_OP, 'tokenType':types.MP_MINUS}
    elif lookAhead.getType() == types.MP_PLUS:
        #print "Extending Rule 88: AddingOperator -> '+'"
        match(types.MP_PLUS)
        addOp = {'type':recTypes.ADD_OP, 'tokenType':types.MP_PLUS}
    else:
        syntaxError("or, -, +")
    return addOp
"""
Rule 91:
Term -> Factor FactorTail
"""
def term(formalParam):
    thisTerm = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT:
            #print "Extending Rule 91: Term -> Factor FactorTail"
            thisFactor = factor(formalParam)
            thisFactorTail = factorTail(thisFactor)
            if thisFactorTail is None:
                thisFactorTail = thisFactor
            thisTerm = thisFactorTail
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer")
    return thisTerm
"""
Rule 92 and 93:
FactorTail -> MultiplyingOperator Factor FactorTail
           -> Lambda
"""
def factorTail(left):
    thisFactorTail = None
    if lookAhead.getType() == types.MP_COMMA or \
        lookAhead.getType() == types.MP_RPAREN or \
        lookAhead.getType() == types.MP_OR or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS or \
        lookAhead.getType() == types.MP_NEQUAL or \
        lookAhead.getType() == types.MP_GEQUAL or \
        lookAhead.getType() == types.MP_LEQUAL or \
        lookAhead.getType() == types.MP_GTHAN or \
        lookAhead.getType() == types.MP_LTHAN or \
        lookAhead.getType() == types.MP_EQUAL or \
        lookAhead.getType() == types.MP_DOWNTO or \
        lookAhead.getType() == types.MP_TO or \
        lookAhead.getType() == types.MP_DO or \
        lookAhead.getType() == types.MP_UNTIL or \
        lookAhead.getType() == types.MP_ELSE or \
        lookAhead.getType() == types.MP_THEN or \
        lookAhead.getType() == types.MP_SCOLON or \
        lookAhead.getType() == types.MP_END:
            #print "Extending Rule 93: FactorTail -> Lambda"
            Lambda()
    elif lookAhead.getType() == types.MP_AND or \
        lookAhead.getType() == types.MP_MOD or \
        lookAhead.getType() == types.MP_DIV or \
        lookAhead.getType() == types.MP_FLOAT_DIVIDE or \
        lookAhead.getType() == types.MP_TIMES:
            #print "Extending Rule 92: FactorTail -> MultiplyingOperator Factor FactorTail"
            thisMulOp = multiplyingOperator()
            thisFactor = factor(None)
            thisFactor = analyzer.genMulOp(left, thisMulOp, thisFactor)
            thisFactorTail = factorTail(thisFactor)
            if thisFactorTail is None:
                thisFactorTail = thisFactor
    else:
        syntaxError("',', ), or, -, +, <>, >=, <=, >, <, =, downto, to, do, until, else, then, ;, end, and, mod, div, / , *")
    return thisFactorTail
"""
Rule 94, 95, 96, 97 and 98:
MultiplyingOperator -> "*"
                    -> "/"
                    -> "div"
                    -> "mod"
                    -> "and"
"""
def multiplyingOperator():
    thisMulOp = None
    if lookAhead.getType() == types.MP_TIMES:
        #print "Extending Rule 94: MultiplyingOperator -> '*'"
        match(types.MP_TIMES)
        thisMulOp = {'type':recTypes.MUL_OP, 'tokenType':types.MP_TIMES}
    elif lookAhead.getType() == types.MP_FLOAT_DIVIDE:
        #print "Extending Rule 95: MultiplyingOperator -> '/'"
        match(types.MP_FLOAT_DIVIDE)
        thisMulOp = {'type':recTypes.MUL_OP, 'tokenType':types.MP_FLOAT_DIVIDE}
    elif lookAhead.getType() == types.MP_DIV:
        #print "Extending Rule 96: MultiplyingOperator -> 'div'"
        match(types.MP_DIV)
        thisMulOp = {'type':recTypes.MUL_OP, 'tokenType':types.MP_DIV}
    elif lookAhead.getType() == types.MP_MOD:
        #print "Extending Rule 97: MultiplyingOperator -> 'mod'"
        match(types.MP_MOD)
        thisMulOp = {'type':recTypes.MUL_OP, 'tokenType':types.MP_MOD}
    elif lookAhead.getType() == types.MP_AND:
        #print "Extending Rule 98: MultiplyingOperator -> 'and'"
        match(types.MP_AND)
        thisMulOp = {'type':recTypes.MUL_OP, 'tokenType':types.MP_AND}
    else:
        syntaxError("and, mod, div, / , *")
    return thisMulOp
"""
Rule 99, 100, 101, 102, 103, 104, 105 and 106:
Factor -> UnsignedInteger
       -> UnsignedFloat
       -> StringLiteral
       -> "True"
       -> "False"
       -> "not" Factor
       -> "(" Expression ")"
       -> FunctionIdentifier OptionalActualParameterList
"""
def factor(formalParam):
    factorRec = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        factorVar = analyzer.findSymbol(lookAhead.getLexeme(), None)
        if factorVar is not None:
            if factorVar['classification'] == classification.VARIABLE or factorVar['classification'] == classification.PARAMETER:
                #print "Extending Rule: Factor -> VariableIdentifier"
                varId = variableIdentifier()
                factorRec = {'type':recTypes.IDENTIFIER, 'classification':factorVar['classification'], 'lexeme':varId}
                if formalParam is not None:
                    formalParamRec = {'type':recTypes.FORMAL_PARAM, 'formalType':formalParam['type'], 'formalMode':formalParam['mode']}
                    factorRec = analyzer.genPushIdWithFormalParam(factorRec, formalParamRec)
                else: 
                    factorRec = analyzer.genPushId(factorRec)
            elif factorVar['classification'] == classification.FUNCTION:
                #print "Extending Rule 106: Factor -> FunctionIdentifier OptionalActualParameterList"
                funcId = functionIdentifier()
                analyzer.genComment("call to " + funcId + " start")
                analyzer.genSPslot() # reserve space for return value
                analyzer.genSPslot() # reserve space for the register slot
                formalParams = {'name':funcId, 'attributes':factorVar['attributes'], 'pointer':0}
                optionalActualParameterList(formalParams)
                funcRec = {'type':recTypes.IDENTIFIER, 'classification':classification.FUNCTION, 'controlId':funcId}
                analyzer.genFuncCall(funcRec)
                analyzer.genComment("call to " + funcId + " end")
                factorRec = {'type':recTypes.LITERAL, 'varType':factorVar['type']}
            else:
                semanticError("Cannot use proc identifier '" + lookAhead.getLexeme() + "' as factor")
        else:
            semanticError("Undeclared identifier: '" + lookAhead.getLexeme() + "'")
    elif lookAhead.getType() == types.MP_LPAREN:
        #print "Extending Rule 105: Factor -> '(' Expression ')'"
        match(types.MP_LPAREN)
        factorRec = expression(None)
        match(types.MP_RPAREN)
    elif lookAhead.getType() == types.MP_NOT:
        #print "Extending Rule 104: Factor -> 'not' Factor"
        match(types.MP_NOT)
        factorRec = factor(None)
        analyzer.genNotBool(factorRec)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.BOOLEAN}
    elif lookAhead.getType() == types.MP_INTEGER_LIT:
        #print "Extending Rule 99: Factor -> UnsignedInteger"
        lex = lookAhead.getLexeme()
        match(types.MP_INTEGER_LIT)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.INTEGER}
        analyzer.genPushLit(factorRec, lex)
    elif lookAhead.getType() == types.MP_FALSE:
        #print "Extending Rule 103: Factor -> 'False'"
        lex = lookAhead.getLexeme()
        match(types.MP_FALSE)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.BOOLEAN}
        analyzer.genPushLit(factorRec, lex)
    elif lookAhead.getType() == types.MP_TRUE:
        #print "Extending Rule 102: Factor -> 'True'"
        lex = lookAhead.getLexeme()
        match(types.MP_TRUE)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.BOOLEAN}
        analyzer.genPushLit(factorRec, lex)
    elif lookAhead.getType() == types.MP_STRING_LIT:
        #print "Extending Rule 101: Factor -> StringLiteral"
        lex = lookAhead.getLexeme()
        match(types.MP_STRING_LIT)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.STRING}
        analyzer.genPushLit(factorRec, lex)
    elif lookAhead.getType() == types.MP_FLOAT_LIT:
        #print "Extending Rule 100: Factor -> UnsignedFloat"
        lex = lookAhead.getLexeme()
        match(types.MP_FLOAT_LIT)
        factorRec = {'type':recTypes.LITERAL, 'varType':varTypes.FLOAT}
        analyzer.genPushLit(factorRec, lex)
    else:
        syntaxError("identifier, (, not, Integer, false, true, String, Float")
    return factorRec
"""
Rule 107:
ProgramIdentifier -> Identifier
"""
def programIdentifier():
    progId = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 107: ProgramIdentifier -> Identifier"
        progId = lookAhead.getLexeme()
        match(types.MP_IDENTIFIER)
    else:
        syntaxError("identifier")
    return progId
"""
Rule 108:
VariableIdentifier -> Identifier
"""
def variableIdentifier():
    lex = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        "Extending Rule 108: VariableIdentifier -> Identifier"
        lex = lookAhead.getLexeme()
        match(types.MP_IDENTIFIER)
    else:
        syntaxError("identifier")
    return lex
"""
Rule 109:
ProcedureIdentifier -> Identifier
"""
def procedureIdentifier():
    procId = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 109: ProcedureIdentifier -> Identifier"
        procId = lookAhead.getLexeme()
        match(types.MP_IDENTIFIER)
    else:
        syntaxError("identifier")
    return procId
"""
Rule 110:
FunctionIdentifier -> Identifier
"""
def functionIdentifier():
    funcId = None
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 110: FunctionIdentifier -> Identifier"
        funcId = lookAhead.getLexeme()
        match(types.MP_IDENTIFIER)
    else:
        syntaxError("identifier")
    return funcId
"""
Rule 111:
BooleanExpression -> Expression
"""
def booleanExpression():
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 111: BooleanExpression -> Expression"
            semRec = expression(None)
            if semRec['type'] == recTypes.LITERAL:
                varType = semRec['varType']
                if varType != varTypes.BOOLEAN:
                    semanticError("BooleanExpression requires a bool literal type, but found type: " + str(varType))
            elif semRec['type'] == recTypes.IDENTIFIER:
                rowData = analyzer.findSymbol(semRec['lexeme'], semRec['classification'])
                varType = rowData['type']
                if varType != varTypes.BOOLEAN:
                    semanticError("BooleanExpression requires a bool identifier type, but found: " + str(semRec['lexeme']) + " with type: " + str(varType))
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
"""
Rule 112:
OrdinalExpression -> Expression
"""
def ordinalExpression(formalParam):
    ordRec = None
    if lookAhead.getType() == types.MP_IDENTIFIER or \
        lookAhead.getType() == types.MP_FALSE or \
        lookAhead.getType() == types.MP_TRUE or \
        lookAhead.getType() == types.MP_STRING_LIT or \
        lookAhead.getType() == types.MP_FLOAT_LIT or \
        lookAhead.getType() == types.MP_LPAREN or \
        lookAhead.getType() == types.MP_NOT or \
        lookAhead.getType() == types.MP_INTEGER_LIT or \
        lookAhead.getType() == types.MP_MINUS or \
        lookAhead.getType() == types.MP_PLUS:
            #print "Extending Rule 112: OrdinalExpression -> Expression"
            ordRec = expression(formalParam)
    else:
        syntaxError("identifier, false, true, String, Float, (, not, Integer, -, +")
    return ordRec
"""
Rule 113:
IdentifierList -> Identifier IdentifierTail
"""
def identifierList():
    idList = []
    if lookAhead.getType() == types.MP_IDENTIFIER:
        #print "Extending Rule 113: IdentifierList -> Identifier IdentifierTail"
        idList.append(lookAhead.getLexeme())
        match(types.MP_IDENTIFIER)
        identifierTail(idList)
    else:
        syntaxError("identifier")
    return idList
"""
Rule 114 and 115:
IdentifierTail -> "," Identifier IdentifierTail
               -> Lambda
"""
def identifierTail(idList):
    if lookAhead.getType() == types.MP_COMMA:
        #print "Extending Rule 114: IdentifierTail -> ',' Identifier IdentifierTail"
        match(types.MP_COMMA)
        idList.append(lookAhead.getLexeme())
        match(types.MP_IDENTIFIER)
        identifierTail(idList)
    elif lookAhead.getType() == types.MP_COLON:
        #print "Extending Rule 115: IdentifierTail -> Lambda"
        Lambda()
    else:
        syntaxError("',', :")