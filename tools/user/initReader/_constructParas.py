''' Construct parameter objects.
'''

# project library
from tools.economics.paras.clsParas import parasCls

def _constructParas(initDict):
    ''' Construct parametrization from model.cfg.
    '''
    # Algorithm.
    parasObj = parasCls()

    ''' BASICS
    '''
    for key_ in ['subsidy', 'cost', 'discount']:
        
        value = initDict['BASICS'][key_]
    
        parasObj.addParameter('BASICS', key_, value)
        
    ''' CHILDREN
    '''    
    value  = initDict['CHILD']['coeffs']['value'][0]
    
    isFree = initDict['CHILD']['coeffs']['free'][0] 
    
    parasObj.addParameter('CHILD', None, value, isFree)
    
    ''' UTILITY
    '''
    for subtype in ['coeffs', 'int']:
        
        values = initDict['UTILITY'][subtype]['value']
        
        isFree = initDict['UTILITY'][subtype]['free'] 
        
        count = 0
        
        for value in values:
    
            parasObj.addParameter('UTILITY', subtype, value, isFree[count])
            
            count = count + 1
    
    ''' WAGE
    '''
    for subtype in ['coeffs', 'int']:
        
        values = initDict['WAGE'][subtype]['value']
        
        isFree = initDict['WAGE'][subtype]['free'] 
        
        count = 0
        
        for value in values:
    
            parasObj.addParameter('WAGE', subtype, value, isFree[count])
            
            count = count + 1
    
    # Special treatment of experience.
    value  = initDict['WAGE']['exper']['value'][0]
    
    isFree = initDict['WAGE']['exper']['free'][0] 
        
    parasObj.addParameter('EXPERIENCE', None, value, isFree)
    
    ''' SHOCKS
    '''
    for subtype in ['eps', 'eta', 'rho']:

        value = initDict['SHOCKS'][subtype]['value']
    
        isFree = initDict['SHOCKS'][subtype]['free'] 
        
        parasObj.addParameter('SHOCK', subtype, value, isFree)
     
       
    parasObj.lock()
    
    # Finishing.
    return parasObj