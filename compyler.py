#!/usr/bin/env python
import scanner as scanner
import dispatcher as dispatcher
from tokens import EOF
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
    writeln("  Line Col  Token") 
  
    dispatcher.initialize(sourceText) 
  
    while True:
        token = dispatcher.getToken()
        writeln(token.show()) 
        if token.type == EOF: break
    
def writeln(*args): 
    for arg in args: 
        print str(arg)

if __name__ == "__main__":
    main()
    print "Completed run of Compiler."