#symbolTable.py
import sys

class SymbolTable:
    scopeName = None
    branch = None
    nestingLevel = 0
    tableRows = []
    tableSize = 0
    variableCount = 0
    parameterCount = 0
    
    def __init__(self, scopeName, branch):
        global nestingLevel, tableRows, tableSize, scopeName, branch
        scopeName = scopeName
        branch = branch
        nestingLevel = getAndIncrementNestingLevel()
        tableRows = getAndIncrementTableSize()
        tableSize = 0
    
    def getNestingLevel():
        return nestingLevel
    
    def getTableSize():
        return tableSize
    
    def getScopeName():
        return scopeName
    
    def getBranch():
        return branch
    
    def getSymbolTable():
        return tableRows
    
    def getAndIncrementTableSize():
        curSize = tableSize
        tableSize += 1
        return curSize
    
    def getAndIncrementNestingLevel():
        curLevel = nestingLevel
        nestingLevel += 1
        return curLevel
    
    def decrementTableSize():
        tableSize -= 1
        
    def decrementNestingLevel():
        nestingLevel -= 1
    
    def contains(row):
        for r in tableRows:
            if r == row:
                return true
        return false
    
    def insertNewRow(row):
        for r in tableRows:
            if r.lexeme == row.lexeme:
                sys.exit("Identifier (" + row.lexeme + ") has already been declared.")
        tableRows.append(row)
        
    def findSymbol(lexeme):
        for r in tableRows:
            if r.lexeme == lexeme:
                return r
        return null
    
    def addDataSymbolsToTable(classification, ids, attributes):
        if len(attributes) == 1:
            attribute = attributes
            attributes = []
            for i in ids:
                attributes.append(attribute)
        for i in ids:
            lex = ids[i]
            attribute = attributes[i]
            if classification == "VARIABLE":
                row = [lex, classification, attribute.type, getAndIncrementTableSize(), attribute.mode]
                insertNewRow(row)
                variableCount += 1
                break
            elif classification == "PARAMETER":
                row = [lex, classification, attribute.type, getAndIncrementTableSize(), attribute.mode]
                insertNewRow(row)
                parameterCount += 1
                break
            elif classification == "RETADDR" or classification == "DISREG":
                row = [lex, classification, attribute.type, getAndIncrementTableSize(), attribute.mode]
                insertNewRow(row)
                break
            else:
                break      

    def addModuleSymbolsToTable(classification, lexeme, Type, attributes, branch):
        if classification == "FUNCTION":
            row = [lexeme, classification, Type, attributes, branch]
            insertNewRow(row)
        elif classification == "PROCEDURE":
            row = [lexeme, classification, attributes, branch]
            insertNewRow(row)
        else:
            print "Failed to add Module Symbol to Table: " + classification
            pass
    
    def printTable():
        print "SymbolTable Name: " + scopeName + ", Nesting Level: " + nestingLevel + ", Branch Label: " +
            branch + ", Size: " + tableSize
            
        for r in tableRows:
            print "Row " + str(r)
