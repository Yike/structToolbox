#!/usr/bin/env python
''' Simulation script.
'''
# standard library
import numpy  as np
import pandas as pd

import argparse
import sys
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
import tools.computation.performance.performance as perf

from tools.user.interface        import *

from tools.economics.interface   import *

def process(data, initFile = 'init.ini'):
    ''' Process of agent population.
    '''
    # Antibugging.
    assert (isinstance(initFile, str))    
    assert (os.path.exists(initFile))

    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read(initFile)
    
    initObj.lock()
    
    ''' Distribute information.
    '''
    initDict = initObj.getAttr('initDict')
    
    seed     = initDict['SIM']['seed']
    
    parasObj = initDict['PARAS']  
    
    treeObj  = initDict['TREE']      
    
    ''' Process dataset.
    '''
    df = pd.read_csv(data,  header = -1, delim_whitespace = True)
    
    df = df.drop(0, axis = 1)
    
    ''' Get information.
    '''
    numAgents, numPeriods = getSize(df)
        
    ''' Simulate agent population.
    '''
    np.random.seed(seed)
    
    agentObjs = []
   
    row = 0
   
    for _ in range(numAgents):
        
        ''' Initialize attributes.
        '''
        attr = initializeDictionary(numPeriods)
        

        t = 0
        
        while True:
        
            ''' Preference and wage shifters.
            '''
            pos = initDict['UTILITY']['coeffs']['pos']
                
            attr['utility'][t] = list(df.iloc[row, pos])
        
        
            pos = initDict['WAGE']['coeffs']['pos']
                
            attr['wage'][t] = list(df.iloc[row, pos])
        
            
            ''' Children.
            '''
            pos = initDict['UTILITY']['child']['pos']
            
            attr['children'] += list(df.iloc[row, pos])
            
            ''' Spouse.
            '''
            pos = initDict['OBSERVED']['spouse']
            
            attr['spouse'] += list(df.iloc[row, pos])   


            ''' Endogenous
            '''
            # Experience.
            pos = initDict['WAGE']['exper']['pos']
        
            attr['experience'] += list(df.iloc[row, pos])

            # Wage.
            pos  = initDict['OBSERVED']['wage']

            wage = list(df.iloc[row, pos])[0]

            if(wage == '.'): 
                
                wage = np.nan
                
            else:
                
                wage = float(wage)
            
            attr['wages'] += [wage]
            
            # Choices.    
            pos  = initDict['OBSERVED']['choice']
    
            attr['choices'] += [int(df.iloc[row, pos])]
            
            
            # Update counts.
            t    = t + 1
            
            row  = row  + 1
            
            if(t == numPeriods): break
    

        agentObj = agentCls()
                
        agentObj.setAttr('attr', attr)
    
        agentObj.setAttr('parasObj', parasObj)

        agentObj.setAttr('treeObj', treeObj)
                
        agentObj.lock()
        
        ''' Add histories.
        '''
        agentObj.attr['choices'] = attr['choices']
        
        agentObj.attr['wages']   = attr['wages']
        
        agentObj.attr['states']  = constructStates(attr)
        
        # Collect agents.
        agentObjs = agentObjs + [agentObj]
  
    ''' Initialize economy.
    '''
    economyObj = economyCls()
    
    economyObj.setAttr('parasObj', parasObj)
    
    economyObj.setAttr('agentObjs', agentObjs)
    
    economyObj.lock()
    
    ''' Store.
    '''
    file_ = data[:data.rfind('.')] + '.pkl'
    
    economyObj.store(file_)

''' Auxiliary functions.
'''
def initializeDictionary(numPeriods):
    ''' Initialize dictionary for attributes.
    '''
    attr = {}
        
    for key_ in ['experience', 'children', 'spouse', \
                 'choices', 'wages']:
            
        attr[key_] = []        
        
    for key_ in ['wage', 'utility']:

        attr[key_] = {}
            
        for t in range(numPeriods):
                
            attr[key_][t] = []
            
    # Finishing.
    return attr
           
def constructStates(attr):
    ''' Construct state history based on agent decisions.
    '''
    # Construct auxiliary objects.
    numPeriods = len(attr['choices'])
    
    # Initialize and extend.
    states = ['0']
        
    for i in range(numPeriods):
        
        state = states[-1] + str(attr['choices'][i])
        
        states += [state] 
    
    # Finishing.
    return states
    
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    initFile = args.init 
    
    data     = args.data
    
    # Assertions.
    assert (initFile is not None)
    assert (os.path.exists(initFile))

    assert (data is not None)
    assert (os.path.exists(data))
        
    # Finishing.
    return initFile, data

def getSize(df):
    ''' Get agent count.
    '''
    # Antibugging.
    assert (isinstance(df, pd.DataFrame))

    # Number of periods.
    numPeriods, i = 1, 1
        
    while True:
        
        next_ = (df.iloc[i, 0] == 1.0)
        
        i     = i + 1
    
        if(next_): break
        
        numPeriods = numPeriods + 1

    # Number of agents. 
    numRows   = df.shape[0]
        
    numAgents = numRows/numPeriods
        
    remainder = numRows%numPeriods
        
    # Quality check.
    assert (remainder == 0)
    assert (isinstance(numAgents, int))
    assert (numAgents > 0)

    # Finishing.
    return numAgents, numPeriods

''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
        'Processing of a dataset into an economy object for the structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--init', \
                        action  = 'store', \
                        dest    = 'init', \
                        default = 'init.ini', \
                        help    = 'specify initialization file')

    parser.add_argument('--data', \
                        action  = 'store', \
                        dest    = 'data', \
                        required = True, \
                        help    = 'source file for processing')
    
    initFile, data = _distributeInput(parser)
    
    process(initFile = initFile, data = data)