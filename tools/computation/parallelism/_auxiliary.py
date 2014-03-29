''' Auxiliary script for the MPI communication.
'''
# standard library
import math
import itertools

def splitList(list_, numBins):
    ''' Split a list in bins and returns a nested list.
    '''
    # Antibugging.
    assert (isinstance(numBins, int))
    assert (isinstance(list_, list))
    
    assert (numBins > 0)
    assert (numBins <= len(list_))
    
    # Algorithm.
    incr = int(math.ceil(float(len(list_))/float(numBins)))
  
    # Quality check.
    splittedList = []
    
    lower = 0
    upper = incr
    
    for _ in range(numBins):
         
        splittedList.append(list_[lower:upper])

        lower = upper
        upper = min(lower + incr, len(list_))
    
    # Quality checks.
    assert (list(itertools.chain(*splittedList)) == list_)
        
    # Finishing.
    return splittedList

