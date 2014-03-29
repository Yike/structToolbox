''' Performance enhancing replacements for instances of the agentCls.
'''

# standard library
import scipy
import numpy as np

def replacements():
    ''' Replacements
    '''
    import tools.computation.f90.f90_main as fort 
    
    scipy.stats.norm.pdf = fort.wrapper_norm_pdf
        
    scipy.stats.norm.cdf = fort.wrapper_norm_cdf
        
    np.dot               = fort.wrapper_dotproduct
        
    np.clip              = fort.wrapper_clip_value
    
    np.sqrt              = fort.wrapper_sqrt

    np.log               = fort.wrapper_log    
