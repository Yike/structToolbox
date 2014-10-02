#!/usr/bin/env python
''' Module for all things related to the aggregation of multiple
    optimization processes.
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
 
# standard library
import pickle  as pkl
import numpy   as np

from signal     import signal
from signal     import SIGTERM 
from sys        import exit

import argparse
import atexit
import time
import glob
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.auxiliary  import writeStep
from tools.auxiliary  import readStep
from tools.clsMeta    import meta

''' Auxiliary function
'''
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    terminate = args.terminate 

    start     = args.start 
    
    # Assertions.
    assert (start in [True, False])
    assert (terminate in [True, False])
    assert ((terminate is True) or (start is True))
        
    # Finishing.
    return start, terminate

''' Main Class.
'''
class aggregatorCls(meta):
    
    def __init__(self):

        # Constitutive attributes.
        self.attr = {}
        
        # Derived attributes.
        self.attr['stepFval'] = np.inf
        
        self.attr['count']    = 0        
        
        self.attr['root']     = None
    
        # Status Indicator.
        self.isLocked = False
 
    ''' Public Methods.
    '''
    def run(self):
        ''' Aggregate multiple logging files.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Main loop.
        isStarting = True
        
        while True:

            time.sleep(1)
            
            try:

                names = glob.glob('.slave*.struct.out')

            except:
                
                continue
            
            # Determine active processes.
            numActive = self._process(names)

            if((numActive == 0) and (isStarting is False)): break

            #Update initialization period.
            if(isStarting):
                
                if(numActive > 0):
                     
                    isStarting = False
            
    ''' Private Methods.
    '''
    def _derivedAttributes(self):
        ''' Create derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)

        # Initialize lock file.   
        with open('.aggregator.struct.out', 'w') as file_:
            
            file_.write(str(os.getpid()))
            
        self.attr['root'] = os.getcwd()
        
    def _process(self, names):
        ''' Process multiple logging files.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (isinstance(names, list))

        # Distribute class attributes.
        count = self.attr['count']
        
        # Process files.
        numActive = 0
        
        for name in names:

            stepFval = self.attr['stepFval']
            
            # Count active processes.
            if(os.path.exists(name + '/.optimization.struct.out')):
            
                numActive = numActive + 1
            
            try:
                
                dict_ = pkl.load(open(name + '/stepInfo.struct.pkl', 'r')) 
                
                fval, vals = dict_['fval'], dict_['vals']
                
            except:
                        
                continue
                
            # Determine event.  
            isStep = (fval < stepFval)
                
            if(not isStep): continue
                
            # Check.
            os.chdir(name)
            
            assert (len(readStep('paras') == len(vals)))
            
            os.chdir('../')

            # Update logging.
            writeStep(vals, fval, count, pkl_ = False)
  
            # Update attributes.        
            self.attr['stepFval'] = fval
            
            self.attr['count']    = count + 1
        
        return numActive
    
    def _cleanup(self):
        ''' Cleanup process.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        root = self.attr['root']
            
        # Remove lock file.
        os.remove(root + '/.aggregator.struct.out')
        
def aggregate(start = False, terminate = False):
    ''' Start subprocess that aggregates.
    '''
    # Antibugging.
    assert (start in [True, False])
    assert (terminate in [True, False])
    assert ((terminate is True) or (start is True))
        
    # Process.
    if(start):

        if(os.path.exists('.aggregator.struct.out')):
            
            raise AssertionError
    
    if(terminate):

        if(not os.path.exists('.aggregator.struct.out')):
            
            raise AssertionError
    
    if(start):
        
        # Initialize lock file.   
        open('.aggregator.struct.out', 'w').close()
        
        # Initialize child.
        aggObj = aggregatorCls()
                   
        # Ensure gentle termination.
        atexit.register(aggObj._cleanup,)
            
        signal(SIGTERM, lambda signum, stack_frame: exit(1))
                            
        # Start aggregation.
        aggObj.lock()
    
        aggObj.run()
        
    elif(terminate):
        
        pid = int(open('.aggregator.struct.out', 'r').read())

        os.kill(int(pid), SIGTERM)
        
    else:
        
        raise AssertionError
    
''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
      'Working with aggregator to manage multiple optimization instances.', 
      formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--terminate', \
                        action  = 'store_true', \
                        dest    = 'terminate', \
                        default = False, \
                        help    = 'terminate aggregator')
    
    parser.add_argument('--start', \
                        action  = 'store_true', \
                        dest    = 'start', \
                        default = False, \
                        help    = 'start aggregator')
        
    start, terminate = _distributeInput(parser)

    aggregate(start = start, terminate = terminate)  