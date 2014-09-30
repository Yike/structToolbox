#!/usr/bin/env python
''' Test cases that ensures that the static code yields the same result as the
    dynamic version in the special case of a 0.0 discount factor.
'''
# standard library
import numpy    as np
np.seterr('ignore')

import pickle  as pkl

import shutil
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
from tools.auxiliary                import readStep

from scripts.simulate               import simulate

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)

class testCls(object):
    
    def test_case_1(self):
        
        shutil.copy('../dat/testB.ini', 'model.struct.ini')

        shutil.copy('../dat/optimizers.ini', 'optimizers.struct.ini')
                
        simulate()
        
        ''' Process initialization file.
        '''
        initObj = initCls()
        
        initObj.read()
        
        initObj.lock()
        
        ''' Distribute information.
        '''
        obsEconomy = pkl.load(open('simEconomy.struct.pkl', 'rb'))
        
        
        initDict = initObj.getAttr('initDict')
        
        optimization = initDict['OPT']
        
        parasObj     = initDict['PARAS']
        
        derived      = initDict['DERIV']
        
        fval         = None
        
        for static in [True, False]:
            
            
            derived['static'] = static
            
        
            requestObj = requestCls()
            
            requestObj.setAttr('parasObj', parasObj)
            
            requestObj.setAttr('obsEconomy', obsEconomy)
                        
            requestObj.setAttr('derived', derived)
            
            requestObj.setAttr('single', True)
            
            requestObj.setAttr('optimization', optimization)
            
            requestObj.lock()
            
            ''' Call optimization.
            '''
            optimize(requestObj)
            
            ''' Check results.
            ''' 
            rslt = readStep('fval') 

            if(fval is None): fval = rslt 
            
            assert_true(np.allclose(fval, -165.628510699) == True)
            
        os.remove('model.struct.ini')

        os.remove('optimizers.struct.ini')
            
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
