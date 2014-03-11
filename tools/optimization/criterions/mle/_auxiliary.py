''' Auxiliary functions for the calculations of the MLE criterion functions.
'''


# standard library
import scipy.stats

import numpy        as np
import tools.computation.f90.f90_main     as fort

def cdfConditional_single(eval_, u, v, real):
    ''' Evaluate the cumulative distribution function of the conditional
        distribution of U given V = v.
    '''
    # Calculate ingredients.
    mean = u['mean'] + u['rho']['eta']*(u['sd']/v['sd'])*(real - v['mean'])
    
    sd   = np.sqrt((1.0 - u['rho']['eta']**2)*u['sd']**2)

    # Compute results
    rslt = fort.wrapper_norm_cdf(eval_ - mean, 0.0, sd)

    # Finishing.
    return rslt  

def cdfConditional_multiple(eval_, u, v, real):
    ''' Evaluate the cumulative distribution function of the conditional
        distribution of U given V = v.
    '''
    # Calculate ingredients.
    mean = u['mean'] + u['rho']['eta']*(u['sd']/v['sd'])*(real - v['mean'])
    
    sd   = np.sqrt((1.0 - u['rho']['eta']**2)*u['sd']**2)

    # Compute results
    rslt = scipy.stats.norm.cdf(eval_ - mean, 0.0, sd)

    # Finishing.
    return rslt  
