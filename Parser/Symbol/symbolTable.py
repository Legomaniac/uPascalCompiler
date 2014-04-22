#symbolTable.py
import sys
sys.path.insert(0, '../')
from Parser.classifications import classification

class SymbolTable:
    scopeName = None
    branch = None
    nestingLevel = 0
    tableRows = []
    tableSize = 0
    varCount = 0
    parCount = 0
    
    def __init__(self, scopeName, branch):
        scopeName = scopeName
        branch = branch
        nestingLevel = self.getAndIncrementNestingLevel()
        tableRows = self.getAndIncrementTableSize()
        tableSize = 0
    
    def getVarCount(self):
        return self.varCount
    
    def getParCount(self):
        return self.parCount
    
    def getNestingLevel(self):
        return self.nestingLevel
    
    def getTableSize(self):
        return self.tableSize
    
    def getScopeName(self):
        return self.scopeName
    
    def getBranch(self):
        return self.branch
    
    def getSymbolTable(self):
        return self.tableRows
    
    def getAndIncrementTableSize(self):
        curSize = self.tableSize
        self.tableSize += 1
        return curSize
    
    def getAndIncrementNestingLevel(self):
        curLevel = self.nestingLevel
        self.nestingLevel += 1
        return curLevel
    
    def decrementTableSize(self):
        self.tableSize -= 1
        
    def decrementNestingLevel(self):
        self.nestingLevel -= 1
    
    def contains(self, row):
        for r in self.tableRows:
            if r == row:
                return True
        return False
    
    def insertNewRow(self, row):
        for r in self.tableRows:
            if r['lexeme'] == row['lexeme']:
                sys.exit("Identifier (" + row['lexeme'] + ") has already been declared.")
        self.tableRows.append(row)
        
    def findSymbol(self, lexeme):
        for r in self.tableRows:
            if r['lexeme'] == lexeme:
                return r
        return None
    
    def findSymbol(self, lexeme, c):
        for r in self.tableRows:
            if r['lexeme'] == lexeme and r['classification'] == c:
                return r
        return None
    
    def addDataSymbolsToTable(self, c, ids, attributes):
        att = 0
        for i in ids:
            if len(attributes) == 1:
                attribute = []
                attribute = attribute.append(attributes)
            else:
                attribute = attributes[att]
            lex = i
            if c == classification.VARIABLE:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':self.getAndIncrementTableSize(), 'mode':attribute['mode']}
                self.insertNewRow(row)
                self.varCount += 1
            elif c == classification.PARAMETER:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':self.getAndIncrementTableSize(), 'mode':attribute['mode']}
                self.insertNewRow(row)
                self.varCount += 1
            elif c == classification.RETADDR or c == classification.DISREG:
                row = {'lexeme':lex,'classification':c,'type':attribute['type'],'offset':self.getAndIncrementTableSize(), 'mode':attribute['mode']}
                self.insertNewRow(row)
            else:
                continue
            att += 1

    def addModuleSymbolsToTable(self, c, lex, Type, attributes, branch):
        if c == classification.FUNCTION:
            row = {'lexeme':lex,'classification':c,'type':Type,'attributes':attributes,'branch':branch}
            self.insertNewRow(row)
        elif c == classification.PROCEDURE:
            row = {'lexeme':lex,'classification':c,'attributes':attributes,'branch':branch}
            self.insertNewRow(row)
        else:
            print "Failed to add Module Symbol to Table: " + c
    
    def printTable(self):
        print "SymbolTable Name: " + self.scopeName + ", Nesting Level: " + self.nestingLevel + ", Branch Label: " + self.branch + ", Size: " + self.tableSize
            
        for r in self.tableRows:
            print "Row " + str(r)
