''' Module for the initialization of the options for all optimizers.
'''

# standard library
import shlex

''' Main
'''
def initializeOptions():
    ''' Initialize the optimization options.
    '''
    # Initialize container.
    optDict = {}
        
    with open('optimizers.struct.ini', 'r') as initFile:
            
        for line in initFile:
                
            currentLine = shlex.split(line)
                
            ''' Preprocessing.
            '''
            isEmpty, isKeyword = _processCases(currentLine)
                
            if(isEmpty):    
                    
                continue
               
            elif(isKeyword):  
                    
                keyword = currentLine[0]
                
                optDict[keyword] = {}
                
                continue
                
            if(keyword ==  'SCIPY-POWELL'):
                    
                optDict = _processScipyPowell(optDict, currentLine)

            if(keyword ==  'SCIPY-BFGS'):
                    
                optDict = _processScipyBfgs(optDict, currentLine)
    
    # Quality checks.
    _checks(optDict)
            
    # Finishing.
    return optDict
        
''' Private functions.
'''
def _processScipyBfgs(optDict, currentLine):
    '''Process DATA block.
    ''' 
    # Antibugging.
    assert (isinstance(optDict, dict))
    assert (isinstance(currentLine, list))
    assert (len(currentLine) == 2)
        
    # Process information.    
    keyword = currentLine[0]
    flag    = currentLine[1]
        
    # Special treatments.
    if(keyword in ['gtol', 'epsilon']):
            
        flag = float(flag)
        
    # Special treatment.
    if(keyword == 'maxiter'):
                            
        if(flag.upper() == 'NONE'):
                                
            flag = None
                                
        else:
                                
            flag = int(flag)
        
    # Construct dictionary.        
    optDict['SCIPY-BFGS'][keyword] = flag
            
    # Finishing.
    return optDict
    
def _processScipyPowell(optDict, currentLine):
    '''Process DATA block.
    ''' 
    # Antibugging.
    assert (isinstance(optDict, dict))
    assert (isinstance(currentLine, list))
    assert (len(currentLine) == 2)
        
    # Process information.    
    keyword = currentLine[0]
    flag    = currentLine[1]
        
    # Special treatments.
    if(keyword in ['xtol', 'ftol']):
            
        flag = float(flag)
        
    if(keyword in ['maxfun']):
        
        flag = int(flag)

    if(keyword == 'maxiter'):
                            
        if(flag.upper() == 'NONE'):
                                
            flag = None
                                
        else:
                                
            flag = int(flag)
            
    # Construct dictionary.        
    optDict['SCIPY-POWELL'][keyword] = flag
            
    # Finishing.
    return optDict
    
''' Auxiliary functions
'''
def _processCases(currentLine):
    ''' Process special cases of empty list and keywords.
    '''
    def _checkEmpty(currentLine):
        ''' Check whether the list is empty.
        '''
        # Antibugging.
        assert (isinstance(currentLine, list))
            
        # Evaluate list.
        isEmpty = (len(currentLine) == 0)
            
        # Check integrity.
        assert (isinstance(isEmpty, bool))
            
        # Finishing.
        return isEmpty
    
    def _checkKeyword(currentLine):
        ''' Check for keyword.
        '''
        # Antibugging.
        assert (isinstance(currentLine, list))
            
        # Evaluate list.
        isKeyword = False
            
        if(len(currentLine) > 0):
                
            isKeyword = (currentLine[0].isupper())
            
        # Check integrity.
        assert (isinstance(isKeyword, bool))
            
        # Finishing.
        return isKeyword
        
    ''' Main Function.
    '''
    # Antibugging.
    assert (isinstance(currentLine, list))
    
    # Determine indicators.
    isEmpty   = _checkEmpty(currentLine) 
    
    isKeyword = _checkKeyword(currentLine)
        
    # Finishing.
    return isEmpty, isKeyword

def _checks(optDict):
    ''' Check optimization dictionary.
    '''
    # Antibugging.
    assert (isinstance(optDict, dict))
    
    # Powell.
    if('SCIPY-POWELL' in optDict.keys()):
        
        opts   = optDict['SCIPY-POWELL']

        xtol   = opts['xtol']

        ftol   = opts['ftol']
        
        maxfun = opts['maxfun']
        
        # Checks.
        assert (isinstance(xtol, float))
        assert (xtol > 0)

        assert (isinstance(ftol, float))
        assert (ftol > 0)

        assert (isinstance(maxfun, int))
        assert (maxfun > 0)    
    
    # BFGS.
    if('SCIPY-BFGS' in optDict.keys()):
        
        opts    = optDict['SCIPY-BFGS']
        
        gtol    = opts['gtol']

        epsilon = opts['epsilon']
        
        # Checks.
        assert (isinstance(gtol, float))
        assert (gtol > 0)

        assert (isinstance(epsilon, float))
        assert (epsilon > 0)

    # Finishing.
    return True