''' Logging capabilities for the progress of the SciPy algorithms.
'''

# standard library
import numpy as np

''' Main function.
'''
def logging(scipyObj, isFinal):
    ''' Function for logging of SciPy algorithms.
    '''
    # Antibugging.
    assert (scipyObj.getStatus() == True)
    assert (isFinal in [True, False])
    
    # Distribute class attributes.
    rslt = scipyObj.attr['fval']['current']

    # Determine events.
    isStart = (scipyObj.attr['fval']['start'] is None)
 
    isStep  = (rslt < scipyObj.attr['fval']['step'])
 
    # Log progress.
    if(isStart or isStep):

        parasObj = scipyObj.attr['parasObj']
                
        x = parasObj.getValues('internal', 'all')
        
        scipyObj.attr['paras']['step'] = x
        
        np.savetxt('stepParas.struct.out', x, fmt = '%15.10f')
         
    # Initialize start.
    if(isStart):
            
        scipyObj.attr['fval']['start'] = rslt

        scipyObj.attr['fval']['step']  = rslt            


        _writeOptimizationHeader(scipyObj)


        file_ = open('optimization.struct.log', 'a')
                                    
        file_.write('''\n Start \n\n   Value: ''' + str(rslt) + '\n\n')
            
        file_.close()
        
        
        np.savetxt('startParas.struct.out', x, fmt = '%15.10f')
            
    # Document progress.
    if(isStep):
                
        scipyObj.attr['fval']['step'] = rslt
        
        scipyObj.attr['step']         = scipyObj.attr['step'] + 1
        
        
        file_ = open('optimization.struct.log', 'a')
                        
        file_.write('''\n\n Step ''' + str(scipyObj.attr['step']) + '''\n\n   Value: ''' + str(rslt) + '\n')
        
        file_.close()
    
    # Finalize output.
    if(isFinal):
        
        rslt = scipyObj.attr['rslt']
                  
        success = str(rslt['success'])

        msg     = rslt['message']
        
        fval    = str(scipyObj.attr['fval']['step'])
        
        file_ = open('optimization.struct.log', 'a')

        file_.write('''\n\n\n Optimization Report \n''')        
        file_.write('''\n      Final:   ''' + fval)
        file_.write('''\n      Success: ''' + success)
        file_.write('''\n      Message: ''' + msg + '\n\n\n\n')
            
        file_.close()
                  
''' Private functions.
'''
def _writeOptimizationHeader(scipyObj):
    ''' Write information on applied optimization algorithm.
    ''' 
    # Antibugging.
    assert (scipyObj.getStatus() == True)
    
    # Distribute class attributes.
    numAgents = str(scipyObj.attr['numAgents'])

    algorithm = scipyObj.attr['optimization']['optimizer']
        
    optsDict  = scipyObj.attr['optsDict']
    
    if(algorithm == 'POWELL'):
 
        xtol   = str('{:15.7f}'.format(optsDict['SCIPY-POWELL']['xtol']))
            
        ftol   = str('{:15.7f}'.format(optsDict['SCIPY-POWELL']['ftol']))
            
    if(algorithm == 'BFGS'):
 
        gtol = str('{:15.7f}'.format(optsDict['SCIPY-BFGS']['gtol']))
                
    # Write logging file.
    file_ = open('optimization.struct.log', 'w')
                
    file_.write('\n Optimization \n ------------ \n\n')
            
    file_.write(' Toolbox:     SciPy' + '\n' )

    file_.write(' Algorithm:   ' + algorithm + '\n\n')
        
    file_.write(' Agent Count: ' + numAgents + '\n\n')
        
    if(algorithm == 'POWELL'):
            
        file_.write(' xtol:   ' + xtol + '\n')

        file_.write(' ftol:   ' + ftol + '\n')
                                
    if(algorithm == 'BFGS'):
            
        file_.write(' gtol:    ' + gtol + '\n')
                    
    file_.close()

    