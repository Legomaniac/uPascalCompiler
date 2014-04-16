import sys
sys.path.insert(0, '../')
from Parser import recordTypes as recTypes
from tokenTypes import types as tokenTypes
sys.path.insert(0, '../Parser/')
from Parser.Symbol import symbolTable
import parser as parser
from Parser.classifications import classification
from Parser.modes import mode

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
        memOffset = str(table['offset'])
        nestingLvl = 'D' + nestingLvl
        return memOffset + '(' + nestingLvl + ')'
    # --------------------------------------------------------------
    # VM Assembly Functions
    # --------------------------------------------------------------
    def genHLT(self):
        o.write("HLT")

    def genRD(self):
        o.write("RD")

    def genRDF(self):
        o.write("RDF")

    def genRDS(self):
        o.write("RDS")

    def genWRT():
        o.write("WRT")

    def genWRTS():
        o.write("WRTS")

    def genWRTLN():
        o.write("WRTLN")

    def genWRTLNS():
        o.write("WRTLNS")

    def genMOV():
        o.write("MOV")

    def genNEG():
        o.write("NEG")

    def genADD():
        o.write("ADD")

    def genSUB():
        o.write("SUB")

    def genMUL():
        o.write("MUL")

    def genDIV():
        o.write("DIV")

    def genMOD():
        o.write("MOD")

    def genNEGF():
        o.write("NEGF")

    def genADDF():
        o.write("ADDF")

    def genSUBF():
        o.write("SUBF")

    def genMULF():
        o.write("MULF")

    def genDIVF():
        o.write("DIVF")

    def genPUSH(self, location):
        o.write("PUSH " + str(location))

    def genPOP(self, location):
        o.write("POP " + str(location))

    def genNEGS():
        o.write("NEGS")

    def genADDS(self):
        o.write("ADDS")

    def genSUBS(self):
        o.write("SUBS")

    def genMULS():
        o.write("MULS")

    def genDIVS():
        o.write("DIVS")

    def genMODS():
        o.write("MODS")

    def genNEGSF():
        o.write("NEGSF")

    def genADDSF():
        o.write("ADDSF")

    def genSUBSF():
        o.write("SUBSF")

    def genMULSF():
        o.write("MULSF")

    def genDIVSF():
        o.write("DIVSF")

    def genCASTSI(self):
        o.write("CASTSI")

    def genCASTSF():
        o.write("CASTSF")

    def label(label):
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

    def genANDS():
        o.write("ANDS")

    def genORS():
        o.write("ORS")

    def genNOTS():
        o.write("NOTS")

    def genCMPEQS():
        o.write("CMPEQS")

    def genCMPGES(self):
        o.write("CMPGES")

    def genCMPGTS():
        o.write("CMPGTS")

    def genCMPLES(self):
        o.write("CMPLES")

    def genCMPLTS():
        o.write("CMPLTS")

    def genCMPNES():
        o.write("CMPNES")

    def genCMPEQSF():
        o.write("CMPEQSF")

    def genCMPGESF():
        o.write("CMPGESF")

    def genCMPGTSF():
        o.write("CMPGTSF")

    def genCMPLESF():
        o.write("CMPLESF")

    def genCMPLTSF():
        o.write("CMPLTSF")

    def genCMPNESF():
        o.write("CMPNESF")

    def genBRTS():
        o.write("BRTS")

    def genBRFS():
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

    def genBEQ():
        o.write("BEQ")

    def genBGE():
        o.write("BGE")

    def genBGT():
        o.write("BGT")

    def genBLE():
        o.write("BLE")

    def genBLT():
        o.write("BLT")

    def genBNE():
        o.write("BNE")

    def genBEQF():
        o.write("BEQF")

    def genBGEF():
        o.write("BGEF")

    def genBFTF():
        o.write("BGTF")

    def genBLEF():
        o.write("BLEF")

    def genBLTF():
        o.write("BLTF")

    def genBNEF():
        o.write("BNEF")

    def genCALL():
        o.write("CALL")

    def genRET():
        o.write("RET")

    def genPRTS():
        o.write("PRTS")

    def genPRTR():
        o.write("PRTR")
    
    def brUncond(self, label):
        o.write('BR ' + str(label))
    
    def genForController(self, controlRec, forDir):
        inc = false
        if forDir['type'] == recTypes.FOR_DIRECTION:
            if forDir['tokenType'] == tokenTypes.MP_TO:
                inc = true
            elif forDir['tokenType'] == tokenTypes.MP_DOWNTO:
                inc = true
            else:
                self.semanticError("Invalid FOR_DIRECTION: " + forDir['tokenType'])
        else:
            self.semanticError("Cannot use non-FOR_DIRECTION rec type: " + forDir['type'])
        if controlRec['type'] == recTypes.IDENTIFIER:
            if controlRec['classification'] == classification.VARIABLE:
                row = self.findSymbol(controlRec['controlId'])
                memLocation = self.generateOffset(self.findSymbolTable(row), row)
                if inc:
                    genPUSH(memLocation)
                    genPUSH('#1')
                    genADDS()
                    genPOP(memLocation)
                else:
                    genPUSH(memLocation)
                    genPUSH('#1')
                    genSUBS()
                    genPOP(memLocation)
            else:
                self.semanticError("Cannot use non-var as control var")
        else:
            self.semanticError("Cannot use non-identifier as contorl var")
                    
    
    def genForComp(self, forDir):
        if forDir['type'] == recTypes.FOR_DIRECTION:
            if forDir['tokenType'] == tokenTypes.MP_TO:
                genCMPLES()
            elif forDir['tokenType'] == tokenTypes.MP_DOWNTO:
                genCMPGES()
            else:
                self.semanticError("Invalid FOR_DIRECTION: " + forDir['tokenType'])
        else:
            self.semanticError("Cannot use non-FOR_DIRECTION rec type: " + forDir['type'])
    
    def genAssignCast(self, leftRec, rightRec):
        leftType = getSemRecType(leftRec)
        rightType = getSemRecType(rightRec)
        returnRec = None
        if leftType == rightType:
            returnRec = rightRec
        elif leftType == varTypes.INTEGER and rightType == varTypes.FLOAT:
            genCASTSI()
        elif leftType == varTypes.FLOAT and rightType == varTypes.INTEGER:
            genCASTSF()
        else:
            self.semanticError("Invalid cast from " + rightType + " to " + leftType)
    
    def genPushVar(self, varRec):
        if varRec['type'] == recTypes.IDENTIFIER:
            if varRec['classification'] == classification.VARIABLE:
                row = self.findSymbol(varRec['controlId'])
                memLocation = self.generateOffset(self.findSymbolTable(row),row)
                genPUSH(memLocation)
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
    
    def genComment(self, inComment):
        self.comment(inComment)
        
    def comment(comment):
        o.writeln('\t ' + str(comment))