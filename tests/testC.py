#!/usr/bin/env python
''' Test cases
'''
# standard library
import numpy    as np
np.seterr('ignore')

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
        
        ''' Process initialization file.
        '''
        initObj = initCls()
        
        initObj.read('../dat/testB.ini')
                
        initObj.lock()
        
        ''' Distribute information.
        '''
        initDict = initObj.getAttr('initDict')
               
        parasObj     = initDict['PARAS']
            
        paraObjs     = parasObj.getAttr('paraObjs')


        for paraObj in paraObjs:
            
            value = paraObj.getAttr('value')
            
            if(paraObj.getAttr('rest')[0] in ['fixed']): continue
            
            ext   = parasObj._transformToExternal(paraObj, value)
            
            int_  = parasObj._transformToInternal(paraObj, ext)
            
            assert_almost_equal(value, int_)
                    
''' Execution of module as script.
'''
if __name__ == '__main__':
    
    runmodule()
