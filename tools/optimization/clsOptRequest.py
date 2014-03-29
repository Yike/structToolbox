''' Module for the optimization request.
'''
# project library
from tools.clsMeta import meta

class optRequestCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        self.attr['userRequestObj'] = None
        
        self.attr['optimization']   = None

        self.attr['commObj']        = None
        
        self.attr['obsEconomy']     = None
        
        self.attr['parasObj']       = None

        self.attr['startVals']      = None
        
        self.attr['static']         = None
        
        # Status indicator.
        self.isLocked = False
        
    def _derivedAttributes(self):
        ''' Derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
