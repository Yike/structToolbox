''' Interface to all maximization algorithm.
'''
# project library
from tools.clsMeta import meta

# Submodules
from _processOptions        import initializeOptions
from scipy.scipyAlgorithms  import scipyCls

class algoCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        self.attr['requestObj'] = None
        
        # Derived attributes.
        self.attr['source']  = None

        self.attr['options'] = None

        self.attr['toolbox'] = None
                
        # Status indicator.
        self.isLocked = False 
    
    def optimize(self):
        ''' Optimization.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        requestObj = self.attr['requestObj'] 
        
        options    = self.attr['options'] 
        
        toolbox    = self.attr['toolbox'] 
        
        # Initialize options.
        optsDict = initializeOptions(options)
                
        # Select toolbox.
        if(toolbox == 'SCIPY'):
        
            optObj = scipyCls(requestObj, optsDict)
#
        else:
            
            assert (False == True)
           
        
        optObj.lock()
            
        optObj.optimize()
        
    ''' Private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        requestObj   = self.attr['requestObj']
        
        optimization = requestObj.getAttr('optimization')
        
        # Encapsulation.
        self.attr['source']  = requestObj.getAttr('optimization')

        self.attr['options'] = optimization['options']

        self.attr['toolbox'] = optimization['toolbox']
        
        