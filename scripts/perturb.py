#!/usr/bin/env python
''' Perturb starting parameter values.
'''
# standard library
import numpy   as np
import cPickle as pkl

import sys
import os
import argparse

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface           import *

''' Auxiliary function.
'''
def process(args):
    ''' Process arguments.
    '''
    # Distribute arguments.
    seed, scale = args.seed, args.scale
    
    # Quality checks.
    assert (isinstance(seed, int))
    assert (isinstance(scale, float))
    assert (scale >= 0)
    
    # Finishing.
    return seed, scale

''' Parsing Arguments.
'''
parser  = argparse.ArgumentParser(description = 'Perturb current value of structural parameters.')

parser.add_argument('-seed', \
                    type    = int , \
                    default = 123, \
                    dest    = 'seed', \
                    help    = 'Random Seed')

parser.add_argument('-scale', \
                    type    = float , \
                    default = 0.1, \
                    dest    = 'scale', \
                    help    = 'Scale')

args        = parser.parse_args()

seed, scale = process(args)

''' Obtain starting values.
'''
initObj = initCls()
    
initObj.read('init.ini')
    
initObj.lock()

''' Distribute attributes.
'''
initDict = initObj.getAttr('initDict')

parasObj = initDict['PARAS']

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