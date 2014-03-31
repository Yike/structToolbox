''' Module for performance enhancing functionality.
'''

# standard library
import numpy as np
import scipy

''' Mock functions.
'''
def dot():
    
    pass

def norm_cdf():
    
    pass

def norm_pdf():
    
    pass

def clip():
    
    pass

def sqrt():
    
    pass

def log():
    
    pass

def nan():
    
    pass

def isfinite():
    
    pass

''' Module initialization.
'''
def initialize(accelerated):

    import performance as perf
    
    perf.nan      = np.nan
        
    perf.isfinite = np.isfinite

    perf.inf      = np.inf
    

    perf.random_multivariate_normal = np.random.multivariate_normal


    if(accelerated):
        
        import tools.computation.f90.f90_main as fort 
    
    
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
        