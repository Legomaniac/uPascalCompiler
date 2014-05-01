import sys
import datetime
sys.path.insert(0, '../')
from tokenTypes import types as tokenTypes
from label import Label
sys.path.insert(0, '../Parser/')
import parser as parser
from Parser.classifications import classification
from Parser.modes import mode
from Parser.types import varTypes
from Parser.recordTypes import recTypes

class Analyzer:

    outfile = "Output/output-" + datetime.datetime.now().strftime("%m%d%y-%H%M") + ".up"
    o = open(outfile, 'w')
    symbolTables = None
    
    def __init__(self, tables):
        global symbolTables, label
        label = Label()
        if self.o.closed:
            print "ERROR: Output file not opened properly..."
        symbolTables = tables
        
    # --------------------------------------------------------------
    # Symbol Tables Functions
    # --------------------------------------------------------------
    """
    Can pass either the symbol table name or symbol in the table
    """
    def findSymbolTable(self, element):
        tables = symbolTables[::-1]
        if tables is not None:
            for i in range(len(tables)):
                st = tables[i]
                if st.contains(element):
                    return st
                elif st.getScopeName() == element:
                    return st
                else:
                    continue
        return None
    """
    Calls one of two findSymbol functions on the table depending on
    if the classification is passed or not... calls symbolTable function
    """
    def findSymbol(self, lex, c):
        tables = symbolTables[::-1]
        for i in range(len(tables)):
            st = tables[i]
            if c is not None:
                row = st.findSymbol(lex, c)
                if row is not None:
                    return row
            else:
                row = st.findSymbol(lex, None)
                if row is not None:
                    return row
        return None
    """
    Updates the symbolTables variable from the parser, called from parser
    """
    def updateTables(self, tables):
        symbolTables = tables
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
            t = rec['varType']
        else:
            self.semanticError("Record type: " + str(rec['type']) + " does not have a type.")
        return t
    
    def getSemRecIdRow(self, rec):
        if "lexeme" in rec:
            lex = rec['lexeme']
        else:
            lex = rec['controlId']
        c = rec['classification']
        r = self.findSymbol(lex, c)
        if r is None:
            self.semanticError("Identifier: type " + str(c) + " lexeme " + str(lex) + " is not declared in current scope.")
        return r
    
    def generateOffset(self, table, data):
        nestingLvl = str(table.getNestingLevel())
        memOffset = str(data['offset'])
        nestingLvl = 'D' + nestingLvl
        return str(memOffset + '(' + nestingLvl + ')')
    # --------------------------------------------------------------
    # VM Assembly Functions
    # --------------------------------------------------------------
    def genHLT(self):
        self.o.write("HLT" + '\n')
    
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
        self.o.write("RD " + offset + '\n')
    
    def genRDF(self, offset):
        self.o.write("RDF " + offset + '\n')
    
    def genRDS(self, offset):
        self.o.write("RDS " + offset + '\n')
    
    def genWrite(self, writeRec, expRec):
        if writeRec['tokenType'] == tokenTypes.MP_WRITE:
            self.genWRTS()
        else:
            self.genWRTLNS()
    
    def genWRTS(self):
        self.o.write("WRTS" + '\n')
    
    def genWRTLN(self):
        self.o.write("WRTLN" + '\n')
    
    def genWRTLNS(self):
        self.o.write("WRTLNS" + '\n')
    
    def genMOV(self, src, dst):
        self.o.write("MOV " + str(src) + " " + str(dst) + '\n')
    
    def genADD(self, src1, src2, dst):
        self.o.write("ADD " + str(src1) + " " + str(src2) + " " + str(dst) + '\n')
    
    def genSUB(self, src1, src2, dst):
        self.o.write("SUB " + str(src1) + " " + str(src2) + " " + str(dst) + '\n')
    
    def genNEGF(self):
        self.o.write("NEGF" + '\n')
    
    def genADDF(self):
        self.o.write("ADDF" + '\n')
    
    def genSUBF(self):
        self.o.write("SUBF" + '\n')
    
    def genMULF(self):
        self.o.write("MULF" + '\n')
    
    def genDIVF(self):
        self.o.write("DIVF" + '\n')
    
    def genPUSH(self, location):
        self.o.write("PUSH " + str(location) + '\n')
    
    def genPOP(self, location):
        self.o.write("POP " + str(location) + '\n')
    
    def genNEGS(self):
        self.o.write("NEGS" + '\n')
    
    def genADDS(self):
        self.o.write("ADDS" + '\n')
    
    def genSUBS(self):
        self.o.write("SUBS" + '\n')
    
    def genMULS(self):
        self.o.write("MULS" + '\n')
    
    def genDIVS(self):
        self.o.write("DIVS" + '\n')
    
    def genMODS(self):
        self.o.write("MODS" + '\n')
    
    def genNEGSF(self):
        self.o.write("NEGSF" + '\n')
    
    def genADDSF(self):
        self.o.write("ADDSF" + '\n')
    
    def genSUBSF(self):
        self.o.write("SUBSF" + '\n')
    
    def genMULSF(self):
        self.o.write("MULSF" + '\n')
    
    def genMODSF(self):
        self.o.write("MODSF" + '\n')
    
    def genDIVSF(self):
        self.o.write("DIVSF" + '\n')
    
    def genCASTSI(self):
        self.o.write("CASTSI" + '\n')
    
    def genCASTSF(self):
        self.o.write("CASTSF" + '\n')
    
    def genANDS(self):
        self.o.write("ANDS" + '\n')
    
    def genORS(self):
        self.o.write("ORS" + '\n')
    
    def genNOTS(self):
        self.o.write("NOTS" + '\n')
    
    def genCMPEQS(self):
        self.o.write("CMPEQS" + '\n')
    
    def genCMPGES(self):
        self.o.write("CMPGES" + '\n')
    
    def genCMPGTS(self):
        self.o.write("CMPGTS" + '\n')
    
    def genCMPLES(self):
        self.o.write("CMPLES" + '\n')
    
    def genCMPLTS(self):
        self.o.write("CMPLTS" + '\n')
    
    def genCMPNES(self):
        self.o.write("CMPNES" + '\n')
    
    def genCMPEQSF(self):
        self.o.write("CMPEQSF" + '\n')
    
    def genCMPGESF(self):
        self.o.write("CMPGESF" + '\n')
    
    def genCMPGTSF(self):
        self.o.write("CMPGTSF" + '\n')
    
    def genCMPLESF(self):
        self.o.write("CMPLESF" + '\n')
    
    def genCMPLTSF(self):
        self.o.write("CMPLTSF" + '\n')
    
    def genCMPNESF(self):
        self.o.write("CMPNESF" + '\n')
    
    def genBRTS(self, lbl):
        self.o.write("BRTS " + str(lbl) + '\n')
    
    def genBRFS(self, lbl):
        self.o.write("BRFS " + str(lbl) + '\n')
    
    def genBR(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.o.write("BR " + nameRec['label'] + '\n')
        else:
            self.semanticError("Called genBR with type other than LABEL")
    
    def label(self, lbl):
        self.o.write(lbl + ':' + '\n')
    
    def genLabel(self):
        lbl = label.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':lbl}
        self.label(lbl)
        return lblRec
    
    def genSpecLabel(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.label(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genActRec(self, nameRec, blockType):
        if blockType['type'] == recTypes.BLOCK:
            block = blockType['label']
            table = self.findSymbolTable(nameRec['scope'])
            varCount = table.getVarCount()
            parCount = table.getParCount()
            if block == "program":
                self.genComment(nameRec['scope'] + ' start')
                self.genADD('SP', '#1', 'SP') # reserve space for old register value
                self.genADD('SP', '#' + str(varCount), 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + str(varCount + 1) + '(SP)'
                self.genMOV(register, offset)
                self.genSUB("SP", "#" + str(varCount + 1), register)
                self.genComment("activation end")
            elif block == "procedure" or block == "function":
                self.genComment(nameRec['scope'] + ' start')
                self.genADD('SP', '#' + str(varCount), 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + str(varCount + parCount + 2) + '(SP)' # slot for both return address and old register value
                self.genMOV(register, offset)
                self.genSUB("SP", "#" + str(varCount + parCount + 2), register)
                self.genComment("activation end")
            else:
                self.semanticError("Block type: " + block + " is not supported")
        else:
            self.semanticError("Semantic record: " + str(blockType['type']) + " is not supported for recType.BLOCK param")
    
    """
    Generate Program Deactivation Record
    """
    def genProgDR(self, nameRec):
        table = self.findSymbolTable(nameRec['scope'])
        varCount = table.getVarCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + str(varCount + 1) + '(SP)'
        self.genComment('deactivation start')
        self.genMOV(offset, register)
        self.genSUB('SP', '#' + str(varCount + 1), 'SP')
        self.genComment(nameRec['scope'] + ' end')
    
    """
    Generate Procedure Deactivation Record
    """
    def genProcDR(self, nameRec):
        table = self.findSymbolTable(nameRec['scope'])
        varCount = table.getVarCount()
        parCount = table.getParCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + str(varCount + parCount + 2) + '(SP)'
        self.genComment('deactivation start')
        self.genMOV(offset, register)
        self.genSUB('SP', '#' + str(varCount), 'SP')
        self.genRET()
        self.genComment(nameRec['scope'] + ' end')
    
    """
    Generate Function(Procedure) Deactivation Record
    """
    def genFuncDR(self, nameRec):
        self.genProcDR(nameRec)
    
    """
    Generate Procedure Call
    """
    def genProcCall(self, procRec):
        row = self.getSemRecIdRow(procRec)
        lbl = row['branch']['label']
        self.genCALL(lbl)
        paramSize = len(row['attributes'])
        self.genSUB('SP', '#' + str(paramSize + 1), 'SP')
    
    """
    Generate Function Call
    """
    def genFuncCall(self, funcRec):
        row = self.getSemRecIdRow(funcRec)
        lbl = row['branch']['label']
        self.genCALL(lbl)
        paramSize = len(row['attributes'])
        self.genSUB('SP', '#' + str(paramSize + 1), 'SP')
    
    def genBEQ(self):
        self.o.write("BEQ" + '\n')
    
    def genBGE(self):
        self.o.write("BGE" + '\n')
    
    def genBGT(self):
        self.o.write("BGT" + '\n')
    
    def genBLE(self):
        self.o.write("BLE" + '\n')
    
    def genBLT(self):
        self.o.write("BLT" + '\n')
    
    def genBNE(self):
        self.o.write("BNE" + '\n')
    
    def genBEQF(self):
        self.o.write("BEQF" + '\n')
    
    def genBGEF(self):
        self.o.write("BGEF" + '\n')
    
    def genBFTF(self):
        self.o.write("BGTF" + '\n')
    
    def genBLEF(self):
        self.o.write("BLEF" + '\n')
    
    def genBLTF(self):
        self.o.write("BLTF" + '\n')
    
    def genBNEF(self):
        self.o.write("BNEF" + '\n')
    
    def genCALL(self, lbl):
        self.o.write("CALL " + str(lbl) + '\n')
    
    def genRET(self):
        self.o.write("RET" + '\n')
    
    def genPRTS(self):
        self.o.write("PRTS" + '\n')
    
    def genPRTR(self):
        self.o.write("PRTR" + '\n')
    
    def genSPslot(self):
        self.genADD('SP', '#1', 'SP')
    
    def brUncond(self, lbl):
        self.o.write('BR ' + str(lbl) + '\n')
    
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
        return {'type':recTypes.LITERAL, 'varType':rowData['type']}
    
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
            row = self.findSymbol(factor['lexeme'], classification.VARIABLE)
            actualParamType = row['type']
            actualParamMode = row['mode']
            varClass = True
        elif factor['classification'] == classification.PARAMETER:
            row = self.findSymbol(factor['lexeme'], classification.PARAMETER)
            actualParamType = row['type']
            actualParamMode = row['mode']
            varClass = False
        if actualParamType is not None and actualParamMode is not None:
            if formalParamMode == mode.VALUE:
                if actualParamMode == mode.VALUE:
                    offset = self.generateOffset(table, rowData)
                    returnVal = {'type':recTypes.LITERAL, 'varType':rowData['type']}
                    self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                    self.genPUSH(offset)
                elif actualParamMode == mode.VARIABLE:
                    if varClass:
                        offset = self.generateOffset(table, rowData)
                        returnVal = {'type':recTypes.LITERAL, 'varType':rowData['type']}
                        self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                        self.genPUSH(offset)
                    else:
                        offset = '@' + self.generateOffset(table, rowData)
                        returnVal = {'type':recTypes.LITERAL, 'varType':rowData['type']}
                        self.genComment("push class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + offset)
                        self.genPUSH(offset)
            elif formalParamMode == mode.VARIABLE:
                if actualParamMode == mode.VALUE:
                    self.semanticError("Cannot send 'mode: VALUE, actual parameter': " + factor['lexeme'] + " into 'mode: VARIABLE, formal param' procedure/function")
                elif actualParamMode == mode.VARIABLE:
                    if formalParamType == actualParamType:
                        if varClass:
                            register = 'D' + str(table.getNestingLevel())
                            offset = rowData['offset']
                            returnVal = factor
                            self.genComment("push address class: " + rowData['classification'] + ", lexeme: " + rowData['lexeme'] + ", type: " + rowData['type'] + ", offset: " + str(offset))
                            self.genPUSH(register)
                            self.genPUSH('#' + str(offset))
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
            arrayRec.append(left)
            castL = True
        elif leftType == varTypes.INTEGER:
            self.genComment("start cast left to float")
            self.genSUB('SP', '#1', 'SP') # move to the left variable on stack
            self.genCASTSF()
            self.genADD('SP', '#1', 'SP') # move back
            self.genComment("end cast left to float")
            arrayRec.append({'type':recTypes.LITERAL, 'varType':varTypes.FLOAT})
            castL = True
        else:
            castL = False
        if rightType == varTypes.FLOAT:
            arrayRec.append(left)
            castR = True
        elif rightType == varTypes.INTEGER:
            self.genCASTSF()
            arrayRec.append({'type':recTypes.LITERAL, 'varType':varTypes.FLOAT})
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
            arrayRec.append(left)
            arrayRec.append(right)
        elif leftType == varTypes.INTEGER and rightType == varTypes.FLOAT:
            self.genComment("start cast left to float")
            self.genSUB('SP', '#1', 'SP') # move to the left variable on stack
            self.genCASTSF()
            self.genADD('SP', '#1', 'SP') # move back
            self.genComment("end cast left to float")
            arrayRec.append({'type':recTypes.LITERAL, 'varType':varTypes.FLOAT})
            arrayRec.append(right)
        elif leftType == varTypes.FLOAT and rightType == varTypes.INTEGER:
            self.genCASTSF()
            arrayRec.append(left)
            arrayRec.append({'type':recTypes.LITERAL, 'varType':varTypes.FLOAT})
        else:
            self.semanticError("Invalid casting from " + rightType + " to " + leftType)
            return None
        return arrayRec
    
    def checkTypesInt(self, left, right):
        leftType = self.getSemRecType(left)
        rightType = self.getSemRecType(right)
        if leftType != varTypes.INTEGER or rightType != varTypes.INTEGER:
            self.semanticError("The div operator only works on integer operand. Left operand: " + leftType + ", right operand: " + rightType)
    
    def genMulOp(self, left, mulOp, right):
        results = []
        op = mulOp['tokenType']
        if op == tokenTypes.MP_DIV:
            self.checkTypesInt(left, right)
            self.genDIVS()
            resultType = varTypes.INTEGER
        elif op == tokenTypes.MP_FLOAT_DIVIDE:
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
        return {'type':recTypes.LITERAL, 'varType':resultType}
    
    def genAddOp(self, left, addOp, right):
        results = self.genCast(left, right)
        resultType = self.getSemRecType(results[0])
        op = addOp['tokenType']
        if resultType == varTypes.INTEGER:
            if op == tokenTypes.MP_MINUS:
                self.genSUBS()
            elif op == tokenTypes.MP_PLUS:
                self.genADDS()
            else:
                self.semanticError(op + " is not an addOp for type: " + resultType)
        elif resultType == varTypes.FLOAT:
            if op == tokenTypes.MP_MINUS:
                self.genSUBSF()
            elif op == tokenTypes.MP_PLUS:
                self.genADDSF()
            else:
                self.semanticError(op + " is not an addOp for type: " + resultType)
        elif resultType == varTypes.BOOLEAN:
            if op == tokenTypes.MP_OR:
                self.genORS()
            else:
                self.semanticError(op + " is not an addOp for type: " + resultType)
        else:
            self.semanticError(resultType + " does not have adding operation")
        return {'type':recTypes.LITERAL, 'varType':resultType}
    
    def genOptSimNeg(self, opSign, term):
        if opSign is not None and term is not None:
            termType = self.getSemRecType(term)
            op = opSign['tokenType']
            if termType == varTypes.INTEGER:
                if op == tokenTypes.MP_MINUS:
                    self.genNEGS()
                elif op == tokenTypes.MP_PLUS:
                    # do not throw sem error, but do nothing
                    pass
                else:
                    self.semanticError(opSign + " is not a neg op for type: " + termType)
            elif termType == varTypes.FLOAT:
                if op == tokenTypes.MP_MINUS:
                    self.genNEGSF()
                elif op == tokenTypes.MP_PLUS:
                    # do not throw sem error, but do nothing
                    pass
                else:
                    self.semanticError(opSign + " is not a neg op for type: " + termType)
            else:
                self.semanticError(termType + " does not have a neg operation")
    
    def genPushLit(self, lit, lex):
        litType = lit['varType']
        self.genComment("push lexeme: " + lex + ", type: " + str(litType))
        if litType == varTypes.STRING:
            self.genPUSH("#\"" + str(lex) + "\"")
        elif litType == varTypes.BOOLEAN:
            if lex == "true":
                self.genPUSH('#1')
            else:
                self.genPUSH('#0')
        elif litType == varTypes.INTEGER:
            self.genPUSH('#' + str(lex))
        elif litType == varTypes.FLOAT:
            if lex.find("e") > -1 and lex.find(".") == -1:
                split = lex.find("e") * -1
                start = str(lex[0:split])
                split = split * -1
                end = str(lex[split:])
                lex = start + ".0" + end
            self.genPUSH('#' + str(lex))
        else:
            self.semanticError(lex + " of type: " + str(litType) + " cannot be pushed onto the stack")
    
    def genNotBool(self, factor):
        factorType = self.getSemRecType(factor)
        if factorType == varTypes.BOOLEAN:
            self.genNOTS()
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
                row = self.findSymbol(controlRec['controlId'], None)
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
                row = self.findSymbol(varRec['controlId'], None)
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
            self.genPOP(leftOffset)
        elif leftRow['classification'] == classification.FUNCTION:
            funcRow = leftRow
            nestingLevel = symTable['nestinglvl']
            register = 'D' + nestingLevel
            offset = '-1(' + register + ')'
            self.genPOP(offset)
            funcRow['returnValue'] = True
        elif leftRow['classification'] == classification.PARAMETER:
            leftTable = self.findSymbolTable(leftRow)
            row = leftRow
            paramMode = row['mode']
            offset = None
            if paramMode == mode.VALUE:
                offset = self.generateOffset(leftTable, row)
                self.genPOP(offset)
            elif paramMode == mode.VARIABLE:
                offset = '@' + self.generateOffset(leftTable, row)
                self.genPOP(offset)
    
    def genAssignFor(self, idRec, exp):
        idType = self.getSemRecType(idRec)
        if idType == varTypes.INTEGER:
            self.genAssign(idRec, exp, None)
        else:
            self.semanticError("The 'for' loop's control var must be of type Integer")
    
    def genBranchUncond(self):
        lbl = label.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':lbl}
        self.brUncond(lbl)
        return lblRec
    
    def genBranchUncondTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.brUncond(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrueTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.genBRTS(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchFalseTo(self, nameRec):
        if nameRec['type'] == recTypes.LABEL:
            self.genBRFS(nameRec['label'])
        else:
            self.semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrue(self):
        lbl = label.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':lbl}
        self.genBRTS(lbl)
        return lblRec
    
    def genBranchFalse(self):
        lbl = label.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':lbl}
        self.genBRFS(lbl)
        return lblRec
    
    def genOptRelPart(self, left, op, right):
        if left is not None and op is not None and right is not None:
            results = self.genCast(left, right)
            resultType = self.getSemRecType(results[0])
            relOp = op['token']
            if resultType == varTypes.INTEGER:
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
                    self.genCMPEQS()
                else:
                    self.semanticError(relOp + " isn't an operator for " + resultType)
            elif resultType == varTypes.FLOAT:
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
                    self.genCMPEQSF()
                else:
                    self.semanticError(relOp + " isn't an operator for " + resultType)
            else:
                self.semanticError(resultType + " doesn't have relOps")
    
    def genComment(self, comment):
        print "\t " + str(comment) + "\n"