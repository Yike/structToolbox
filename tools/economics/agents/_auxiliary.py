''' Module with auxiliary functions for the agent class.
'''
# standard library
import numpy as np

from scipy.stats import norm

''' Wrapper functions.
'''
def wrapper_norm_cdf(x, mean, sd):
    ''' Wrapper for normal cdf calculation.
    '''
        
    return norm.cdf(x, mean, sd)

def wrapper_norm_pdf(x, mean, sd):
    ''' Wrapper for normal pdf calculation.
    '''
        
    return norm.pdf(x, mean, sd)

def wrapper_dot_product(a,b):
    ''' Wrapper for dot product calculation.
    '''

    return np.dot(a, b)

def wrapper_clip_value(value, lowerBound, upperBound):
    ''' Wrapper to clip value.
    '''

    return np.clip(value, lowerBound, upperBound)