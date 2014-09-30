''' Construct parameter objects.
'''

# project library
from tools.economics.paras.clsParas import parasCls

def _constructParas(initDict):
    ''' Construct parametrization from model.cfg.
    '''
    # Algorithm.
    parasObj = parasCls()

    ''' ENVIRONMENT
    '''
    for key_ in ['subsidy', 'cost', 'discount']:
        
        value = initDict['ENVIRO'][key_]
        
        parasObj.addParameter('ENVIRO', key_, value)
        
    ''' UTILITY
    '''
    # Special treatment of children.
    value  = initDict['UTILITY']['child']['value'][0]
    
    isFree = initDict['UTILITY']['child']['free'][0] 
    
    parasObj.addParameter('CHILD', None, value, isFree)
    
    for subtype in ['coeffs', 'int']:
        
        values = initDict['UTILITY'][subtype]['value']
        
        isFree = initDict['UTILITY'][subtype]['free'] 
        
        count  = 0
        
        for value in values:
    
            parasObj.addParameter('UTILITY', subtype, value, isFree[count])
            
            count = count + 1
    
    ''' WAGE
    '''
    # Special treatment of experience.
    value  = initDict['WAGE']['exper']['value'][0]
    
    isFree = initDict['WAGE']['exper']['free'][0] 
        
    parasObj.addParameter('EXPERIENCE', None, value, isFree)
    
    for subtype in ['coeffs', 'int']:
        
        values = initDict['WAGE'][subtype]['value']
        
        isFree = initDict['WAGE'][subtype]['free'] 
        
        count  = 0
        
        for value in values:

            parasObj.addParameter('WAGE', subtype, value, isFree[count])
            
            count = count + 1

    ''' SHOCKS
    '''
    for subtype in ['eps', 'eta', 'rho']:

        value  = initDict['SHOCKS'][subtype]['value']
    
        isFree = initDict['SHOCKS'][subtype]['free'] 
        
        parasObj.addParameter('SHOCK', subtype, value, isFree)
     
       
    parasObj.lock()
    
    # Finishing.
    return parasObj