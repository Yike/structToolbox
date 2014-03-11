''' Module that holds the class for the parameters.
'''

# standard library
import copy

# project library
from tools.clsMeta import meta
  
class paraCls(meta):
    ''' Object that holds single parameters.         
    '''
    def __init__(self):
        
        self.attr = {}

        # Attributes.
        self.attr['type']    = None
        
        self.attr['subtype'] = None
        
        self.attr['start']   = None

        self.attr['rest']    = None
        
        # Derived attributes.
        self.attr['update']  = None

        self.attr['value']   = None

        self.attr['bounds']  = None
                
        # Status.
        self.isLocked = False
    
    def setValue(self, value):
        ''' Set value of parameter.
        '''
        # Antibugging.
        assert (isinstance(value, float))
        
        # Check bounds.
        lowerBound, upperBound = self.attr['bounds']
        
        if(lowerBound is not None): assert (lowerBound < value)
        
        if(upperBound is not None): assert (upperBound > value)

        # Update value.
        self.attr['value'] = value
        
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        startVal = self.attr['start']
        
        # Process values.
        self.attr['value'] = copy.deepcopy(startVal)
        
        # Process restrictions.
        type_, info  = self.attr['rest']

        self.attr['update'], self.attr['bounds'] = True, info
                
        if(type_ in ['fixed']):
            
            self.attr['update'] = False
