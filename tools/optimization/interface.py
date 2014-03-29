''' Interface to optimization algorithms.
'''
# standard library
import numpy as np

# project library
from tools.optimization.algorithms.clsAlgorithms    import algoCls

from tools.optimization.clsOptRequest               import optRequestCls

from tools.computation.performance.replacements     import replacements

from tools.computation.parallelism.clsComm          import commCls


def optimize(requestObj):
    ''' Function for optimization.
    '''
    # Antibugging
    assert (requestObj.getStatus() == True)

    ''' Distribute attributes.
    '''
    estimation   = requestObj.getAttr('estimation')

    optimization = requestObj.getAttr('optimization')

    obsEconomy   = requestObj.getAttr('obsEconomy')        

    derived      = requestObj.getAttr('derived')             
    
    # Further information.
    accelerated = estimation['accelerated']
    
    isRestart   = estimation['restart']
    
    numProcs    = estimation['processors']

    static      = derived['static']
    
    ''' Performance
    '''
    if(accelerated): replacements()
        
    ''' Parallelism
    '''
    commObj = None
    
    if(numProcs > 1):
        
        commObj = commCls()
        
        commObj.setAttr('numProcs', numProcs)
    
        commObj.lock()
        
        commObj.initialize()
    
    ''' Get starting values.
    '''
    parasObj = requestObj.getAttr('parasObj')
    
    
    if(isRestart):
        
        x = np.genfromtxt('stepParas.struct.out')
        
        parasObj.update(x, 'internal', 'all')
        
    
    startVals = parasObj.getValues('external', 'free')
    
    
    ''' Construct optimization request.
    '''
    optRequestObj = optRequestCls()

    optRequestObj.setAttr('userRequestObj', requestObj)
    
    optRequestObj.setAttr('optimization', optimization)

    optRequestObj.setAttr('startVals', startVals)

    optRequestObj.setAttr('commObj', commObj)
    
    optRequestObj.setAttr('obsEconomy', obsEconomy)
    
    optRequestObj.setAttr('parasObj', parasObj)

    optRequestObj.setAttr('static', static)
                
    optRequestObj.lock()
    

    ''' Run optimization.
    '''
    algoObj = algoCls()    
    
    algoObj.setAttr('requestObj', optRequestObj)
    
    algoObj.lock()
    
    
    algoObj.optimize()
    
    
    ''' Wrapping up.
    '''
    if(numProcs > 1): commObj.terminate()   