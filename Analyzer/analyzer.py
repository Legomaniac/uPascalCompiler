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
        if writeRec['writeType'] == tokenTypes.MP_WRITE:
            self.genWRTS()
        else:
            self.genWRTLNS()

    def genWRT(self):
        o.write("WRT")

    def genWRTS(self):
        o.write("WRTS")

    def genWRTLN(self):
        o.write("WRTLN")

    def genWRTLNS(self):
        o.write("WRTLNS")

    def genMOV(self):
        o.write("MOV")

    def genNEG(self):
        o.write("NEG")

    def genADD(self):
        o.write("ADD")

    def genSUB(self):
        o.write("SUB")

    def genMUL(self):
        o.write("MUL")

    def genDIV(self):
        o.write("DIV")

    def genMOD(self):
        o.write("MOD")

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

    def genDIVSF(self):
        o.write("DIVSF")

    def genCASTSI(self):
        o.write("CASTSI")

    def genCASTSF(self):
        o.write("CASTSF")

    def label(self, label):
        o.write(label + ':')
    
    def genLabel(self):
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        label(label)
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
                self.comment(nameRec['label'] + ' start')
                o.write("SP #1 SP") # reserve space for old register value
                o.write("SP #" + varCount + " SP") # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + 1) + '(SP)'
                self.move(register, offset)
                self.sub("SP", "#" + (varCount + 1), register)
                self.comment("activation end")
            elif block == "procedure" or block == "function":
                self.comment(nameRec['label'] + ' start')
                self.add('SP', '#' + varCount, 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + parCount + 2) + '(SP)' # slot for both return address and old register value
                self.move(register, offset)
                self.sub("SP", "#" + (varCount + parCount + 2), register)
                self.comment("activation end")
            else:
                self.semanticError("Block type: " + block + " is not supported")
        else:
            self.semanticError("Semantic record: " + str(blockType['type']) + " is not supported for recType.BLOCK param")

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

    """
    Generate Program Deactivation Record
    """
    def genProgDR(self, nameRec):
        table = self.findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + 1) + '(SP)'
        self.comment('deactivation start')
        self.move(offset, register)
        self.sub('SP', '#' + (varCount + 1), 'SP')
        self.comment(nameRec['label'] + ' end')

    """
    Generate Procedure Deactivation Record
    """
    def genProcDR(self, nameRec):
        table = self.findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        parCount = table.getParCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + parCount + 2) + '(SP)'
        self.comment('deactivation start')
        self.move(offset, register)
        self.sub('SP', '#' + (varCount), 'SP')
        self.ret()
        self.comment(nameRec['label'] + ' end')

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

    def genCALL(self):
        o.write("CALL")

    def genRET(self):
        o.write("RET")

    def genPRTS(self):
        o.write("PRTS")

    def genPRTR(self):
        o.write("PRTR")
    
    def brUncond(self, label):
        o.write('BR ' + str(label))

    def genCast(self, left, right):
        leftType = self.getSemRecType(left)
        rightType = self.getSemRecType(right)
        arrayRec = []
        if leftType == rightType:
            arrayRec[1] = left
            arrayRec[2] = right
        elif leftType == varTypes.INTEGER and rightType == varTypes.FLOAT:
            self.genSUB()
            #Fix dis
            self.genCASTSF()
            self.genADD()
            #Fix dis
            arrayRec[0] = {'type':recTypes.LITERAL, 'varType':varTypes.MP_FLOAT}
            arrayRec[1] = right
        elif leftType == varTypes.FLOAT and rightType == varTypes.INTEGER:
            self.genCASTSI()
            arrayRec[0] = left
            arrayRec[1] = {'type':recTypes.LITERAL, 'varType':varTypes.MP_FLOAT}
        else:
            self.semanticError("Invalid casting from " + rightType + " to " + leftType)
            return None
        return arrayRec

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
    
    def genAssign(self, Id, exp, symTable):
        self.genAssignCast(Id, exp)
        leftRow = self.getSemRecIdRow(Id)
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
    
    def genAssignFor(self, Id, exp):
        idType = self.getSemRecType(Id)
        if idType == varTypes.INTEGER:
            self.genAssign(Id, exp, None)
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

    
    def genComment(self, inComment):
        self.comment(inComment)
        
    def comment(comment):
        o.writeln('\t ' + str(comment))