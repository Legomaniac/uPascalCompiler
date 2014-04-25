##FSA plugin with all implemented FSA methods
from token import *
from tokens import *
from tokenTypes import *
import scanner as scanner

class ScanError(Exception): pass

"""FSA for Identifiers"""
def IdentifierFSA(currentChar):
    state = 1
    lex = ""
    current = currentChar
    while state != 4:
        if not scanner.hasNextChar() and state == 2:
            state = 4
        else:
            if state == 1:
                if current['lexeme'] in string.letters:
                    state = 2
                    lex += current['lexeme']
                elif current['lexeme'] == "_":
                    state = 3
                    lex += current['lexeme']
                else:
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'] -1)
            elif state == 2:
                if scanner.hasNextChar():
                    current = scanner.getNextChar()
                    if current['lexeme'] in string.letters:
                        state = 2
                        lex += current['lexeme']
                    elif current['lexeme'] == "_":
                        state = 3
                        lex += current['lexeme']
                    else:
                        state = 4
                else:
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'] -1)
            elif state == 3:
                if scanner.hasNextChar():
                    current = scanner.getNextChar()
                    if current['lexeme'] in string.letters:
                        state = 2
                        lex += current['lexeme']
                    else:
                        return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'] -1)
                else:
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'] -1)
            else:
                continue
    if current['lexeme'] in ReservedWords:
        return Token(ReservedWords[current['lexeme']], lex, current['lineIndex'], current['colIndex'] - len(lex))
    else:
        return Token(types.MP_IDENTIFIER, lex, current['lineIndex'], current['colIndex'] - len(lex))

def LiteralFSA(currentChar):
    state = 1
    lex = ""
    current = currentChar
    startingLine = current['lineIndex']
    startingCol = current['colIndex']
    while state != 4:
        if not scanner.hasNextChar() and state == 3:
            state = 4
        else:
            if state == 1:
                if current['lexeme'] == "\'":
                    state = 2
                else:
                    current = scanner.getNextChar()
            elif state == 2:
                if scanner.hasNextChar():
                    current = scanner.getNextChar()
                    if current['lexeme'] != "\'" and scanner.hasNextChar():
                        state = 2
                        lex += current['lexeme']
                    elif current['lexeme'] == "\'":
                        state = 3
                else:
                    return Token(types.MP_RUN_STRING, lex, startingLine, startingCol)
            elif state == 3:
                if scanner.hasNextChar():
                    if current['lexeme'] == "\'":
                        current = scanner.getNextChar()
                        state = 2
                        lex += current['lexeme']
                    else:
                        state = 4
                else:
                    return Token(types.MP_RUN_STRING, lex, startingLine, startingCol)
    return Token(types.MP_STRING_LIT, lex, startingLine, startingCol)

def NumbersFSA(currentChar):
    token = None
    state = 1
    lex = ""
    current = currentChar
    acceptedRule = 0
    while state != 8:
        if state == 1:
            if current['lexeme'] in string.digits:
                state = 2
                lex += current['lexeme']
                token = Token(types.MP_INTEGER_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
            else:
                return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'])
        elif state == 2:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] in string.digits:
                    state = 2
                    lex += current['lexeme']
                    token = Token(types.MP_INTEGER_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
                elif current['lexeme'] == ".":
                    token = Token(types.MP_INTEGER_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
                    state = 4
                    lex += current['lexeme']
                elif current['lexeme'] == "e" or current['lexeme'] == "E":
                    token = Token(types.MP_INTEGER_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
                    state = 3
                    lex += current['lexeme']
                else:
                    acceptedRule = 2
                    state = 8
                    token = Token(types.MP_INTEGER_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
            else:
                acceptedRule = 2
                state = 8
        elif state == 3:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] == "+" or current['lexeme'] == "-":
                    state = 6
                    lex += current['lexeme']
                elif current['lexeme'] in string.digits:
                    state = 5
                    lex += current['lexeme']
                else:
                    scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                    return token
            else:
                scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                return token
        elif state == 4:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] in string.digits:
                    state = 7
                    lex += current['lexeme']
                else:
                    scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                    return token
            else:
                scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                return token
        elif state == 5:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] in string.digits:
                    state = 5
                    lex += current['lexeme']
                else:
                    acceptedRule = 5
                    state = 8
                token = Token(types.MP_FLOAT_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
            else:
                acceptedRule = 5
                state = 8
        elif state == 6:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] in string.digits:
                    state = 5
                    lex += current['lexeme']
                else:
                    scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                    return token
            else:
                scanner.setColumnIndex(current['colIndex'] + len(lex) -1)
                return token
        elif state == 7:
            if scanner.hasNextChar():
                current = scanner.getNextChar()
                if current['lexeme'] in string.digits:
                    state = 7
                    lex += current['lexeme']
                    token = Token(types.MP_FIXED_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
                elif current['lexeme'] == "e" or current['lexeme'] == "E":
                    token = Token(types.MP_FIXED_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
                    state = 3
                    lex += current['lexeme']
                else:
                    acceptedRule = 7
                    state = 8
                    token = Token(types.MP_FIXED_LIT, lex, current['lineIndex'], current['colIndex'] - len(lex))
            else:
                acceptedRule = 7
                state = 8
        if state == 8:
            Type = None
            if acceptedRule == 2:
                Type = types.MP_INTEGER_LIT
            elif acceptedRule == 5:
                Type = types.MP_FLOAT_LIT
            elif acceptedRule == 7:
                Type = types.MP_FLOAT_LIT
            token = Token(Type, lex, current['lineIndex'], current['colIndex'] - len(lex))
    return token

def WhitespaceFSA(currentChar):
    token = None
    state = 1
    lex = ""
    current = currentChar
    while state != 3:
        if not scanner.hasNextChar() and state == 2:
            state = 3
        else:
            if state == 1:
                if current['lexeme'] == " " or current['lexeme'] == "\t":
                    state = 2
                    lex += current['lexeme']
            elif state == 2:
                current = scanner.getNextChar()
                if current['lexeme'] == " " or current['lexeme'] == "\t":
                    state = 2
                    lex += current['lexeme']
                else:
                    state = 3
    return Token(types.MP_WHITESPACE, lex, current['lineIndex'], current['colIndex'] - len(lex))

def CommentFSA(currentChar):
    state = 1
    lex = ""
    current = currentChar
    startingLine = current['lineIndex']
    startingCol = current['colIndex']
    openBraceCount = 0
    while state != 3:
        if not scanner.hasNextChar() and state == 3:
            state = 3
        else:
            if state == 1:
                if current['lexeme'] == "{":
                    openBraceCount += 1
                    state = 2
            elif state == 2:
                if scanner.hasNextChar():
                    current = scanner.getNextChar()
                    if current['lexeme'] == "}":
                        openBraceCount -= 1
                        if openBraceCount == 0:
                            state = 3
                    elif current['lexeme'] == "{":
                        print "WARNING: found a nested {, please check the comments. Found @ line: " + str(current['lineIndex']) + ", column: " + str(current['colIndex'])
                        openBraceCount += 1
                        char = scanner.getNextChar()
                        lex += char['lexeme']
                    else:
                        char = scanner.getNextChar()
                        lex += char['lexeme']
                else:
                    return Token(types.MP_RUN_COMMENT, lex, startingLine, startingCol)
    return Token(types.COMMENT, lex, startingLine, startingCol)

def SymbolFSA(currentChar):
    token = None
    state = 1
    lex = ""
    current = currentChar
    while state != 18:
        if not scanner.hasNextChar() and (state >= 2 and state <= 17):
            state = 18
        else:
            if state == 1:
                if current['lexeme'] == ".":
                    state = 2
                elif current['lexeme'] == ",":
                    state = 3
                elif current['lexeme'] == ";":
                    state = 4
                elif current['lexeme'] == "(":
                    state = 5
                elif current['lexeme'] == ")":
                    state = 6
                elif current['lexeme'] == "=":
                    state = 7
                elif current['lexeme'] == "+":
                    state = 8
                elif current['lexeme'] == "-":
                    state = 9
                elif current['lexeme'] == "*":
                    state = 10
                elif current['lexeme'] == ":":
                    state = 11
                elif current['lexeme'] == "<":
                    state = 13
                elif current['lexeme'] == ">":
                    state = 16
                elif current['lexeme'] == "/":
                    state = 19
                lex += current['lexeme']
            elif state in range(2, 11) or state == 19:
                state = 18
            elif state == 11: # :
                if current['lexeme'] == "=":
                    current = scanner.getNextChar()
                    lex += current['lexeme']
                    state = 12
                else:
                    state = 18
            elif state == 12: # :=
                state = 18
            elif state == 13: # <
                if current['lexeme'] == ">":
                    current = scanner.getNextChar()
                    lex += current
                    state = 14
                elif current['lexeme'] == "=":
                    current = scanner.getNextChar()
                    lex += current
                    state = 15
                else:
                    state = 18
            elif state == 14: # <>
                state = 18
            elif state == 15: # <=
                state = 18
            elif state == 16: # >
                if current['lexeme'] == "=":
                    current = scanner.getNextChar()
                    lex += current['lexeme']
                    state = 17
                else:
                    state = 18
            elif state == 17: # >=
                state = 18

    thisType = None
    if lex == ".":
        thisType = types.MP_PERIOD
    elif lex == ",":
        thisType = types.MP_COMMA
    elif lex == ";":
        thisType = types.MP_SCOLON
    elif lex == "(":
        thisType = types.MP_LPAREN
    elif lex == ")":
        thisType = types.MP_RPAREN
    elif lex == "=":
        thisType = types.MP_EQUAL
    elif lex == ">":
        thisType = types.MP_GTHAN
    elif lex == ">=":
        thisType = types.MP_GEQUAL
    elif lex == "<":
        thisType = types.MP_LTHAN
    elif lex == "<=":
        thisType = types.MP_LEQUAL
    elif lex == "<>":
        thisType = types.MP_NEQUAL
    elif lex == ":=":
        thisType = types.MP_ASSIGN
    elif lex == "+":
        thisType = types.MP_PLUS
    elif lex == "-":
        thisType = types.MP_MINUS
    elif lex == "*":
        thisType = types.MP_TIMES
    elif lex == "/":
        thisType = types.MP_DIV
    elif lex == ":":
        thisType = types.MP_COLON

    token = Token(thisType, lex, current['lineIndex'], current['colIndex'] - len(lex))

    return token