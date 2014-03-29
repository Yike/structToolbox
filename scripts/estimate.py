#!/usr/bin/env python
''' Estimation script
'''
# standard library
import cPickle as pkl
import numpy   as np

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
def estimate(initFile = 'init.ini', update = False, dataFile = 'obsEconomy.pkl'):
    ''' Run estimation. 
    '''
    # Antibugging.
    assert (isinstance(initFile, str))
    assert (isinstance(dataFile, str))
    
    assert (os.path.exists(initFile))
    assert (os.path.exists(dataFile))
    
    assert (update in [True, False])
        
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

    derived      = initDict['DERIV']

    ''' Update.
    '''
    if(update):
        
        values = np.genfromtxt(open('stepParas.struct.out', 'r'))
        
        parasObj.update(values, 'internal', 'all')
    
    ''' Construct request.
    ''' 
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
    
    update   = args.update
    
    dataFile = args.dataFile
    
    # Assertions.
    for file_ in [initFile, dataFile]:

        assert (file_ is not None)
        assert (os.path.exists(file_))
    
    assert (update in [False, True])
    
    if(update): assert (os.path.exists('stepParas.struct.out'))
    
    # Finishing.
    return initFile, update, dataFile

def fork():
    ''' Fork child process to run estimation in the background.
    '''
        
    pid = os.fork()

    if(pid > 0): sys.exit(0)

    pid = os.getpid()
    
    np.savetxt('.pid', [pid], fmt ='%d')
    
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
      'Estimation run of the structToolbox.')

    parser.add_argument('--dataFile', \
                        action  = 'store', \
                        dest    = 'dataFile', \
                        default = 'obsEconomy.pkl', \
                        help    = 'Name of dataset.')
    
    parser.add_argument('--init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'Configuration for estimation.')
    
    parser.add_argument('--update', \
                        action  = 'store_true', \
                        dest    = 'update', \
                        default = False, \
                        help    = 'Update parameter class.')
    
    fork() 
     
    initFile, update, dataFile = _distributeInput(parser)
        
    estimate(initFile = initFile, update = update, dataFile = dataFile)