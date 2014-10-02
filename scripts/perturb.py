#!/usr/bin/env python
''' Perturb starting parameter values.
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
 
# standard library
import numpy   as np

import os
import argparse

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.auxiliary        import readStep
from tools.auxiliary        import writeStep
from tools.user.interface   import *

''' Main function.
'''
def perturb(scale = 0.1, seed = 123, update = False):
    ''' Perturb current values of structural parameters.
    '''
    ''' Obtain starting values.
    '''
    initObj = initCls()
        
    initObj.read()
        
    initObj.lock()
    
    ''' Distribute attributes.
    '''
    initDict = initObj.getAttr('initDict')
    
    parasObj = initDict['PARAS']
    
    ''' Update parameter object.
    '''
    if(update):

        # Antibugging.
        assert (os.path.isfile('stepInfo.struct.out'))
        
        values = readStep('paras')
        
        # Update parameter objects.
        parasObj.update(values, 'internal', 'all')
        
    ''' Perturb external values.
    '''
    np.random.seed(seed)
    
    baseValues = parasObj.getValues('external', 'free')
    
    perturb    = (np.random.sample(len(baseValues)) - 0.5)*scale
    
    evalPoints = baseValues + perturb
    
    ''' Transform evaluation points.
    '''
    parasObj.update(evalPoints, 'external', 'free')
    
    evalPoints = parasObj.getValues('internal', 'all')
    
    ''' Finishing.
    '''
    writeStep(evalPoints, fval = '---', count = 0)
    
''' Auxiliary function.
'''
def process(args):
    ''' Process arguments.
    '''
    # Distribute arguments.
    seed, scale, update = args.seed, args.scale, args.update
    
    # Quality checks.
    assert (update in [True, False])
    assert (os.path.exists('model.struct.ini'))
    assert (isinstance(seed, int))
    assert (isinstance(scale, float))
    assert (scale >= 0)
    
    # Finishing.
    return seed, scale, update

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser  = argparse.ArgumentParser(description = \
        'Perturb current value of structural parameters for structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument('--seed', \
                        type    = int , \
                        default = 123, \
                        dest    = 'seed', \
                        help    = 'value of random seed')
    
    parser.add_argument('--scale', \
                        type    = float , \
                        default = 0.1, \
                        dest    = 'scale', \
                        help    = 'magnitude of perturbation')

    parser.add_argument('--update', \
                        action  = 'store_true', \
                        dest    = 'update', \
                        default = False, \
                        help    = 'update structural parameter')
    
    args = parser.parse_args()
    
    seed, scale, update = process(args)
    
    perturb(scale = scale, seed = seed, update = update)