#!/usr/bin/env python
''' Test cases
'''
# standard library
import numpy    as np
import scipy

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

import tools.computation.f90.f90_main     as fort

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)

class testCls(object):
    
    def test_case_1(self):
        ''' Test dot product calculation.
        '''
        
        for _ in range(1000):


            dim = np.random.randint(1, 100)
        
            a   = np.random.randn(dim)
            
            b   = np.random.randn(dim)
            
            
            f90 = fort.wrapper_dotproduct(a, b)
            
            py  = np.dot(a,b)
            
            
            assert_true(np.allclose(f90, py) == True)
            
    def test_case_2(self):
        ''' Test dot product calculation.
        '''
        
        for _ in range(1000):
    
            eval_ = np.random.normal(scale = 10)
    
            mean  = np.random.normal(scale = 10)
    
            sd    = np.random.normal(scale = 10)**2
    
            
            f90   = fort.wrapper_norm_cdf(eval_, mean, sd)
            
            py    = scipy.stats.norm.cdf(eval_, mean, sd)
            
            
            assert_true(np.allclose(f90, py) == True)

    def test_case_3(self):
        ''' Test normal pdf calculation.
        '''
        
        for _ in range(1000):
    
            eval_ = np.random.normal(scale = 10)
    
            mean  = np.random.normal(scale = 10)
    
            sd    = np.random.normal(scale = 10)**2
    
            
            f90   = fort.wrapper_norm_pdf(eval_, mean, sd)
            
            py    = scipy.stats.norm.pdf(eval_, mean, sd)
            
            
            assert_true(np.allclose(f90, py) == True)
                        
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
