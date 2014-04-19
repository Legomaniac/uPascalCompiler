#!/usr/bin/env python
import sys
from Parser import parser as parser

"""
microPascal compiler implemented in Python
This is the main driver for the program
"""

def main():
    print "############# Starting run of Compyler #############"
    fname = sys.argv[1]
    if fname.__len__() > 0:
        sourceText = open(str(fname)).read()
        parser.parse(sourceText)
    else:
        print "User Input Error: This program requires a filepath parameter..."

def writeln(*args):
    for arg in args:
        print str(arg)

if __name__ == "__main__":
    main()
    print "Completed run of Compiler."