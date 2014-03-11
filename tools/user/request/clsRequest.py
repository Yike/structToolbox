''' Module for the user request.
'''
# project library
from tools.clsMeta import meta

class requestCls(meta):
    
    def __init__(self):
        
        self.attr = {}

        self.attr['parasObj']     = None
                
        self.attr['obsEconomy']   = None
        
        self.attr['optimization'] = None

        self.attr['estimation']   = None        

        self.attr['derived']      = None        
        
        # Status indicator.
        self.isLocked = False
        
    