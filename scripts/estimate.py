#!/usr/bin/env python
''' Estimation script
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
  
# standard library
import pickle as pkl

import argparse
import shutil
import glob
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.optimization.interface   import optimize
from tools.auxiliary                import readStep
from tools.user.interface           import *

''' Auxiliary functions.
'''
def cleanup(resume):
    ''' Remove results from previous estimation run. All other files
        are immediately overwritten.
    '''

    if(resume):
        
        pass
        
    else:
        
        dirs = glob.glob('.slave-*')

        for dir_ in dirs:
            
            shutil.rmtree(dir_)

def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    resume   = args.resume
    
    single   = args.single
    
    static   = args.static
    
    # Assertions.
    assert (single in [True, False])
    
    assert (resume in [False, True])

    assert (static in [False, True])
        
    if(resume): 
        
        assert (os.path.exists('stepInfo.struct.out'))
    
    else:
        
        assert (not os.path.exists('.aggregator.struct.out'))
    
    # Finishing.
    return resume, single, static

''' Main function.
'''
def estimate(resume = False, single = False, static = False):
    ''' Run estimation. 
    '''
    # Antibugging.
    assert (os.path.exists('model.struct.ini'))
    assert (resume in [True, False])
    assert (static in [True, False])
    
    cleanup(resume)
    
    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read()
    
    initObj.lock()
    
    
    ''' Distribute information.
    '''
    initDict = initObj.getAttr('initDict')
    
    
    optimization = initDict['OPT']
    
    estimation   = initDict['EST']
    
    parasObj     = initDict['PARAS']

    derived      = initDict['DERIV']


    file_        = initDict['EST']['file']
    
    if(static): derived['static'] = True
    
    ''' Load dataset.
    '''
    obsEconomy = pkl.load(open(file_, 'rb'))
    
    
    ''' Subset.
    '''
    numSubset = estimation['agents']
   
    obsEconomy.subset(numSubset)
    
    
    ''' Update.
    '''
    if(resume): 
        
        parasObj.update(readStep('paras'), 'internal', 'all')
    
    
    ''' Construct request.
    ''' 
    requestObj = requestCls()

    requestObj.setAttr('optimization', optimization)

    requestObj.setAttr('obsEconomy', obsEconomy)
    
    requestObj.setAttr('parasObj', parasObj)
    
    requestObj.setAttr('derived', derived)
    
    requestObj.setAttr('single', single)

    requestObj.lock()
    
    ''' Call optimization.
    '''
    optimize(requestObj)

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
        'Start of estimation run of the structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--resume', \
                        action  = 'store_true', \
                        dest    = 'resume', \
                        default = False, \
                        help    = 'resume estimation run')
    
    parser.add_argument('--single', \
                        action  = 'store_true', \
                        dest    = 'single', \
                        default = False, \
                        help    = 'single evaluation')

    parser.add_argument('--static', \
                        action  = 'store_true', \
                        dest    = 'static', \
                        default = False, \
                        help    = 'static model')
    
    resume, single, static = _distributeInput(parser)  
    
    estimate(resume = resume, single = single, static = static)