##FSA plugin with all implemented FSA methods
from token import *
from tokens import *
from tokenTypes import *
import scanner as scanner

class ScanError(Exception): pass

"""FSA for Identifiers"""
def IdentifierFSA(currentChar):
    token = None
    state = 1
    lex = ""
    current = currentChar
    while state != 4:
        if not scanner.hasNextChar() and state == 2:
            state = 4
        else:
            if state = 1:
                if current['lexeme'] in string.letters:
                    state = 2
                    lex += current['lexeme']
                elif current['lexeme'] == "_":
                    state = 3
                    lex += current['lexeme']
                else:
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'])
            elif state = 2:
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
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'])
            elif state = 3:
                if scanner.hasNextChar():
                    current = scanner.getNextChar()
                    if current['lexeme'] in string.letters:
                        state = 2
                        lex += current['lexeme']
                    else:
                        return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'])
                else:
                    return Token(types.MP_ERROR, str(current['lexeme']), current['lineIndex'], current['colIndex'])
            else:
                continue
    if current['lexeme'] in ReservedWords:
        token = Token(ReservedWords[current['lexeme']], lex, current['lineIndex'], current['colIndex'])
    else:
        token = Token(types.MP_IDENTIFIER, lex, current['lineIndex'], current['colIndex'] - len(lex))
    return token

## NEED TO ADD THE OTHER FSA'S