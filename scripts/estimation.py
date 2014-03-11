#!/usr/bin/env python
''' Estimation script
'''
# standard library
import cPickle as pkl

import argparse
import sys
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface           import *

from tools.optimization.interface   import optimize

''' Process initialization file.
'''
def estimation(initFile = 'init.ini', dataFile = 'obsEconomy.pkl'):
    ''' Run estimation. 
    '''
    # Antibugging.
    assert (isinstance(initFile, str))
    assert (isinstance(dataFile, str))    
    
    assert (os.path.exists(initFile))
    assert (os.path.exists(dataFile))
        
    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read(initFile)
    
    initObj.lock()
    
    ''' Distribute information.
    '''
    obsEconomy = pkl.load(open(dataFile, 'r'))
    
    
    initDict = initObj.getAttr('initDict')
    
    optimization = initDict['OPT']
    
    estimation   = initDict['EST']
    
    parasObj     = initDict['PARAS']

    derived     = initDict['DERIV']

    
        
    requestObj = requestCls()
    
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
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    initFile = args.init 
    
    # Assertions.
    assert (initFile is not None)
    assert (os.path.exists(initFile))
    
    # Finishing.
    return initFile

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
      'Estimation run of the structToolbox.')

    parser.add_argument('-init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'Configuration for estimation.')
    
    initFile = _distributeInput(parser)
        
    estimation(initFile = initFile)