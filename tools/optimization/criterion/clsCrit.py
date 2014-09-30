''' Module that holds the criterion function.
'''
# standard library
from scipy.stats    import norm

import numpy        as np

# project library
import tools.computation.speed.performance as perf    

from tools.optimization.criterion.logger.clsLogger  import loggerCls
from tools.clsMeta                                  import meta

# submodule
from tools.optimization.criterion._auxiliary import cdfConditional_multiple
from tools.optimization.criterion._auxiliary import cdfConditional_single

''' Classes
'''
class critCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        # Constitutive attributes.
        self.attr['obsEconomy'] = None
        
        self.attr['parasObj']   = None

        self.attr['derived']    = None

        # Derived attributes.
        self.attr['logObj']     = None
        
        self.attr['static']     = None

        # Status.
        self.isLocked = False     
    
    def evaluate(self, x):
        ''' SciPy wrapper for criterion function.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (isinstance(x, np.ndarray))
        assert (np.all(np.isfinite(x)))
        assert (x.ndim == 1)
        assert (x.dtype == 'float')
        
        # Distribute class attributes.
        parasObj = self.attr['parasObj']
        
        logObj   = self.attr['logObj']

        # Update parameters.
        parasObj.update(x, 'external', 'free')
                
        # Criterion function.    
        fval = self._sampleLikelihood(parasObj)
       
        # Logging. 
        logObj.process(fval, x)

        # Finishing. 
        return fval   
     
    ''' Private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        parasObj = self.attr['parasObj']
        
        derived  = self.attr['derived']
        
        # Encapsulation.
        self.attr['static'] = derived['static']
        
        # Initialize logger.
        logObj = loggerCls()
        
        logObj.setAttr('parasObj', parasObj)
        
        logObj.lock()
        
        # Collect.
        self.attr['logObj'] = logObj
        
        # Cleanup
        del self.attr['derived']
        
    def _sampleLikelihood(self, parasObj):
        ''' Function calculates the sample likelihood.
        '''
        # Distribute class attributes.
        static     = self.attr['static']
        
        # Select implementation
        if(static): 
                    
            likl = self._staticCalculation(parasObj)
        
        else:
            
            likl = self._scalarEvaluations(parasObj)
    
     
        # Quality checks
        assert (np.isfinite(likl))
        assert (isinstance(likl, float))    
        
        # Finishing.
        return likl
    
    def _staticCalculation(self, parasObj):
        ''' Calculation of sample likelihood.
        '''
        # Distribute class attributes.
        obsEconomy = self.attr['obsEconomy']
        
        # Distribute class attributes
        numPeriods = obsEconomy.getAttr('numPeriods')
            
        attr       = obsEconomy.getAttr('attr')
    
        # Auxiliary objects.
        contrib = []
    
        # Loop over periods.    
        for t in range(numPeriods):
            
            # Experiences.
            wages     = obsEconomy.getAttr('wages')[t] 
        
            choices   = obsEconomy.getAttr('choices')[t]
            
            # Experience 
            coeffs        = parasObj.getParameters('experience')
                            
            z             = attr['experience'][t]
          
            idxExperience = np.dot(z, coeffs) 
                    
            # Wage 
            coeffs, int_ = parasObj.getParameters('wage')
                            
            z            = attr['wage'][t]
            
            idxWage      = np.dot(z, coeffs.T)  + int_ + idxExperience
                        
            # Utility 
            coeffs, int_ = parasObj.getParameters('utility')
                            
            z            = attr['utility'][t]
                            
            idxUtility   = np.dot(z, coeffs.T)  + int_
            
            # Children 
            coeff    = parasObj.getParameters('child')
                            
            cost     = parasObj.getParameters('cost')
                            
            subsidy  = parasObj.getParameters('subsidy') 
                            
            n        = attr['children'][t]
                            
            idxChild = np.dot(n, (cost - subsidy) + coeff)
                    
            # Latent variable index
            xiStar = idxWage - idxChild - idxUtility
            
            # Home.
            xi   = parasObj.getParameters('xi')
                                                    
            home = norm.cdf(-xiStar, xi['mean'], xi['sd'])
                
            # Working.
            eta  = parasObj.getParameters('eta')
                                
            # Working (unconditional)  
            real          = wages - idxWage
            
            unconditional = norm.pdf(real, eta['mean'], eta['sd'])      
            
            conditional   = 1.0 - cdfConditional_multiple(-xiStar, xi, eta, real) 
        
            working       = conditional*unconditional
            
            working[np.isnan(working)] = 0.0
     
            # Aggregation.
            contrib += [choices*working + (1.0 - choices)*home]
           
        # Collect across periods.
        contrib = np.clip(contrib, 1e-20, np.inf)
                
        likl    = -np.log(contrib)
        
        likl    = np.sum(likl)

        # Finishing
        return likl
    
    def _scalarEvaluations(self, parasObj):
        ''' Calculation of likelihood using OOP paradigm.
        '''
        # Distribute class attributes.
        obsEconomy = self.attr['obsEconomy']
        
        # Distribute class attributes.  
        numPeriods = obsEconomy.getAttr('numPeriods')
        
        agentObjs  = obsEconomy.getAttr('agentObjs')
            
        likl = 0.0
        
        # Calculate likelihood.
        for agentObj in agentObjs:
                
            # Update agent calculations.
            agentObj.unlock()
                
            agentObj.setAttr('parasObj', parasObj)
                    
            agentObj.lock()
                    
            # Collect probabilities.
            for period in range(numPeriods):
                
                # Calculate likelihood.
                prob = self._individualLikelihood(agentObj, parasObj, period)
                                                  
                # Collect results.
                likl = likl + prob
        
        # Finishing.
        return likl
    
    @staticmethod
    def _individualLikelihood(agentObj, parasObj, period):
        ''' Calculation of individual likelihood.
        '''
        # Distribute agent attributes.
        wage     = agentObj.attr['wages'][period]
    
        position = agentObj.attr['states'][period + 1]
        
        idxWage  = agentObj.attr['w']['exAnte'][position]
        
        choice   = agentObj.attr['choices'][period]
        
        # Observable components.
        upper, lower = position[:-1] + '1', position[:-1] + '0'
        
        xiStar       = agentObj.attr['v']['exAnte'][upper] - \
                            agentObj.attr['v']['exAnte'][lower]
        
        xi   = parasObj.getParameters('xi')
        
        eta  = parasObj.getParameters('eta')
        
        # Select calculation.
        if(choice == 0):
            
            prob = perf.norm_cdf(-xiStar, xi['mean'], xi['sd'])
                    
        else:
                                                                
            ''' Unconditional distribution.
            '''              
            real          = wage - idxWage
            
            unconditional = perf.norm_pdf(real, eta['mean'], eta['sd'])
                                     
            ''' Conditional distribution.
            '''
            conditional = 1.0 - cdfConditional_single(-xiStar, xi, eta, real) 
          
            prob        = conditional*unconditional
            
        # Aggregation.        
        prob = perf.clip(prob, 1e-20, perf.inf)
                            
        prob = -perf.log(float(prob))
        
        # Quality checks.
        assert (perf.isfinite(prob))
        assert (isinstance(prob, float))
        
        # Finishing.
        return prob
