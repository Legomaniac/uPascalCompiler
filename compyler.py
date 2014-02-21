#!/usr/bin/env python
import scanner as scanner
from tokens import *
import sys

"""
microPascal compiler implemented in Python
This is the main driver for the program
"""

def main():
    print "We have started the compiler"
    fname = sys.argv[1]
    sourceText = open(str(fname)).read()
    writeln("Here are the tokens returned by the scanner:")
    writeln("Token Line Col Lexeme")
    scanner.initialize(sourceText)
    while True:
        token = scanner.getToken()
        if token is None:
            print "Exception thrown! Quitting now..."
            break
        writeln(token.show())
        if token.type == EPSILON: break
                
def writeln(*args):
    for arg in args:
        print str(arg)

if __name__ == "__main__":
    main()
    print "Completed run of Compiler."