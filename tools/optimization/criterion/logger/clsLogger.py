''' Logging capabilities for the optimization process.
'''
# standard library
import shutil

# project library
from tools.auxiliary import writeStep
from tools.clsMeta   import meta

''' Main function.
'''
class loggerCls(meta):
    
    def __init__(self):
        
        # Constitutive attributes.
        self.attr = {}

        self.attr['parasObj']  = None
        
        # Derived attributes.
        self.attr['stepVals']  = None

        self.attr['stepFval']  = None
        
        self.attr['count']     = None
        
        # Status indicator.
        self.isLocked = False
    
    ''' Public methods.
    '''
    def process(self, fval, x):
        ''' Process event.
        '''
        
        internal = self._transform(x, 'internal')
        
        # Auxiliary objects.
        isStart = (self.attr['stepFval'] is None)
        
        # Process start.
        if(isStart): self._initialize(fval, internal)
                
        # Determine event.
        isStep = (fval < self.attr['stepFval'])
        
        if((not isStep) and (not isStart)): return None
        
        # Write step.
        self._writeStep(fval, internal)
        
        # Starting values.
        if(isStart):
            
            shutil.copy('stepInfo.struct.out', 'startInfo.struct.out')

        # Update attributes.     
        self.attr['stepFval'] = fval

        self.attr['count']    = self.attr['count'] + 1

    def _transform(self, x, version):
        ''' Transform free external values.
        '''
        # Distribute class attributes.
        parasObj = self.attr['parasObj']
        
        # Update parameter.        
        parasObj.update(x, 'external', 'free')
        
        # Transform values.
        if(version == 'internal'):
            
            values = parasObj.getValues('internal', 'all')
        
        else:
            
            values = parasObj.getValues('external', 'all')
        
        # Finishing.
        return values
    
    def _writeStep(self, fval, internal):
        ''' Write step.
        '''
        # Distribute class attributes.
        count = self.attr['count']
       
        # Write to file.
        writeStep(internal, fval, count, pkl_ = True)

    ''' Private methods.
    '''
    def _initialize(self, startFval, startVals):
        ''' Initialize logging files. 
        '''
        
        # Initialize.
        self.attr['stepFval'] = startFval
            
        self.attr['count']    = 0

        