#!/usr/bin/env python
''' Cleanup.
'''

# standard library.
import os
import glob
import argparse

''' Auxiliary functions.
'''
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    isRestart = args.restart 

    # Assertions.
    assert (isRestart in [True, False])
    
    # Finishing.
    return isRestart

''' Process command line arguments.
'''
parser = argparse.ArgumentParser(description = 
'Cleanup for structEstimator.')

parser.add_argument('-restart', \
                    action  = 'store_true', \
                    dest    = 'restart', \
                    default = False, \
                    help    = 'Keep restart information.')

isRestart = _distributeInput(parser)
        
# Potential files.
fileList = glob.glob('*.struct.*')
    
# Ensure restart.
if(isRestart):
    
    try:      
        
        fileList.remove('stepParas.struct.out')
    
    except:
        
        pass
# Remove files.
for file_ in fileList:
        
    os.remove(file_)
     