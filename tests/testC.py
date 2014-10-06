#!/usr/bin/env python
''' Test cases that ensures that the transformations between internal
    and external parameter values are correct and can be reversed.
'''
# standard library
import numpy    as np
np.seterr('ignore')

import shutil
import glob
import sys
import os

# module variables
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_PATH = os.getcwd()

# testing library
from nose.core  import runmodule
from nose.tools import *
 
# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/tests', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface import *

# Set working directory.
dir_ = os.path.abspath(os.path.split(sys.argv[0])[0])
os.chdir(dir_)

''' Auxiliary functions.
'''
def cleanup():

    files = []

    files = files + ['model.struct.ini']

    files = files + ['optimizers.struct.ini']

    for file_ in files:

        try:

            os.remove(file_)

        except OSError:

            pass

''' Test class.
'''
class testCls(object):

    def setup(self):

        os.chdir(FILE_PATH)

    def teardown(self):

        cleanup()

        os.chdir(TEST_PATH)

    def test_case_1(self):

        shutil.copy('../dat/testB.ini', 'model.struct.ini')

        shutil.copy('../dat/optimizers.ini', 'optimizers.struct.ini')
        
        ''' Process initialization file.
        '''
        initObj = initCls()
        
        initObj.read()
                
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
