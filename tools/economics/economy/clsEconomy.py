''' Module that contains the economy class.
'''
# standard library
import numpy as np

# project library
from tools.clsMeta import meta

class economyCls(meta):
    ''' Class instance that governs the economy object
    '''    
    def __init__(self):
        
        self.attr = {}
      
        # Attributes.
        self.attr['parasObj']  = None
        
        self.attr['agentObjs'] = None

        # Derived attributes.
        self.attr['numAgents']  = None
        
        self.attr['numPeriods'] = None 

        
        self.attr['attr'] = {}
        
        self.attr['attr']['children'] = None
        
        self.attr['attr']['utility']  = None

        self.attr['attr']['income']   = None
                
        self.attr['attr']['wage']     = None


        self.attr['wages']            = None

        self.attr['choices']          = None


        # Status indicator.
        self.isLocked = False

    ''' Public Methods.
    '''
    def subset(self, numSubset):
        ''' Select a subset of agents only.
        '''
        # Antibugging. 
        assert (isinstance(numSubset, int))
        assert (0 < numSubset <= self.attr['numAgents'])
        
        # Check applicability.
        if(numSubset is None): return
            
        if(self.attr['numAgents'] == numSubset): return 
        
        # Select subset of agents.
        self.unlock()
        
        self.attr['agentObjs'] = self.attr['agentObjs'][:numSubset]
        
        self.lock()
        
    def simulate(self):
        ''' Simulate economy.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        agentObjs = self.attr['agentObjs']

        for agentObj in agentObjs:
            
            agentObj.step()

        # Update derived attributes.
        self._derivedAttributes()
        
    ''' Private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Distribute attributes.
        agentObjs = self.attr['agentObjs']
        
        # Calculate derived attributes.
        self.attr['numPeriods'] = len(agentObjs[0].attr['choices'])
        
        self.attr['numAgents']  = len(agentObjs)
        
        # Distribute class attributes.
        numPeriods = self.attr['numPeriods']
        
        # Exogenous characteristics.
        labels = ['children', 'wage', 'utility', 'spouse', 'experience']
        
        for label in labels:
        
            self.attr['attr'][label] = {}
            
            for t in range(numPeriods):

                attr = []
                
                for agentObj in agentObjs:
                    
                    attr.append(agentObj.attr['attr'][label][t])
                
                # Type conversion.
                attr = np.array(attr, ndmin = 2)
                
                if(label not in ['wage', 'utility']):
                    
                    attr = attr.T

                self.attr['attr'][label][t] =  attr
        
        # Endogenous characteristics.
        labels = ['wages', 'choices']
    
        for label in labels:

            self.attr[label] = {}
            
            for t in range(numPeriods):
                
                attr = []
            
                for agentObj in agentObjs:
                    
                    attr.append(agentObj.attr[label][t])
           
                # Type conversion.
                attr = np.array(attr, ndmin = 2).T
                            
                self.attr[label][t] = attr 
