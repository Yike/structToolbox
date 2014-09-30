''' Interface to SciPy algorithms.
'''
__all__ = ['scipyInterface']

# standard library
import sys
import os

import pickle      as      pkl

from scipy.optimize  import  fmin_powell
from scipy.optimize  import  fmin_bfgs

# submodules
from tools.optimization.optimizers._auxiliary import setup

''' Algorithm interface.
'''
def scipyInterface(algorithm, optsDict, critObj, startVals):
    ''' Interface to the SCIPY algorithms
    '''
    
    # Setup.
    setup()
    
    # Distribute class attributes.
    opts = optsDict[algorithm]
    
    # Select interface.
    sys.stdout = open('optimizer.struct.out', 'w')

    if('BFGS'   in algorithm): rslt = _scipyBfgs(critObj, startVals, opts)

    if('POWELL' in algorithm): rslt = _scipyPowell(critObj, startVals, opts)
    
    sys.stdout = sys.__stdout__ 

    # Storage.
    pkl.dump(rslt, open('rslt.struct.pkl', 'w'))

       
    os.chdir('../')
            
''' Private functions.
'''
def _scipyBfgs(self, startVals, opts):
    ''' Interface to BFGS algorithm.
    '''
    # Distribute options.
    gtol    = opts['gtol']
                
    epsilon = opts['epsilon']

    maxiter = opts['maxiter']
                
    # Interface to algorithm.
    opt = fmin_bfgs(self.evaluate, startVals, gtol = gtol, \
                    epsilon = epsilon, maxiter = maxiter, \
                    full_output = True)
        
    # Prepare interface.
    rslt = {}; rslt['x'], rslt['fun'] = opt[0], opt[1]
       
               
    msg = 'None'

    if(opt[6] == 1): msg = 'Maximum number of iterations exceeded.'
        
    if(opt[6] == 2): msg = 'Gradient and/or function calls not changing.'
    
    rslt['message'] = msg
        
        
    rslt['success'] = (opt[6] == 0)

    rslt['opt']     = opt
                
    # Finishing.
    return rslt 
    
def _scipyPowell(self, startVals, opts):
    ''' Interface to the Powell algorithm.
    '''
    # Distribute options.
    xtol    = opts['xtol']
                
    ftol    = opts['ftol']
                
    maxfun  = opts['maxfun']

    maxiter = opts['maxiter']
        
    # Interface to algorithm.
    opt = fmin_powell(self.evaluate, startVals, \
                xtol = xtol, ftol = ftol, maxiter = maxiter, \
                maxfun = maxfun, full_output = True)   
        
    # Prepare interface.
    rslt = {}; rslt['x'], rslt['fun'] = opt[0], opt[1]
            
            
    msg = 'None'

    if(opt[5] == 1): msg = 'Maximum number of function evaluations exceeded.'
        
    if(opt[5] == 2): msg = 'Maximum number of iterations exceeded.'   
    
    rslt['message'] = msg
        
        
    rslt['success'] = (opt[5] == 0)

    rslt['opt']     = opt
        
    # Finishing.
    return rslt