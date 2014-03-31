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
from scripts.simulate             import simulate
from scripts.estimate             import estimate

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)


''' Auxiliary functions.
'''
def _checkEnvironment():
    ''' Check for parallel and 
    '''
    
    mpi4py = True
    
    try:
                    
        import mpi4py
                
    except ImportError:
                    
        mpi4py = False
        

    fortran = True
    
    try:
                    
        import tools.computation.f90.f90_main as fort 
                
    except ImportError:
                    
        fortran = False
        
    # Finishing.
    return mpi4py, fortran

class testCls(object):
    
    def test_case_1(self):
        
        mpi4py, fortran = _checkEnvironment()

        if(not (mpi4py)):  return
                
        if(not (fortran)): return
        
        
                    
        simulate(initFile = '../dat/testF_parallel_function.ini', dataFile = 'obsEconomy.pkl')

        for file_ in ['testF_parallel_function.ini', 'testF_parallel_gradient.ini', \
                            'testF_parallel_function_accelerated.ini', \
                            'testF_parallel_gradient_accelerated.ini']:        
                    
            estimate(initFile = '../dat/' + file_, dataFile = 'obsEconomy.pkl')
            
            rslt = pkl.load(open('rslt.struct.pkl', 'r'))
   
            assert_true(np.allclose(rslt['fun'], 2.37085576774) == True)     
        
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
