import sys
sys.path.insert(0, '../')
from Parser import recordTypes as recTypes
from tokenTypes import types as tokenTypes
sys.path.insert(0, '../Parser/')
from Parser.Symbol import symbolTable
import parser as parser
from Parser.classifications import classification
from Parser.modes import mode
from Parser.types import varTypes

class Analyzer:
    o = None
    symbolTables = None
    
    def __init__(self, tables):
        global symbolTables, o
        o = open('../output.up', 'w')
        symbolTables = tables
        
    # --------------------------------------------------------------
    # Symbol Tables Functions
    # --------------------------------------------------------------
    """
    Can pass either the symbol table name or symbol in the table
    """
    def findSymbolTable(self, element):
        tables = symbolTables.reverse()
        for table in tables:
            st = tables[table]
            if st.contains(element):
                return st
            elif st.getScopeName() == element:
                return st
            else:
                continue
        return None
    """
    Calls one of two findSymbol functions on the table depending on
    if the classification is passed or not
    """
    def findSymbol(self, lex, c):
        tables = symbolTables.reverse()
        for table in tables:
            st = tables[table]
            if c is not None:
                if st.findSymbol(lex, c):
                    return st
            else:
                if st.findSymbol(lex):
                    return st
        return None
    # --------------------------------------------------------------
    # Error Handling
    # --------------------------------------------------------------
    def semanticError(self, inputError):
        sys.exit("Semantic error: " + inputError)
    # --------------------------------------------------------------
    # Semantic Record Helper Functions
    # --------------------------------------------------------------
    def getSemRecType(self, rec):
        t = None
        if rec['type'] == recTypes.IDENTIFIER:
            r = self.getSemRecIdRow(rec)
            t = r['type']
        elif rec['type'] == recTypes.LITERAL:
            t = rec['type']
        else:
            self.semanticError("Record type: " + str(rec['type']) + " does not have a type.")
        return t
    
    def getSemRecIdRow(self, rec):
        lex = rec['lexeme']
        c = rec['classification']
        r = self.findSymbol(lex, c)
        if r is None:
            self.semanticError("Identifier: type " + str(c) + " lexeme " + str(lex) + " is not declared in current scope.")
        return r
    
    def generateOffset(table, data):
        nestingLvl = str(table.getNestingLevel())
        memOffset = str(data['offset'])
        nestingLvl = 'D' + nestingLvl
        return memOffset + '(' + nestingLvl + ')'
    # --------------------------------------------------------------
    # VM Assembly Functions
    # --------------------------------------------------------------
    def genHLT(self):
        o.write("HLT")
    
    def genRead(self, readRec, isVar):
        thisRow = self.getSemRecIdRow(readRec)
        thisType = thisRow['type']
        thisTable = self.findSymbolTable(thisRow)
        if isVar:
            thisoffset = self.generateOffset(thisTable, thisRow)
        else:
            thisoffset = "@" + self.generateOffset(thisTable, thisRow)
    
        if thisType == varTypes.INTEGER:
            self.genRD(thisoffset)
        elif thisType == varTypes.FLOAT:
            self.genRDF(thisoffset)
        elif thisType == varTypes.STRING:
            self.genRDS(thisoffset)
        else:
            self.semanticError("Can't read into a variable of " + str(thisType))
    
    def genRD(self, offset):
        o.write("RD " + offset)
    
    def genRDF(self, offset):
        o.write("RDF " + offset)
    
    def genRDS(self, offset):
        o.write("RDS " + offset)
    
    def genWrite(self, writeRec, expRec):
        if writeRec['tokenType'] == tokenTypes.MP_WRITE:
            self.genWRTS()
        else:
            self.genWRTLNS()
    
    def genWRTS(self):
        o.write("WRTS")
    
    def genWRTLN(self):
        o.write("WRTLN")
    
    def genWRTLNS(self):
        o.write("WRTLNS")
    
    def genMOV(self, src, dst):
        o.write("MOV " + str(src) + " " + str(dst))
    
    def genADD(self, src1, src2, dst):
        o.write("ADD " + str(src1) + " " + str(src2) + " " + str(dst))
    
    def genSUB(self, src1, src2, dst):
        o.write("SUB " + str(src1) + " " + str(src2) + " " + str(dst))
    
    def genNEGF(self):
        o.write("NEGF")
    
    def genADDF(self):
        o.write("ADDF")
    
    def genSUBF(self):
        o.write("SUBF")
    
    def genMULF(self):
        o.write("MULF")
    
    def genDIVF(self):
        o.write("DIVF")
    
    def genPUSH(self, location):
        o.write("PUSH " + str(location))
    
    def genPOP(self, location):
        o.write("POP " + str(location))
    
    def genNEGS(self):
        o.write("NEGS")
    
    def genADDS(self):
        o.write("ADDS")
    
    def genSUBS(self):
        o.write("SUBS")
    
    def genMULS(self):
        o.write("MULS")
    
    def genDIVS(self):
        o.write("DIVS")
    
    def genMODS(self):
        o.write("MODS")
    
    def genNEGSF(self):
        o.write("NEGSF")
    
    def genADDSF(self):
        o.write("ADDSF")
    
    def genSUBSF(self):
        o.write("SUBSF")
    
    def genMULSF(self):
        o.write("MULSF")
    
    def genMODSF(self):
        o.write("MODSF")
    
    def genDIVSF(self):
        o.write("DIVSF")
    
    def genCASTSI(self):
        o.write("CASTSI")
    
    def genCASTSF(self):
        o.write("CASTSF")
    
    def genANDS(self):
        o.write("ANDS")
    
    def genORS(self):
        o.write("ORS")
    
    def genNOTS(self):
        o.write("NOTS")
    
    def genCMPEQS(self):
        o.write("CMPEQS")
    
    def genCMPGES(self):
        o.write("CMPGES")
    
    def genCMPGTS(self):
        o.write("CMPGTS")
    
    def genCMPLES(self):
        o.write("CMPLES")
    
    def genCMPLTS(self):
        o.write("CMPLTS")
    
    def genCMPNES(self):
        o.write("CMPNES")
    
    def genCMPEQSF(self):
        o.write("CMPEQSF")
    
    def genCMPGESF(self):
        o.write("CMPGESF")
    
    def genCMPGTSF(self):
        o.write("CMPGTSF")
    
    def genCMPLESF(self):
        o.write("CMPLESF")
    
    def genCMPLTSF(self):
        o.write("CMPLTSF")
    
    def genCMPNESF(self):
        o.write("CMPNESF")
    
    def genBRTS(self):
        o.write("BRTS")
    
    def genBRFS(self):
        o.write("BRFS")
    
    def genBR(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            o.writeln("BR " + nameRec['label'])
        else:
            self.semanticError("Called genBR with type other than LABEL")
    
    def label(self, label):
        o.write(label + ':')
    
    def genLabel(self):
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        self.label(label)
        return lblRec
    
    def genSpecLabel(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.label(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genActRec(self, nameRec, blockType):
        if blockType['type'] == recTypes.BLOCK:
            block = blockType['label']
            table = self.findSymbolTable(nameRec['label'])
            varCount = table.getVarCount()
            parCount = table.getParCount()
            if block == "program":
                self.genComment(nameRec['label'] + ' start')
                o.write("SP #1 SP") # reserve space for old register value
                o.write("SP #" + varCount + " SP") # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + 1) + '(SP)'
                self.genMOV(register, offset)
                self.genSUB("SP", "#" + (varCount + 1), register)
                self.genComment("activation end")
            elif block == "procedure" or block == "function":
                self.genComment(nameRec['label'] + ' start')
                self.genADD('SP', '#' + varCount, 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + parCount + 2) + '(SP)' # slot for both return address and old register value
                self.genMOV(register, offset)
                self.genSUB("SP", "#" + (varCount + parCount + 2), register)
                self.genComment("activation end")
            else:
                self.semanticError("Block type: " + block + " is not supported")
        else:
            self.semanticError("Semantic record: " + str(blockType['type']) + " is not supported for recType.BLOCK param")
    
    """
    Generate Program Deactivation Record
    """
    def genProgDR(self, nameRec):
        table = self.findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + 1) + '(SP)'
        self.genComment('deactivation start')
        self.genMOV(offset, register)
        self.genSUB('SP', '#' + (varCount + 1), 'SP')
        self.genComment(nameRec['label'] + ' end')
    
    """
    Generate Procedure Deactivation Record
    """
    def genProcDR(self, nameRec):
        table = self.findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        parCount = table.getParCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + parCount + 2) + '(SP)'
        self.genComment('deactivation start')
        self.genMOV(offset, register)
        self.genSUB('SP', '#' + (varCount), 'SP')
        self.ret()
        self.genComment(nameRec['label'] + ' end')
    
    """
    Generate Procedure Call
    """
    def genProcCall(self, procRec):
        row = self.getSemRecIdRow(procRec)
        label = row['branch']
        self.genCALL(label)
        paramSize = len(row['attributes'])
        self.genSUB('SP', '#' + str(paramSize + 1), 'SP')
    
    """
    Generate Function Call
    """
    def genFuncCall(self, funcRec):
        row = self.getSemRecIdRow(procRec)
        label = row['branch']
        self.genCALL(label)
        paramSize = len(row['attributes'])
        self.genSUB('SP', '#' + str(paramSize + 1), 'SP')
    
    def genBEQ(self):
        o.write("BEQ")
    
    def genBGE(self):
        o.write("BGE")
    
    def genBGT(self):
        o.write("BGT")
    
    def genBLE(self):
        o.write("BLE")
    
    def genBLT(self):
        o.write("BLT")
    
    def genBNE(self):
        o.write("BNE")
    
    def genBEQF(self):
        o.write("BEQF")
    
    def genBGEF(self):
        o.write("BGEF")
    
    def genBFTF(self):
        o.write("BGTF")
    
    def genBLEF(self):
        o.write("BLEF")
    
    def genBLTF(self):
        o.write("BLTF")
    
    def genBNEF(self):
        o.write("BNEF")
    
    def genCALL(self, label):
        o.write("CALL " + str(label))
    
    def genRET(self):
        o.write("RET")
    
    def genPRTS(self):
        o.write("PRTS")
    
    def genPRTR(self):
        o.write("PRTR")
    
    def genSPslot(self):
        self.genADD('SP', '#1', 'SP')
    
    def brUncond(self, label):
        o.write('BR ' + str(label))
    
    def genPushId(self, factor):
        factorClass = factor['classification']
        rowData = self.getSemRecIdRow(factor)
        table = self.findSymbolTable(rowData)
        offset = self.generateOffset(table, rowData)
        if factorClass == classification.VARIABLE:
            self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
            self.genPUSH(offset)
        elif factorClass == classification.PARAMETER:
            paramMode = rowData['mode']
            if paramMode == mode.VALUE:
                self.genComment("push param class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                self.genPUSH(offset)
            elif paramMode == mode.VARIABLE:
                self.genComment("push param class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                self.genPUSH('@' + str(offset))
        return {'type':recTypes.LITERAL, 'rowType':rowData['type']}
    
    def genPushIdWithFormalParam(self, factor, formalParamRec):
        returnVal = None
        rowData = self.getSemRecIdRow(factor)
        table = self.findSymbolTable(rowData)
        formalParamType = formalParamRec['formalType']
        formalParamMode = formalParamRec['formalMode']
        actualParamType = None
        actualParamMode = None
        varClass = False
        if factor['classification'] == classification.VARIABLE:
            row = self.findSymbol(factor['varId'], classification.VARIABLE)
            actualParamType = row['type']
            actualParamMode = row['mode']
            varClass = True
        elif factor['classification'] == classification.PARAMETER:
            row = self.findSymbol(factor['varId'], classification.PARAMETER)
            actualParamType = row['type']
            actualParamMode = row['mode']
            varClass = False
        if actualParamType is not None and actualParamMode is not None:
            if formalParamMode == mode.VALUE:
                if actualParamMode == mode.VALUE:
                    offset = self.generateOffset(table, rowData)
                    returnVal = {'type':recTypes.LITERAL, 'rowType':rowData['type']}
                    self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                    self.genPUSH(offset)
                elif actualParamMode == mode.VARIABLE:
                    if varClass:
                        offset = self.generateOffset(table, rowData)
                        returnVal = {'type':recTypes.LITERAL, 'rowType':rowData['type']}
                        self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                        self.genPUSH(offset)
                    else:
                        offset = '@' + self.generateOffset(table, rowData)
                        returnVal = {'type':recTypes.LITERAL, 'rowType':rowData['type']}
                        self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                        self.genPUSH(offset)
            elif formalParamMode == mode.VARIABLE:
                if actualParamMode == mode.VALUE:
                    self.semanticError("Cannot send 'mode:value, actual parameter' " + factor['varId'] + " into 'mode: variable, formal param' procedure/function")
                elif actualParamMode == mode.VARIABLE:
                    if formalParamType == actualParamType:
                        if varClass:
                            register = 'D' + table['nestinglvl']
                            offset = rowData['offset']
                            returnVal = factor
                            self.genComment("push address class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                            self.genPUSH(register)
                            self.genPUSH('#' + offset)
                            self.genADDS()
                        else:
                            returnVal = factor
                            offset = self.generateOffset(table, rowData)
                            self.genComment("push address class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                            self.genPUSH(offset)
                    else:
                        self.semanticError("mode variable actual param type: " + actualParamType + " must match the mode variable formal param type of: " + formalParamType)
            else:
                self.semanticError("actual parameter does not have a valid mode")
        return returnVal
    
    def genCastDivision(self, left, right):
        leftType = self.getSemRecType(left)
        rightType = self.getSemRecType(right)
        arrayRec = []
        castL = False
        castR = False
        if leftType == varTypes.FLOAT:
            arrayRec[0] = left
            castL = True
        elif leftType == varTypes.INTEGER:
            self.genComment("start cast left to float")
            self.genSUB('SP', '#1', 'SP') # move to the left variable on stack
            self.genCASTSF()
            self.genADD('SP', '#1', 'SP') # move back
            self.genComment("end cast left to float")
            arrayRec[0] = {'type':recTypes.LITERAL, 'varType':varTypes.FLOAT}
            castL = True
        else:
            castL = False
        if rightType == varTypes.FLOAT:
            arrayRec[1] = left
            castR = True
        elif rightType == varTypes.INTEGER:
            self.genCASTSF()
            arrayRec[1] = {'type':recTypes.LITERAL, 'varType':varTypes.FLOAT}
            castR = True
        else:
            castR = False
        if castL == False or castR == False:
            self.semanticError("Invalid cast from: " + rightType + " to " + leftType)
            return None
        return arrayRec
    
    def genCast(self, left, right):
        leftType = self.getSemRecType(left)
        rightType = self.getSemRecType(right)
        arrayRec = []
        if leftType == rightType:
            arrayRec[0] = left
            arrayRec[1] = right
        elif leftType == varTypes.INTEGER and rightType == varTypes.FLOAT:
            self.genComment("start cast left to float")
            self.genSUB('SP', '#1', 'SP') # move to the left variable on stack
            self.genCASTSF()
            self.genADD('SP', '#1', 'SP') # move back
            self.genComment("end cast left to float")
            arrayRec[0] = {'type':recTypes.LITERAL, 'varType':varTypes.FLOAT}
            arrayRec[1] = right
        elif leftType == varTypes.FLOAT and rightType == varTypes.INTEGER:
            self.genCASTSI()
            arrayRec[0] = left
            arrayRec[1] = {'type':recTypes.LITERAL, 'varType':varTypes.FLOAT}
        else:
            self.semanticError("Invalid casting from " + rightType + " to " + leftType)
            return None
        return arrayRec
    
    def checkTypesInt(left, right):
        leftType = self.getSemRecType(left)
        rightType = self.getSemRecType(right)
        if leftType != varTypes.INTEGER or rightType != varTypes.INTEGER:
            self.semanticError("The div operator only works on integer operand. Left operand: " + leftType + ", right operand: " + rightType)
    
    def genMulOp(self, left, mulOp, right):
        results = []
        op = mulOp['tokenType']
        if op == tokenTypes.MP_DIV_INT:
            self.checkTypesInt(left, right)
            self.genDIVS()
            resultType = varTypes.INTEGER
        elif op == tokenTypes.MP_DIV:
            results = self.genCastDivision(left, right)
            resultType = self.getSemRecType(results[0])
            self.genDIVSF()
        else:
            results = self.genCast(left, right)
            resultType = self.getSemRecType(results[0])
            if resultType == varTypes.INTEGER:
                if op == tokenTypes.MP_MOD:
                    self.genMODS()
                elif op == tokenTypes.MP_TIMES:
                    self.genMULS()
                else:
                    self.semanticError(op + " is not a mult op for type: " + resultType)
            elif resultType == varTypes.FLOAT:
                if op == tokenTypes.MP_MOD:
                    self.genMODSF()
                elif op == tokenTypes.MP_TIMES:
                    self.genMULSF()
                else:
                    self.semanticError(op + " is not a mult op for type: " + resultType)
            elif resultType == varTypes.BOOLEAN:
                if op == tokenTypes.MP_AND:
                    self.genANDS()
                else:
                    self.semanticError(op + " is not a mult op for type: " + resultType)
            else:
                self.semanticError(resultType + " does not have a mult op")
        return {'type':recTypes.LITERAL, 'resultType':resultType}
    
    def genAddOp(self, left, addOp, right):
        results = genCast(left, right)
        resultType = self.getSemRecType(results[0])
        op = addOp['tokenType']
        if resultType == varTypes.INTEGER:
            if op == tokenTypes.MP_MINUS:
                self.genSUBS()
            elif op == tokenTypes.MP_PLUS:
                self.genADDS()
            else:
                self.semanticError(opSign + " is not an addOp for type: " + resultType)
        elif resultType == varTypes.FLOAT:
            if op == tokenTypes.MP_MINUS:
                self.genSUBSF()
            elif op == tokenTypes.MP_PLUS:
                self.genADDSF()
            else:
                self.semanticError(opSign + " is not an addOp for type: " + resultType)
        elif resultType == varTypes.BOOLEAN:
            if op == tokenTypes.MP_MINUS:
                self.genORS()
            else:
                self.semanticError(opSign + " is not an addOp for type: " + resultType)
        else:
            self.semanticError(resultType + " does not have adding operation")
        return {'type':recTypes.LITERAL, 'resultType':resultType}
    
    def genOptSimNeg(self, opSign, term):
        if opSign is not None and term is not None:
            termType = self.getSemRecType(term)
            op = opSign['sign']
            if termType == varTypes.INTEGER:
                if op == tokenTypes.MP_MINUS:
                    self.genNEGS()
                elif op == tokenTypes.MP_PLUS:
                    # do not throw sem error, but do nothing
                else:
                    self.semanticError(opSign + " is not a neg op for type: " + termType)
            elif termType == varTypes.FLOAT:
                if op == tokenTypes.MP_MINUS:
                    self.genNEGSF()
                elif op == tokenTypes.MP_PLUS:
                    # do not throw sem error, but do nothing
                else:
                    self.semanticError(opSign + " is not a neg op for type: " + termType)
            else:
                self.semanticError(termType + " does not have a neg operation")
    
    def genPushLit(self, lit, lex):
        litType = lit['type']
        self.genComment("push lexeme: " + lex + ", type: " + str(litType))
        if litType == varTypes.STRING:
            self.genPUSH("#\"" + lex + "\"")
        elif litType == varTypes.BOOLEAN:
            if lex == "true":
                self.genPUSH('#1')
            else:
                self.genPUSH('#0')
        elif litType == varTypes.INTEGER:
            self.genPUSH('#' + lex)
        elif litType == varTypes.FLOAT:
            if lex.find("e") > -1 and lex.find(".") == -1:
                split = lex.find("e") * -1
                start = str(lex[0:split])
                split = split * -1
                end = str(lex[split:])
                lex = start + ".0" + end
            self.genPUSH('#' + lex)
        else:
            self.semanticError(lex + " of type: " + str(litType) + " cannot be pushed onto the stack")
    
    def genNotBool(self, factor):
        factorType = self.getSemRecType(factor)
        if factorType == varTypes.BOOLEAN:
            genNOTS()
        else:
            self.semanticError("Not operator expected, but BOOLEAN found " + factorType)
    
    def genForController(self, controlRec, forDir):
        inc = False
        if forDir['type'] == recTypes.FOR_DIRECTION:
            if forDir['tokenType'] == tokenTypes.MP_TO:
                inc = True
            elif forDir['tokenType'] == tokenTypes.MP_DOWNTO:
                inc = True
            else:
                self.semanticError("Invalid FOR_DIRECTION: " + forDir['tokenType'])
        else:
            self.semanticError("Cannot use non-FOR_DIRECTION rec type: " + forDir['type'])
        if controlRec['type'] == recTypes.IDENTIFIER:
            if controlRec['classification'] == classification.VARIABLE:
                row = self.findSymbol(controlRec['controlId'])
                memLocation = self.generateOffset(self.findSymbolTable(row), row)
                if inc:
                    self.genPUSH(memLocation)
                    self.genPUSH('#1')
                    self.genADDS()
                    self.genPOP(memLocation)
                else:
                    self.genPUSH(memLocation)
                    self.genPUSH('#1')
                    self.genSUBS()
                    self.genPOP(memLocation)
            else:
                self.semanticError("Cannot use non-var as control var")
        else:
            self.semanticError("Cannot use non-identifier as contorl var")
                    
    
    def genForComp(self, forDir):
        if forDir['type'] == recTypes.FOR_DIRECTION:
            if forDir['tokenType'] == tokenTypes.MP_TO:
                self.genCMPLES()
            elif forDir['tokenType'] == tokenTypes.MP_DOWNTO:
                self.genCMPGES()
            else:
                self.semanticError("Invalid FOR_DIRECTION: " + forDir['tokenType'])
        else:
            self.semanticError("Cannot use non-FOR_DIRECTION rec type: " + forDir['type'])
    
    def genAssignCast(self, leftRec, rightRec):
        leftType = self.getSemRecType(leftRec)
        rightType = self.getSemRecType(rightRec)
        returnRec = None
        if leftType == rightType:
            returnRec = rightRec
        elif leftType == varTypes.INTEGER and rightType == varTypes.FLOAT:
            self.genCASTSI()
        elif leftType == varTypes.FLOAT and rightType == varTypes.INTEGER:
            self.genCASTSF()
        else:
            self.semanticError("Invalid cast from " + rightType + " to " + leftType)
    
    def genParamCast(self, expression, formalParam):
        actualParamType = self.getSemRecType(expression)
        formalParamType = formalParam['formalType']
        formalParamMode = formalParam['formalMode']
        if expression['type'] == recTypes.LITERAL:
            if formalParamMode == mode.VALUE:
                if actualParamType != formalParamType:
                    if formalParamType == varTypes.INTEGER and actualParamType == varTypes.FLOAT:
                        self.genCASTSI()
                    elif formalParamType == varTypes.FLOAT and actualParamType == varTypes.INTEGER:
                        self.genCASTSF()
                    else:
                        self.semanticError("Invalid cast from formal param " + actualParamType + " to " + formalParamType)
            elif formalParamMode == mode.VARIABLE:
                self.semanticError("Cannot cast value 'actual parameter' to variable 'formal parameter'")
        elif expression['type'] == recTypes.IDENTIFIER:
            if formalParamMode == mode.VALUE:
                self.semanticError("Fault: the case should be handled in genPushId()")
            elif formalParamMode == mode.VARIABLE:
                if actualParamType != formalParamType:
                    self.semanticError("Actual type of 'actual parameter variable' must match 'formal parameter variable' type")
    
    def genPushVar(self, varRec):
        if varRec['type'] == recTypes.IDENTIFIER:
            if varRec['classification'] == classification.VARIABLE:
                row = self.findSymbol(varRec['controlId'])
                memLocation = self.generateOffset(self.findSymbolTable(row),row)
                self.genPUSH(memLocation)
            else:
                self.semanticError("Cannot push non-VARIABLE onto the stack.")
        else:
            self.semanticError("Cannot push non-IDENTIFIER onto the stack.")
    
    def genAssign(self, idRec, exp, symTable):
        self.genAssignCast(idRec, exp)
        leftRow = self.getSemRecIdRow(idRec)
        if leftRow['classification'] == classification.VARIABLE:
            leftTable = self.findSymbolTable(leftRow)
            leftOffset = self.generateOffset(leftTable, leftRow)
            self.pop(leftOffset)
        elif leftRow['classification'] == classification.FUNCTION:
            funcRow = leftRow
            nestingLevel = symTable['nestingLevel']
            register = 'D' + nameRec['nestingLevel']
            offset = '-1(' + register + ')'
            self.pop(offset)
            funcRow['returnValue'] = True
        elif leftRow['classification'] == classification.PARAMETER:
            leftTable = self.findSymbolTable(leftRow)
            row = leftRow
            paramMode = row['mode']
            offset = None
            if paramMode == mode.VALUE:
                offset = self.generateOffset(leftTable, row)
                self.pop(offset)
            elif paramMode == mode.VARIABLE:
                offset = '@' + self.generateOffset(leftTable, row)
                self.pop(offset)
    
    def genAssignFor(self, idRec, exp):
        idType = self.getSemRecType(idRec)
        if idType == varTypes.INTEGER:
            self.genAssign(idRec, exp, None)
        else:
            self.semanticError("The 'for' loop's control var must be of type Integer")
    
    def genBranchUncond(self):
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        self.brUncond(label)
        return lblRec
    
    def genBranchUncondTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.brUncond(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrueTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.branchTrue(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchFalseTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.branchFalse(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrue(self):
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        self.branchTrue(label)
        return lblRec
    
    def genBranchFalse(self):
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        self.branchFalse(label)
        return lblRec
    
    def genOptRelPart(self, left, op, right):
        if left is not None and op is not None and right is not None:
            results = self.genCast(left, right)
            resultType = self.getSemRecType(results[0])
            relOp = op['token']
            if resultType == tokenTypes.MP_INTEGER:
                if relOp == tokenTypes.MP_NEQUAL:
                    self.genCMPNES()
                elif relOp == tokenTypes.MP_GEQUAL:
                    self.genCMPGES()
                elif relOp == tokenTypes.MP_LEQUAL:
                    self.genCMPLES()
                elif relOp == tokenTypes.MP_GTHAN:
                    self.genCMPGTS()
                elif relOp == tokenTypes.MP_LTHAN:
                    self.genCMPLTS()
                elif relOp == tokenTypes.MP_EQUAL:
                    self.genCMPGES()
                else:
                    self.semanticError(relOp + " isn't an operator for " + resultType)
            elif resultType == tokenTypes.MP_FLOAT:
                if relOp == tokenTypes.MP_NEQUAL:
                    self.genCMPNESF()
                elif relOp == tokenTypes.MP_GEQUAL:
                    self.genCMPGESF()
                elif relOp == tokenTypes.MP_LEQUAL:
                    self.genCMPLESF()
                elif relOp == tokenTypes.MP_GTHAN:
                    self.genCMPGTSF()
                elif relOp == tokenTypes.MP_LTHAN:
                    self.genCMPLTSF()
                elif relOp == tokenTypes.MP_EQUAL:
                    self.genCMPGESF()
                else:
                    self.semanticError(relOp + " isn't an operator for " + resultType)
            else:
                self.semanticError(resultType + " doesn't have relOps")
    
    def genComment(self, comment):
        o.writeln('\t ' + str(comment))