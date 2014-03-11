''' Module with some basic checks of the specification of the initialization
    file.
'''

# standard library
import os

def _checks(initDict):
    ''' Interface to check routines.
    '''
    
    _basics(initDict)
    
    _identification(initDict)


def _basics(initDict):
    ''' Check for basic syntax.
    '''
    
    ''' Restart material exists.
    '''
    isRestart = initDict['EST']['restart']

    if(isRestart): assert (os.path.exists('stepParas.struct.out') == True)
    
    ''' There is at least one free parameter.
    '''
    isFree = []
    
    for shock in ['eps', 'eta', 'rho']:
    
        isFree = isFree + [initDict['SHOCKS'][shock]['free']]
    
    for type_ in ['CHILD', 'UTILITY', 'WAGE']:
    
        subtypes = ['coeffs', 'int']
        
        if(type_ == 'CHILD'): subtypes = ['coeffs']
    
        for subtype in subtypes:
            
            isFree = isFree + initDict[type_][subtype]['free']
            
    assert (sum(isFree) > 0)
    
def _identification(initDict):
    ''' Check for identification.
    '''   
    
    ''' Ensure identification of variance in utility equation through 
        exclusions.
    '''
    isFree = initDict['SHOCKS']['eps']['free']
    
    if(isFree):
        
        pos = []
        
        wage    = pos + initDict['WAGE']['coeffs']['pos']
        
        utility = pos + initDict['UTILITY']['coeffs']['pos']
        
        check = set(wage).issubset(utility)
        
        assert (check == False) 