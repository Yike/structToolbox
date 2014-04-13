''' Module that contains the likelihood calculations.
'''

# standard library
import numpy        as np
from scipy.stats import norm

# project library
from _auxiliary import cdfConditional_single, cdfConditional_multiple
import tools.computation.performance.performance    as perf

def sampleLikelihood(obsEconomy, parasObj, static):
    ''' Function calculates the sample likelihood.
    '''
    
    # Select implementation
    if(static): 
                
        likl = _staticCalculation(obsEconomy, parasObj)
    
    else:
        
        likl = _scalarEvaluations(obsEconomy, parasObj)

    # Quality checks
    assert (np.isfinite(likl))
    assert (isinstance(likl, float))    
    
    # Finishing.
    return likl

''' Private functions.
'''
def _staticCalculation(obsEconomy, parasObj):
    ''' Calculation of sample likelihood.
    '''
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
        
        idxExperience = np.dot(z, coeffs.T) 
                
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
                        
        idxChild = np.dot(n, (cost - subsidy) + coeff.T)
                
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

def _scalarEvaluations(obsEconomy, parasObj):
    ''' Calculation of likelihood using OOP paradigm.
    '''
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
            prob = _individualLikelihood(agentObj, parasObj, period)
                                              
            # Collect results.
            likl = likl + prob
    
    # Finishing.
    return likl

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

            