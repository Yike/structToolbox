''' Module for the user request.
'''
# project library
from tools.clsMeta import meta

class requestCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        # Constitutive attributes.
        self.attr['optimization'] = None
        
        self.attr['obsEconomy']   = None
        
        self.attr['parasObj']     = None
        
        self.attr['derived']      = None       

        self.attr['single']       = None       

        # Status indicator.
        self.isLocked = False
    
    def _checkIntegrity(self):
        ''' Check integrity of class instance.
        '''  
        # Antibugging.
        assert (self.getStatus() == True)
        