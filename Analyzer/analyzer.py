import sys
sys.path.insert(0, '../')
from Parser import recordTypes as recTypes
sys.path.insert(0, '../Parser/')
from Symbol import symbolTable
import parser as parser
from classifications import classification
from modes import mode

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
    def findSymbolTable(element):
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
    def findSymbol(lex, c):
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
    def semanticError(inputError):
        sys.exit("Semantic error: " + inputError)
    # --------------------------------------------------------------
    # Semantic Record Helper Functions
    # --------------------------------------------------------------
    def getSemRecType(rec):
        t = None
        if rec['type'] == recTypes.IDENTIFIER:
            r = getSemRecIdRow(rec)
            t = r['type']
        elif rec['type'] == recTypes.LITERAL:
            t = rec['type']
        else:
            semanticError("Record type: " + str(rec['type']) + " does not have a type."
        return t
    
    def getSemRecIdRow(rec):
        lex = rec['lexeme']
        c = rec['classification']
        r = findSymbol(lex, c)
        if r is None:
            semanticError("Identifier: type " + str(c) + " lexeme " + str(lex) + " is not declared in current scope.")
        return r
    
    def generateOffset(table, data):
        nestingLvl = str(table.getNestingLevel())
        memOffset = str(table['offset'])
        nestingLvl = 'D' + nestingLvl
        return memOffset + '(' + nestingLvl + ')'
    # --------------------------------------------------------------
    # VM Assembly Functions
    # --------------------------------------------------------------
    def genHLT():
        o.write("HLT")

    def genRD():
        o.write("RD")

    def genRDF():
        o.write("RDF")

    def genRDS():
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

    def genPUSH():
        o.write("PUSH")

    def genPOP():
        o.write("POP")

    def genNEGS():
        o.write("NEGS")

    def genADDS():
        o.write("ADDS")

    def genSUBS():
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

    def genCASTSI():
        o.write("CASTSI")

    def genCASTSF():
        o.write("CASTSF")

    def label(label):
        o.write(label + ':')
    
    def genLabel():
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        label(label)
        return lblRec
    
    def genSpecLabel(nameRec):
        if nameRec['type'] == recTypes.LABEL:
            label(nameRec['label'])
        else:
            semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genActRec(nameRec, blockType):
        if blockType['type'] == recTypes.BLOCK:
            block = blockType['label']
            table = findSymbolTable(nameRec['label'])
            varCount = table.getVarCount()
            parCount = table.getParCount()
            if block == "program":
                comment(nameRec['label'] + ' start')
                add('SP', '#1', 'SP') # reserve space for old register value
                add('SP', '#' + varCount, 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + 1) + '(SP)'
                move(register, offset)
                sub("SP", "#" + (varCount + 1), register)
                comment("activation end")
            elif block == "procedure" or block == "function":
                comment(nameRec['label'] + ' start')
                add('SP', '#' + varCount, 'SP') # reserve space for variables in program
                register = 'D' + nameRec['nestinglvl']
                offset = '-' + (varCount + parCount + 2) + '(SP)' # slot for both return address and old register value
                move(register, offset)
                sub("SP", "#" + (varCount + parCount + 2), register)
                comment("activation end")
            else:
                semanticError("Block type: " + block + " is not supported")
        else:
            semanticError("Semantic record: " + str(blockType['type']) + " is not supported for recType.BLOCK param")

    def genANDS():
        o.write("ANDS")

    def genORS():
        o.write("ORS")

    def genNOTS():
        o.write("NOTS")

    def genCMPEQS():
        o.write("CMPEQS")

    def genCMPGES():
        o.write("CMPGES")

    def genCMPGTS():
        o.write("CMPGTS")

    def genCMPLES():
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

    def genBR(nameRec):
        if nameRec['type'] == recTypes.LABEL:
            o.writeln("BR " + nameRec['label'])
        else:
            semanticError("Called genBR with type other than LABEL")

    """
    Generate Program Deactivation Record
    """
    def genProgDR(nameRec):
        table = findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + 1) + '(SP)'
        comment('deactivation start')
        move(offset, register)
        sub('SP', '#' + (varCount + 1), 'SP')
        comment(nameRec['label'] + ' end')

    """
    Generate Procedure Deactivation Record
    """
    def genProcDR(nameRec):
        table = findSymbolTable(nameRec['label'])
        varCount = table.getVarCount()
        parCount = table.getParCount()
        register = 'D' + nameRec['nestinglvl']
        offset = '-' + (varCount + parCount + 2) + '(SP)'
        comment('deactivation start')
        move(offset, register)
        sub('SP', '#' + (varCount), 'SP')
        ret()
        comment(nameRec['label'] + ' end')

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
    
    def brUncond(label):
        o.write('BR ' + str(label))
    
    def genAssign(Id, exp, symTable):
        result = genAssignCastType(Id, exp)
        leftRow = getSemRecIdRow(Id)
        if leftRow['classification'] == classification.VARIABLE:
            leftTable = findSymbolTable(leftRow)
            leftOffset = generateOffset(leftTable, leftRow)
            pop(leftOffset)
        elif leftRow['classification'] == classification.FUNCTION:
            funcRow = leftRow
            nestingLevel = symTable['nestingLevel']
            register = 'D' + nameRec['nestingLevel']
            offset = '-1(' + register + ')'
            pop(offset)
            funcRow['returnValue'] = true
        elif leftRow['classification'] == classification.PARAMETER:
            leftTable = findSymbolTable(leftRow)
            row = leftRow
            paramMode = row['mode']
            offset = None
            if paramMode == mode.VALUE:
                offset = generateOffset(leftTable, row)
                pop(offset)
            elif paramMode == mode.VARIABLE:
                offset = '@' + generateOffset(leftTable, row)
                pop(offset)
    
    def genAssignFor(Id, exp):
        idType = getSemRecType(Id)
        if idType == varTypes.INTEGER:
            genAssign(Id, exp, None)
        else:
            semanticError("The 'for' loop's control var must be of type Integer")
    
    def genBranchUncond():
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        brUncond(label)
        return lblRec
    
    def genBranchUncondTo(nameRec):
        if nameRec['type'] == recTypes.LABEL:
            brUncond(nameRec['label'])
        else:
            semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrueTo(nameRec):
        if nameRec['type'] == recTypes.LABEL:
            branchTrue(nameRec['label'])
        else:
            semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchFalseTo(nameRec):
        if nameRec['type'] == recTypes.LABEL:
            branchFalse(nameRec['label'])
        else:
            semanticError("Can't gen label with info of type: " + str(nameRec['type']))
    
    def genBranchTrue():
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        branchTrue(label)
        return lblRec
    
    def genBranchFalse():
        label = parser.getNextLabel()
        lblRec = {'type':recTypes.LABEL, 'label':label}
        branchFalse(label)
        return lblRec
    
    def genComment(comment):
        comment(comment)
        
    def comment(comment):
        o.writeln('\t ' + str(comment))