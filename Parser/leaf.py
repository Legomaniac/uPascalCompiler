class Leaf:
    def __init__(self, token=None):
        self.token = token
        self.level = 0
        self.children = []  # a list of all children
    
    def add(self, token):
        """
        make a leaf out of a token and add it to self.children
        """
        self.addNode(  Leaf(token) )
        
    def addLeaf(self, leaf):
        """
        add a leaf to self.children
        """
        leaf.level = self.level + 1
        self.children.append(leaf)
        
    def toString(self):
        s = "    " * self.level
        
        if self.token == None: s += "ROOT\n"
        else: s +=  self.token.cargo + "\n"
            
        for child in self.children:
            s += child.toString()
        return s