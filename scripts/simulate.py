#!/usr/bin/env python
''' Simulation script.
'''
# standard library
import numpy as np

import argparse
import sys
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface        import *

from tools.economics.interface   import *

def simulate(initFile = 'init.ini', dataFile = 'obsEconomy.pkl', update = False):
    ''' Simulation of agent population.
    '''
    # Antibugging.
    assert (isinstance(initFile, str))
    assert (isinstance(dataFile, str))    
    
    assert (os.path.exists(initFile))
    
    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read(initFile)
    
    initObj.lock()
    
    
    ''' Distribute information.
    '''
    initDict = initObj.getAttr('initDict')
    
    
    numPeriods = initDict['BASICS']['periods']
    
    numAgents  = initDict['SIM']['agents']
    
    seed       = initDict['SIM']['seed']
    
    income     = initDict['SPOUSE']['income']
    
    allPos     = initDict['DERIV']['pos']
    
    parasObj   = initDict['PARAS']  
    
    treeObj    = initDict['TREE']      
    
    ''' Update parameter object.
    '''
    if(update):
        
        x = np.genfromtxt('stepParas.struct.out')
        
        parasObj.update(x, 'internal', 'all')
        
    ''' Simulate agent population.
    '''
    np.random.seed(seed)
    
    agentObjs = []
    
    for _ in range(numAgents):
        
        ''' Construct attributes.
        '''
        values, attr = {}, {}
        
        for i in allPos:
            
            values[i] = np.random.rand()
        
        # Special treatments.
        pos = initDict['UTILITY']['child']['pos']
        
        values[pos[0]] = np.random.randint(low = 0, high = 10)
                
        # Spouse.
        attr['spouse'] = income

        # Experience.
        pos = initDict['WAGE']['exper']['pos']
    
        attr['experience'] = [0.0]
                    
        # Children.
        pos = initDict['UTILITY']['child']['pos']
    
        attr['children'] = values[pos[0]]
        
        # Utility.
        attr['utility'] = []
    
        list_ = initDict['UTILITY']['coeffs']['pos']
        
        for pos in list_:
        
            attr['utility'] = attr['utility'] + [values[pos]]
        
        # Wage.
        attr['wage'] = []
        
        list_ = initDict['WAGE']['coeffs']['pos']
        
        for pos in list_:
        
            attr['wage'] = attr['wage'] + [values[pos]]
             
             
        agentObj = agentCls()
                
        agentObj.setAttr('attr', attr)
    
        agentObj.setAttr('parasObj', parasObj)

        agentObj.setAttr('treeObj', treeObj)
                
        agentObj.lock()
                    
        # Collect agents.
        agentObjs = agentObjs + [agentObj]
    
    
    ''' Initialize economy.
    '''
    economyObj = economyCls()
    
    economyObj.setAttr('parasObj', parasObj)
    
    economyObj.setAttr('agentObjs', agentObjs)
    
    economyObj.lock()
    
    
    ''' Simulate economy.
    '''
    for _ in range(numPeriods):
        
        economyObj.simulate()
    
    ''' Store.
    '''
    economyObj.store(dataFile)
    
    _writeInfo(economyObj, parasObj)

        
''' Auxiliary functions.
'''
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    initFile = args.init 
    
    update   = args.update
    
    # Assertions.
    assert (initFile is not None)
    assert (os.path.exists(initFile))
    assert (update in [False, True])
    
    # Finishing.
    return initFile, update

def _writeInfo(obsEconomy, parasObj):
    ''' Write some info about the simulated economy to a text file.
    '''
    
    # Write parameters.
    x = parasObj.getValues('internal', 'all')

    np.savetxt('simParas.struct.out', x, fmt = '%15.10f')
    
    # Document choices.
    numPeriods = str(obsEconomy.getAttr('numPeriods'))
    
    numAgents  = str(obsEconomy.getAttr('numAgents'))
    
    with open('simEconomy.struct.info', 'w') as file_:
        
        file_.write('\n Simulated Economy\n\n')
        
        file_.write('   Number of Observations: ' + numAgents + '\n\n')

        file_.write('   Number of Periods:      ' + numPeriods + '\n\n\n')  
    
        file_.write('   Choices:  \n\n') 

        file_.write('       Period     Working      Home      \n\n')
        
        for i in range(obsEconomy.getAttr('numPeriods')):
            
            working = str(np.sum(obsEconomy.getAttr('choices')[:,i] == 1))

            home    = str(np.sum(obsEconomy.getAttr('choices')[:,i] == 0))
            
            string  = '''{0[0]:>10} {0[1]:>12} {0[2]:>10}\n'''
            
            file_.write(string.format([i, working, home]))
        
        file_.write('\n\n')
        
''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
      'Simulation of economy for the structToolbox.')

    parser.add_argument('--init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'Configuration for simulation.')
    
    parser.add_argument('--update', \
                        action  = 'store_true', \
                        dest    = 'update', \
                        default = False, \
                        help    = 'Update parameter class.')


    initFile, update = _distributeInput(parser)
    
    simulate(initFile = initFile, update = update)