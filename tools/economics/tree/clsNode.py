''' Module that contains.
'''


# project library
from tools.clsMeta import meta

class nodeCls(meta):
    '''    Class container for each node.
    '''
    
    def __init__(self):
        
        self.attr = {}
        
        
        self.attr['lower']    = None

        self.attr['upper']    = None
        
        self.attr['parent']   = None

        self.attr['name']     = None
        
        self.attr['depth']    = 0
        

        self.attr['numBranches']  = 0
                
        self.attr['isTerminal']  = True

        # Status.
        self.isLocked = False
    
