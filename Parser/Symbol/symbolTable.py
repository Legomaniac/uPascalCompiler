#symbolTable.py
import sys
sys.path.insert(0, '../')
from classifications import classification

class SymbolTable:
    scopeName = None
    branch = None
    nestingLevel = 0
    tableRows = []
    tableSize = 0
    varCount = 0
    parCount = 0
    
    def __init__(self, scopeName, branch):
        global nestingLevel, tableRows, tableSize, scopeName, branch, varCount, parCount
        scopeName = scopeName
        branch = branch
        nestingLevel = getAndIncrementNestingLevel()
        tableRows = getAndIncrementTableSize()
        tableSize = 0
    
    def getVarCount():
        return varCount
    
    def getParCount():
        return parCount
    
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
            if r['lexeme'] == row['lexeme']:
                sys.exit("Identifier (" + row['lexeme'] + ") has already been declared.")
        tableRows.append(row)
        
    def findSymbol(lexeme):
        for r in tableRows:
            if r['lexeme'] == lexeme:
                return r
        return None
    
    def findSymbol(lexeme, c):
        for r in tableRows:
            if r['lexeme'] == lexeme and r['classification'] == c:
                return r
        return None
    
    def addDataSymbolsToTable(c, ids, attributes):
        if len(attributes) == 1:
            attribute = attributes
            attributes = []
            for i in ids:
                attributes.append(attribute)
        for i in ids:
            lex = ids[i]
            attribute = attributes[i]
            if c == classification.VARIABLE:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':getAndIncrementTableSize(), 'mode':attribute['mode']}
                insertNewRow(row)
                varCount += 1
            elif c == classification.PARAMETER:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':getAndIncrementTableSize(), 'mode':attribute['mode']}
                insertNewRow(row)
                parCount += 1
            elif c == classification.RETADDR or c == classification.DISREG:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':getAndIncrementTableSize(), 'mode':attribute['mode']}
                insertNewRow(row)
            else:
                continue      

    def addModuleSymbolsToTable(c, lex, Type, attributes, branch):
        if c == classification.FUNCTION:
            row = {'lexeme':lex,'classification':c,'type':Type,'attributes':attributes,'branch':branch}
            insertNewRow(row)
        elif c == classification.PROCEDURE:
            row = {'lexeme':lex,'classification':c,'attributes':attributes,'branch':branch}
            insertNewRow(row)
        else:
            print "Failed to add Module Symbol to Table: " + c
    
    def printTable():
        print "SymbolTable Name: " + scopeName + ", Nesting Level: " + nestingLevel + ", Branch Label: " +
            branch + ", Size: " + tableSize
            
        for r in tableRows:
            print "Row " + str(r)
