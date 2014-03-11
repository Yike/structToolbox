''' Auxiliary functions for the processing of an initialization file.
'''


def _processLine(currentLine):
    ''' Process line for possible parameter restrictions
    '''
    # Antibugging.
    assert (isinstance(currentLine, str))
    
    # Process fixed parameters.
    isFixed = (currentLine[0] == '!')
    
    # Extract value.
    value = currentLine 
    
    if(isFixed): value = currentLine[1:]
    
    isFree = (isFixed == False)

    # Type conversion.
    value = float(value)

    # Quality checks.
    assert (isinstance(value, float))
    assert (isFree in [True, False])
    
    # Finishing.
    return value, isFree

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