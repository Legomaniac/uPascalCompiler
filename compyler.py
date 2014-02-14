#!/usr/bin/env python
import parser as parser
import sys

"""
microPascal compiler implemented in Python
This is the main driver for the program
"""

def main():
    print "We have started the Parser."
    fname = sys.argv[1]
    sourceText = open(str(fname)).read()
    writeln("Token             Line    Col     Lexeme")
    parser.parse(sourceText)
    
def writeln(*args): 
    for arg in args: 
        print str(arg)

if __name__ == "__main__":
    main()
    print "Completed Parse!"