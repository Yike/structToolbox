''' Auxiliary functions for the calculations of the MLE criterion functions.
'''


# standard library
import scipy.stats
from scipy.stats import norm


import numpy        as np

def cdfConditional_single(eval_, u, v, real):
    ''' Evaluate the cumulative distribution function of the conditional
        distribution of U given V = v.
    '''
    # Calculate ingredients.
    mean = u['mean'] + u['rho']['eta']*(u['sd']/v['sd'])*(real - v['mean'])
    
    sd   = np.sqrt((1.0 - u['rho']['eta']**2)*u['sd']**2)

    # Compute results
    rslt = norm.cdf(eval_ - mean, 0.0, sd)

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
    rslt = norm.cdf(eval_ - mean, 0.0, sd)

    # Finishing.
    return rslt  
