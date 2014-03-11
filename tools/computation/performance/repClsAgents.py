''' Performance enhancing replacements for instances of the agentCls.
'''

# project library
import tools.computation.f90.f90_main as fort 

def replacements(agentObjs):
    ''' Replacements
    '''

    # Replacements
    for agentObj in agentObjs:
    
        agentObj.wrapper_dot_product = fort.wrapper_dotproduct

        agentObj.wrapper_norm_cdf    = fort.wrapper_norm_cdf

        agentObj.wrapper_norm_pdf    = fort.wrapper_norm_pdf

        agentObj.wrapper_clip_value  = fort.wrapper_clip_value
        
    return agentObjs