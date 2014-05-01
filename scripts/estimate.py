#!/usr/bin/env python
''' Estimation script
'''
# standard library
import cPickle as pkl
import numpy   as np

import argparse
import sys
import os

# Check for appropriate version.
assert (sys.version_info[:2] == (2,7)), \
'''\n\n This release of the structToolbox is targeted towards Python 2.7.x,
 we will update to Python 3.x.x in our next iteration. Please change
 your default Python Interpreter accordingly.\n'''

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface           import *

from tools.optimization.interface   import optimize

''' Process initialization file.
'''
def estimate(initFile = 'init.ini', resume = False):
    ''' Run estimation. 
    '''
    # Antibugging.
    assert (isinstance(initFile, str))
    assert (os.path.exists(initFile))

    assert (resume in [True, False])
        
    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read(initFile)
    
    initObj.lock()
    
    ''' Distribute information.
    '''
    initDict = initObj.getAttr('initDict')
    
    
    optimization = initDict['OPT']
    
    estimation   = initDict['EST']
    
    parasObj     = initDict['PARAS']

    derived      = initDict['DERIV']


    file_        = initDict['EST']['file']
    
    ''' Load dataset.
    '''
    obsEconomy = pkl.load(open(file_ + '.pkl', 'r'))
    
    
    ''' Subset.
    '''
    numSubset = estimation['agents']
   
    obsEconomy.subset(numSubset)
    
    
    ''' Update.
    '''
    if(resume):
        
        values = np.genfromtxt(open('stepParas.struct.out', 'r'))
        
        parasObj.update(values, 'internal', 'all')
    
    ''' Construct request.
    ''' 
    requestObj = requestCls()

    requestObj.setAttr('init', initFile)
        
    requestObj.setAttr('parasObj', parasObj)
    
    requestObj.setAttr('obsEconomy', obsEconomy)
    
    requestObj.setAttr('estimation', estimation)

    requestObj.setAttr('derived', derived)
    
    requestObj.setAttr('optimization', optimization)

    requestObj.lock()
    
    ''' Call optimization.
    '''
    optimize(requestObj)

''' Auxiliary functions.
'''
def cleanup():
    ''' Remove results from previous estimation run. All other files
        are immediately overwritten.
    '''

    try:
        
        os.remove('rslt.struct.pkl')
        
    except OSError:
        
        pass
    
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    initFile = args.init 
    
    resume   = args.resume
    
    # Assertions.
    assert (initFile is not None)
    assert (os.path.exists(initFile))
    
    assert (resume in [False, True])
    
    if(resume): assert (os.path.exists('stepParas.struct.out'))
    
    # Finishing.
    return initFile, resume

def fork():
    ''' Fork child process to run estimation in the background.
    '''
        
    pid = os.fork()

    if(pid > 0): sys.exit(0)

    pid = os.getpid()
    
    np.savetxt('.struct.pid', [pid], fmt ='%d')
    
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
        'Start of estimation run of the structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'specify initialization file')
    
    parser.add_argument('--resume', \
                        action  = 'store_true', \
                        dest    = 'resume', \
                        default = False, \
                        help    = 'resume estimation run')
    
    cleanup()
    
    fork() 
     
    initFile, resume = _distributeInput(parser)
        
    estimate(initFile = initFile, resume = resume)