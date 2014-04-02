#!/usr/bin/env python
''' Perturb starting parameter values.
'''
# standard library
import numpy   as np

import sys
import os
import argparse

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface           import *

''' Main function.
'''
def perturb(scale = 0.1, seed = 123, init = 'init.ini', update = False):
    ''' Perturb current values of structural parameters.
    '''
    ''' Obtain starting values.
    '''
    initObj = initCls()
        
    initObj.read(init)
        
    initObj.lock()
    
    ''' Distribute attributes.
    '''
    initDict = initObj.getAttr('initDict')
    
    parasObj = initDict['PARAS']
    
    ''' Update parameter object.
    '''
    if(update):

        # Antibugging.
        assert (os.path.isfile('stepParas.struct.out'))
        
        values = np.array(np.genfromtxt('stepParas.struct.out'), dtype = 'float', ndmin = 1)
        
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
    np.savetxt('stepParas.struct.out',  evalPoints, fmt = '%15.10f')

''' Auxiliary function.
'''
def process(args):
    ''' Process arguments.
    '''
    # Distribute arguments.
    seed, scale, init, update = args.seed, args.scale, args.init, args.update
    
    # Quality checks.
    assert (update in [True, False])
    assert (os.path.exists(init))
    assert (isinstance(seed, int))
    assert (isinstance(scale, float))
    assert (scale >= 0)
    
    # Finishing.
    return seed, scale, init, update

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser  = argparse.ArgumentParser(description = \
                'Perturb current value of structural parameters.')
        
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
    
    parser.add_argument('--init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'source for model configuration')

    parser.add_argument('--update', \
                        action  = 'store_true', \
                        dest    = 'update', \
                        default = False, \
                        help    = 'update structural parameter')
    
    args = parser.parse_args()
    
    seed, scale, init, update = process(args)
    
    perturb(scale = scale, seed = seed, init = init, update = update)