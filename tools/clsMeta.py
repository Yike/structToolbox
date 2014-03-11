''' Meta class for simSandbox.
'''

# standard library
import cPickle as pkl
import copy

class meta(object):
    
    def __init__(self):
        
        pass
    
    ''' Meta methods.
    '''
    def getStatus(self):
        ''' Get status of class instance.
        '''
        
        return self.isLocked

    def lock(self):
        ''' Lock class instance.
        '''
        # Antibugging.
        assert (self.getStatus() == False)

        # Update class attributes.
        self.isLocked = True
        
        # Finalize.
        self._derivedAttributes()
        
        self._checkIntegrity()
    
    def unlock(self):
        ''' Unlock class instance.
        '''
        # Antibugging.
        assert (self.getStatus() == True)

        # Update class attributes.
        self.isLocked = False

    def getAttr(self, key, deep = False):
        ''' Get attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (deep in [True, False])
        
        # Copy requested object.
        if(deep):
            
            attr = copy.deepcopy(self.attr[key])
        
        else:
            
            attr = self.attr[key]
        
        # Finishing.
        return attr

    def setAttr(self, key, value, deep = False):
        ''' Get attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == False)
        assert (key in self.attr.keys())

        # Copy requested object.
        if(deep):
            
            attr = copy.deepcopy(value)
        
        else:
            
            attr = value
              
        # Finishing.
        self.attr[key] = attr
        
    def _derivedAttributes(self):
        ''' Calculate derived attributes.
        '''
        
        pass
    
    def _checkIntegrity(self):
        ''' Check integrity of class instance.
        '''
        
        pass
    
    def store(self, fileName):
        ''' Store class instance.
        '''
        # Antibugging.
        assert (self.getStatus() == True)      
        assert (isinstance(fileName, str))
        
        # Store.
        pkl.dump(self, open(fileName, 'wb'))
        