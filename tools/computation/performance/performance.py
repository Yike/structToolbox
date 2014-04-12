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
import performance as perf
    
perf.nan      = np.nan

perf.isfinite = np.isfinite

perf.inf      = np.inf
    

perf.random_multivariate_normal = np.random.multivariate_normal


if(isAccelerated):
    
    
    perf.norm_pdf = fort.wrapper_norm_pdf
            
    perf.norm_cdf = fort.wrapper_norm_cdf
            
    perf.clip     = fort.wrapper_clip_value
        
    perf.sqrt     = fort.wrapper_sqrt
    
    perf.log      = fort.wrapper_log        
        
    perf.dot      = fort.wrapper_dotproduct

else:
    
        
    perf.norm_pdf = scipy.stats.norm.pdf
            
    perf.norm_cdf = scipy.stats.norm.cdf
            
    perf.clip     = np.clip
        
    perf.sqrt     = np.sqrt

    perf.log      = np.log        
        
    perf.dot      = np.dot
        