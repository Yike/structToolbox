#!/usr/bin/env python
''' Test cases
'''
# standard library
import numpy    as np
import cPickle  as pkl

import sys
import os

# testing library
from nose.core  import runmodule
from nose.tools import *
 
# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/tests', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface           import *
from tools.optimization.interface   import optimize

from scripts.simulation             import simulation
from scripts.estimation             import estimation

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)

class testCls(object):
    
    def test_case_1(self):
        
        simulation(initFile = '../dat/testE_scalar.ini', dataFile = 'obsEconomy.pkl')

        for file_ in ['testE_scalar.ini', 'testE_parallel.ini']:        

            estimation(initFile = '../dat/' + file_, dataFile = 'obsEconomy.pkl')
            
            rslt = pkl.load(open('rslt.struct.pkl', 'r'))
    
            assert_true(np.allclose(rslt['fun'], -0.58179596977255987) == True)
        
        
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
