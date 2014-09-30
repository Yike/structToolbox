''' Interface to optimization algorithms.
'''

# project library
from tools.optimization.optimizers.clsOptimization  import optimizationCls
from tools.optimization.criterion.clsCrit           import critCls

def optimize(requestObj):
    ''' Function for optimization.
    '''
    # Antibugging
    assert (requestObj.getStatus() == True)

    ''' Distribute attributes.
    '''
    optimization = requestObj.getAttr('optimization')

    obsEconomy   = requestObj.getAttr('obsEconomy')        

    derived      = requestObj.getAttr('derived')    

    single       = requestObj.getAttr('single')   
    
    ''' Get starting values.
    '''
    parasObj  = requestObj.getAttr('parasObj')

    startVals = parasObj.getValues('external', 'free')
    
        
    ''' Criterion function.
    '''
    critObj = critCls()
    
    critObj.setAttr('parasObj', parasObj)
    
    critObj.setAttr('obsEconomy', obsEconomy)

    critObj.setAttr('derived', derived)
    
    critObj.lock()


    ''' Optimization.
    '''
    optimizationObj = optimizationCls()    
    
    optimizationObj.setAttr('optimization', optimization)

    optimizationObj.setAttr('startVals', startVals)

    optimizationObj.setAttr('critObj', critObj)
    
    optimizationObj.setAttr('single', single)
                
    optimizationObj.lock()
   
   
    optimizationObj.optimize()
    
        