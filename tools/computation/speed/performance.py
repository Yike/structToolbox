''' Module for performance enhancing functionality.
'''

# standard library
import numpy as np
import scipy.stats

''' Module initialization.
'''
isAccelerated = True
    
try:
                    
    import tools.computation.f90.f90_main as fort 
                
except ImportError:
                    
    isAccelerated = False


''' Replacements.
'''
nan      = np.nan

isfinite = np.isfinite

inf      = np.inf
    

random_multivariate_normal = np.random.multivariate_normal


if(isAccelerated):
    
    
    norm_pdf = fort.wrapper_norm_pdf
            
    norm_cdf = fort.wrapper_norm_cdf
            
    clip     = fort.wrapper_clip_value
        
    sqrt     = fort.wrapper_sqrt
    
    log      = fort.wrapper_log        
        
    dot      = fort.wrapper_dotproduct

else:
    
        
    norm_pdf = scipy.stats.norm.pdf
            
    norm_cdf = scipy.stats.norm.cdf
            
    clip     = np.clip
        
    sqrt     = np.sqrt

    log      = np.log        
        
    dot      = np.dot
        