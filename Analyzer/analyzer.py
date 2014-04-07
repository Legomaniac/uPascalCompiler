import sys
from Parser.recordTypes import recTypes

o = open('output.up', 'w')

def semanticError(inputError):
    sys.exit("Semantic error: " + inputError)

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

def genLabel():
    o.write("L")

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

def genBR(inRec):
    if inRec['type'] == recTypes.LABEL:
        o.write("BR " + inRec['branch'])
    else:
        semanticError("Called genBR with type other than LABEL")

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