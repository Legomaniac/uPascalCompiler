#!/usr/bin/env python
import parser as parser
import sys

"""Parser Driver File"""
"""Only for lab use"""

def main():
    print "Started parse..."
    fname = sys.argv[1]
    sourceText = open(str(fname)).read()
    writeln("Token                Line    Col     Lexeme")
    parser.parse(sourceText)
    
def writeln(*args): 
    for arg in args: 
        print str(arg)

if __name__ == "__main__":
    main()
    print "Completed parse!"