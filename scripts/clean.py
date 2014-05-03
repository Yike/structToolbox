#!/usr/bin/env python
''' Cleanup.
'''

# Check for appropriate Python version.
import sys

assert (sys.version_info[:2] == (2,7)), \
'''\n\n This release of the structToolbox is targeted towards Python 2.7.x,
 we will update to Python 3.x.x in our next iteration. Please change
 your default Python Interpreter accordingly.\n'''

# standard library.
import os
import glob
import argparse

''' Main function.
'''
def clean(resume = False):
    ''' Cleanup after estimation run.
    '''
    # Potential files.
    fileList  = glob.glob('*.struct.*')
    
    fileList += glob.glob('.struct.pid')
   
    # Ensure resume.
    if(resume):
        
        try:      
            
            fileList.remove('stepParas.struct.out')
        
        except:
            
            pass
    # Remove information from simulated data.
    for file_ in ['*.infos.struct.out', '*.paras.struct.out']:
                        
        try:
            
            fileList.remove(glob.glob(file_)[0])
            
        except:
            
            pass
        
    # Remove files.
    for file_ in fileList:
            
        os.remove(file_)
         
''' Auxiliary functions.
'''
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    resume = args.resume 

    # Assertions.
    assert (resume in [True, False])
    
    # Finishing.
    return resume

''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
        'Cleanup after an estimation run of the structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--resume', \
                        action  = 'store_true', \
                        dest    = 'resume', \
                        default = False, \
                        help    = 'keep files required to resume estimation')
    
    resume = _distributeInput(parser)
    
    clean(resume = resume)
    