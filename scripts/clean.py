#!/usr/bin/env python
''' Cleanup.
'''

# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''

# standard library.
import os
import glob
import shutil
import argparse

''' Main function.
'''
def clean(resume = False):
    ''' Cleanup after estimation run.
    '''
    # Potential files.
    fileList  = glob.glob('*.struct.*')
    
    # Ensure resume.
    if(resume):
        
        try:      
            
            fileList.remove('stepInfo.struct.out')
        
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
        
        if('ini' in file_): continue
        
        if('simEconomy' in file_): continue
        
        remove(file_)
    
    # Estimation directory.
    dirs = glob.glob('.slave-*')
    
    for dir_ in dirs:
        
        os.chdir(dir_)

        isRunning = os.path.exists('.optimization.struct.out')
        
        os.chdir('../')

        if(not isRunning): shutil.rmtree(dir_)
    
''' Auxiliary functions.
'''
def remove(name):
    ''' Remove file or directory (if exists).
    '''
    
    try:
        
        os.remove(name)
        
    except OSError:
        
        pass
    
    try:
        
        shutil.rmtree(name)
        
    except OSError:
        
        pass
        
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
    