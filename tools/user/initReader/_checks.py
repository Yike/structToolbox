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
    
    
    ''' Check observed outcomes.
    '''
    dict_ = initDict['OBSERVED']
    
    for key_ in ['wage', 'choice', 'spouse']:
        
        assert (isinstance(dict_[key_], int ))
        assert (dict_[key_] > 0) 
    
    ''' Experience present.
    '''
    assert (len(initDict['WAGE']['exper']['pos']) > 0)

    assert (len(initDict['UTILITY']['child']['pos']) > 0)
        
    ''' There is at least one free parameter.
    '''
    isFree = []
    
    for shock in ['eps', 'eta', 'rho']:
    
        isFree = isFree + [initDict['SHOCKS'][shock]['free']]
    
    for type_ in ['UTILITY', 'WAGE']:
    
        subtypes = ['coeffs', 'int']


        if(type_ == 'UTILITY'): subtypes = subtypes + ['child']

        if(type_ == 'WAGE'):    subtypes = subtypes + ['exper']
        
        
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