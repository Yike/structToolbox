''' Interface to all maximization algorithm.
'''

# standard library
import subprocess
import os

# project library
from tools.optimization.optimizers._scipyAlgorithms  import scipyInterface
from tools.optimization.optimizers._processOptions   import initializeOptions
from tools.clsMeta                                   import meta

class optimizationCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        # Constitutive attributes.
        self.attr['optimization'] = None

        self.attr['startVals']    = None             

        self.attr['critObj']      = None
        
        self.attr['single']       = None

        # Derived attributes.
        self.attr['algorithm'] = None
                                
        # Status indicator.
        self.isLocked = False 
    
    def optimize(self):
        ''' Optimization.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        algorithm  = self.attr['algorithm'] 

        startVals  = self.attr['startVals']
        
        critObj    = self.attr['critObj']
                
        single     = self.attr['single'] 
        
        # Initialize options.
        optsDict = initializeOptions() 
        
        # Special treatment for single evaluation.
        if(single):

            critObj.evaluate(startVals)
            
            for file_ in ['startInfo.struct.out', 'stepInfo.struct.pkl']:
                
                os.remove(file_)
        
        else:
            
            if('SCIPY' in algorithm): interface = scipyInterface
            
            interface(algorithm, optsDict, critObj, startVals)
                 
    ''' Private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute attributes.
        optimization = self.attr['optimization']
        
        single       = self.attr['single']
          
        # Encapsulation.
        self.attr['algorithm'] = optimization['algorithm']     

        # Start aggregator (if required).
        if(not os.path.exists('.aggregator.struct.out')): 
            
            if(not single): self._startAggregator()
            
        # Cleanup.
        del self.attr['optimization']
        
    def _startAggregator(self):
        ''' Start aggregator for multiple optimization runs.
        '''
        # Antibugging.
        assert (not os.path.exists('.aggregator.struct.out'))
        
        # Start subprocess.
        script = os.path.dirname(os.path.realpath(__file__)).replace('/tools/optimization/optimizers', '') + '/scripts/aggregate.py'

        subprocess.Popen(['python ' + script + ' --start'], \
                shell = True, preexec_fn = os.setsid, close_fds = False)
            