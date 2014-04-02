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
from scripts.simulate               import simulate

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)

class testCls(object):
    
    def test_case_1(self):
        
        simulate(initFile = '../dat/testC.ini')
        
        ''' Process initialization file.
        '''
        initObj = initCls()
        
        initObj.read('../dat/testC.ini')
        
        initObj.lock()
        
        ''' Distribute information.
        '''
        obsEconomy = pkl.load(open('testC.pkl', 'r'))
        
        
        initDict = initObj.getAttr('initDict')
        
        optimization = initDict['OPT']
        
        parasObj     = initDict['PARAS']
        
        estimation   = initDict['EST']
        
        derived      = initDict['DERIV']
            
        for static in [True, False]:
            
            
            derived['static'] = static
            
        
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
                
            rslt = pkl.load(open('rslt.struct.pkl', 'r'))
   
            assert_true(np.allclose(rslt['fun'], -0.579814883656) == True)
            
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
