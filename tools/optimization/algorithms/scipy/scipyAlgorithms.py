''' Interface to SciPy algorithms.
'''
# standard library
import  sys

import  cPickle         as      pkl
import  numpy           as      np

from    scipy.optimize  import  fmin_powell
from    scipy.optimize  import  fmin_bfgs

# project library
from tools.clsMeta import meta

from tools.optimization.criterions.mle.calculations import sampleLikelihood

# Submodules.
from ._logging import logging

class scipyCls(meta):
    
    def __init__(self, requestObj, optsDict):
        
        # Antibugging.
        assert (requestObj.getStatus() == True)
        
        self.attr = {}


        self.attr['startVals']      = requestObj.getAttr('startVals')

        self.attr['optimization']   = requestObj.getAttr('optimization') 

        self.attr['obsEconomy']     = requestObj.getAttr('obsEconomy') 

        self.attr['commObj']        = requestObj.getAttr('commObj') 

        self.attr['parasObj']       = requestObj.getAttr('parasObj') 
            
        self.attr['static']         = requestObj.getAttr('static') 


        self.attr['optsDict']       = optsDict
                        
                        
        # Derived attributes.        
        self.attr['rslt'] = None
                
        # Logging.
        self.attr['fval'] = {}
        
        self.attr['fval']['current'] = None

        self.attr['fval']['step']    = None        
        
        self.attr['fval']['start']   = None        

        self.attr['step'] = 0

        # Status.
        self.isLocked = False
    
    ''' Public methods.
    '''           
    def optimize(self):
        ''' Minimize criterion function using SciPy maximization algorithm.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribution of attributes.
        startVals = self.attr['startVals']
        
        optsDict  = self.attr['optsDict']

        # Auxiliary objects.
        optimizer = self.attr['optimization']['optimizer']
                
        maxiter   = self.attr['optimization']['maxiter']
        
        # Maximization.
        opts = optsDict[optimizer]
        
        # Special treatment for single evaluation.
        if(maxiter == 0):
            
            rslt = {}
            
            rslt['x']       = startVals
            
            rslt['fun']     = self._criterionFunction(startVals)
             
            rslt['message'] = 'Single function evaluation at starting values.'
        
            rslt['success'] = True
        
        else:
            
            sys.stdout = open('/dev/null', 'w')
            
            if(optimizer == 'SCIPY-POWELL'):
                
                rslt = self._powell(startVals, maxiter, opts)
            
            if(optimizer == 'SCIPY-BFGS'):
                
                rslt = self._bfgs(startVals, maxiter, opts)
            
            sys.stdout = sys.__stdout__
                    
        # Logging.
        self.attr['rslt'] = rslt
        
        logging(self, isFinal = True)
                        
        # Store.
        pkl.dump(rslt, open('rslt.struct.pkl', 'w'))

    ''' Algorithm interfaces.
    '''
    def _bfgs(self, startVals, maxiter, opts):
        ''' Interface to BFGS algorithm.
        '''
        # Distribute options.
        gtol    = opts['gtol']
                
        epsilon = opts['epsilon']
        
        # Interface to algorithm.
        opt = fmin_bfgs(self._criterionFunction, startVals, \
                gtol = gtol, epsilon = epsilon, maxiter = maxiter, \
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
        
    def _powell(self, startVals, maxiter, opts):
        ''' Interface to the Powell algorithm.
        '''
        # Distribute options.
        xtol   = opts['xtol']
                
        ftol   = opts['ftol']
                
        maxfun = opts['maxfun']
    
        # Interface to algorithm.
        opt = fmin_powell(self._criterionFunction, startVals, \
                    xtol = xtol, ftol = ftol, maxiter = maxiter, \
                    maxfun = maxfun)   
        
        # Prepare interface.
        rslt = {}; rslt['x'], rslt['fun'] = opt[0], opt[1]

                    
        msg = 'None'

        if(opt[5] == 1): msg = 'Maximum number of function evaluations.'
        
        if(opt[5] == 2): msg = 'Maximum number of iterations.'   
    
        rslt['message'] = msg
        
        
        rslt['success'] = (opt[5] == 0)

        rslt['opt']     = opt
        
        # Finishing.
        return rslt

    ''' Private methods.
    '''   
    def _criterionFunction(self, x):
        ''' SciPy wrapper for criterion function.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (isinstance(x, np.ndarray))
        assert (np.all(np.isfinite(x)))
        assert (x.ndim == 1)
        assert (x.dtype == 'float')
        
        # Distribute class attributes.
        parasObj    = self.attr['parasObj']
        
        obsEconomy  = self.attr['obsEconomy']

        static      = self.attr['static']

        commObj     = self.attr['commObj']
                        
        # Update parameters.
        parasObj.update(x, 'external', 'free')
                
        # Criterion function.    
        rslt = sampleLikelihood(obsEconomy, parasObj, static, commObj)
        
        # Collect results.
        self.attr['fval']['current'] = rslt
        
        # Logging. 
        logging(self, isFinal = False)
        
        # Finishing.
        return rslt      