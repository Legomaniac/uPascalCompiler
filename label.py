import sys

class Label:
    labelCounter = 0
    
    def __init__(self):
        global labelCounter
        labelCounter = 1
    
    def getNextLabel(self):
        global labelCounter
        label = "L" + str(labelCounter)
        labelCounter += 1
        return label