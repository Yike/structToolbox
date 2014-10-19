#!/usr/bin/env python
''' Simulation script.
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
 
# standard library
import pickle as pkl
import pandas as pd
import numpy  as np

import argparse
import shutil
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.auxiliary import readStep
from tools.auxiliary import writeStep

from tools.optimization.criterion.clsCrit import critCls

from tools.economics.interface  import agentCls
from tools.economics.interface  import economyCls

from tools.user.interface       import initCls

def simulate(update = False, observed = False, inform = False, source = None):
    ''' Simulation of agent population.
    '''
    # Antibugging.
    assert (os.path.exists('model.struct.ini'))
    assert (observed in [True, False])
    assert (update   in [True, False])
    assert (inform   in [True, False])
        
    ''' Process initialization file.
    '''
    initObj = initCls()
    
    initObj.read()
    
    initObj.lock()
    
    ''' Distribute information.
    '''
    initDict   = initObj.getAttr('initDict')
    
    numPeriods = initDict['SIM']['periods']
    
    numAgents  = initDict['SIM']['agents']
    
    seed       = initDict['SIM']['seed']
        
    allPos     = initDict['DERIV']['pos']
    
    parasObj   = initDict['PARAS']  
    
    treeObj    = initDict['TREE']      
    
    ''' Update parameter object.
    '''
    if(update):
        
        x = readStep('paras')

        parasObj.update(x, 'internal', 'all')
    
    
    ''' Simulate agent attributes.
    '''
    np.random.seed(seed)
    
    attrs = []
    
    
    if(source is not None):
        
        sourceAgents = _getSources(source, numAgents)
        
        for i in range(numAgents):
            
            attr = {}
            
            for key_ in ['experience', 'children', 'utility', \
                             'spouse', 'wage']:
                    
                attr[key_] = sourceAgents[i].getAttr('attr')[key_]
            
            attrs = attrs + [attr]
            
    else:
        
        for _ in range(numAgents):
        
            attr, values = {}, {}
       
            for t in range(numPeriods):
                
                values[t] = {}
                
                for j in allPos:
                    
                    values[t][j] = np.random.rand()
            
            # Spouse.
            attr['spouse'] = _constructSpouse(numPeriods)
    
            # Children.
            pos = initDict['UTILITY']['child']['pos']
        
            attr['children'] = _constructChildren(numPeriods)
            
            # Experience.
            pos = initDict['WAGE']['exper']['pos']
        
            attr['experience'] = [0.0]
                        
            # Utility.
            attr['utility'] = []
        
            list_ = initDict['UTILITY']['coeffs']['pos']
            
            for t in range(numPeriods):
            
                cand =  []
    
                for pos in list_:
                    
                    cand = cand + [values[t][pos]]
                
                attr['utility'] = attr['utility'] + [cand]    
            
            # Wage.
            attr['wage'] = []
            
            list_ = initDict['WAGE']['coeffs']['pos']
            
            for t in range(numPeriods):
            
                cand =  []
    
                for pos in list_:
                    
                    cand = cand + [values[t][pos]]
                
                attr['wage'] = attr['wage'] + [cand]    
    
            attrs = attrs + [attr]
        
        
    # Initialize agents.
    agentObjs = []
    
    for attr in attrs:
        
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
    
    
    ''' Storage.
    '''
    if(inform):
    
        return economyObj
    
    else:
        
        economyObj.store('simEconomy.struct.pkl')
        
        _writeInfo(economyObj, parasObj)
    
        if(observed): _writeData(economyObj, initDict)
        
''' Auxiliary functions.
'''
def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    update   = args.update
    
    observed = args.observed
    
    source   = args.source
    
    # Assertions.
    assert (os.path.exists('model.struct.ini'))
    assert (update in [False, True])
    assert (observed in [True, False])
    
    if(source is not None): 
        
        assert (os.path.exists(source))
    
    # Finishing.
    return update, observed, source

def _getSources(source, numAgents):
    ''' Get sourced agents.
    '''
    # Antibugging.
    assert (os.path.exists(source))
    assert (isinstance(numAgents, int))
    assert (numAgents > 0)
        
    # Load sources.
    sourceEconomy = pkl.load(open(source))
        
    sourceAgents  = sourceEconomy.getAttr('agentObjs')

    numSources    = sourceEconomy.getAttr('numAgents')    
    
    # Sampling.
    replace = False
        
    if(numAgents > numSources): replace = True
        
    sourceAgents = np.random.choice(sourceAgents, size = numAgents, \
                        replace = replace)
            
    # Finishing.
    return sourceAgents
        
def _constructSpouse(numPeriods):
    ''' Construct a history of spouse income.
    '''
    # Initialize auxiliary objects.
    list_ = []
    
    # Time path.
    for _ in range(numPeriods):
 
        spouse = np.random.sample()
        
        list_ += [spouse]
        
    # Finishing.
    return list_

def _constructChildren(numPeriods):
    ''' Construct a child history.
    '''
    # Initialize auxiliary objects.
    list_ = []
    
    # Initial endowment.
    int_ = np.random.randint(0, 10)
    
    # Time path.
    list_ += [int_]
    
    for _ in range(1, numPeriods):
        
        leav = np.random.randint(0, 1)
        
        cand = list_[-1] - leav
        
        cand = max(0, cand)
        
        list_ += [cand]
        
    # Finishing.
    return list_
    
def _writeData(obsEconomy, initDict):
    ''' Write out simulated economy to a text file.
    '''    
    # Distribute class attributes.
    numAgents  = obsEconomy.getAttr('numAgents')
    
    numPeriods = obsEconomy.getAttr('numPeriods')
    
    agentObjs  = obsEconomy.getAttr('agentObjs')
    
    # Auxiliary objects.
    max_ = np.max(initDict['DERIV']['pos']) 
    
    data = np.tile(np.nan, (numAgents*numPeriods, (max_ + 1)))

    # Fill array.
    count = 0
    
    for agentObj in agentObjs:
        
        for t in range(numPeriods):
            
            # Time periods.
            data[count, 0] = t + 1
            
            # Observed outcomes.
            for key_ in ['wage', 'choice']:
                
                pos = initDict['OBSERVED'][key_]
                
                data[count, pos] = agentObj.attr[key_ + 's'][t]
            
            # Deal with spouse income.
            list_ = initDict['OBSERVED']['spouse']
            
            data[count, list_] = agentObj.attr['attr']['spouse'][t]

            # Deal with children.            
            pos = initDict['UTILITY']['child']['pos']
            
            data[count, pos] = agentObj.attr['attr']['children'][t]
            
            # Deal with utility shifters
            list_ = initDict['UTILITY']['coeffs']['pos']
                    
            data[count, list_] = agentObj.attr['attr']['utility'][t]
            
            
            # Deal with wage shifters
            list_ = initDict['WAGE']['coeffs']['pos']
                    
            data[count, list_] = agentObj.attr['attr']['wage'][t]
            
                            
            pos = initDict['WAGE']['exper']['pos']
           
            data[count, pos] = agentObj.attr['attr']['experience'][t]
            
            
            count = count + 1
    
    # Write out.
    df   = pd.DataFrame(data)

    pos  = initDict['DERIV']['pos']   
    
    
    ints = [0]
    
    ints = ints + initDict['WAGE']['exper']['pos']
    
    ints = ints + initDict['UTILITY']['child']['pos']
    
    ints = ints + [initDict['OBSERVED']['choice']]
    
    formats = {}
    
    for idx in range(max(pos)):
        
        formats[idx] = _formatFloat
        
        if(idx in ints): formats[idx] = _formatInteger
        
        
    with open('simEconomy.struct.txt', 'w', newline = '') as file_:
        
        df.to_string(file_, index = False, header = None, na_rep = '.', formatters=formats)

def _formatFloat(x):
    ''' Format floating point number.
    '''
    if pd.isnull(x):
    
        return '    .'
    
    else:
        
        return "%15.8f" % x
        
def _formatInteger(x):
    ''' Format integers.
    '''
    if pd.isnull(x):
    
        return '    .'
    
    else:
        
        return "%5d" % x
            
def _writeInfo(obsEconomy, parasObj):
    ''' Write some info about the simulated economy to a text file.
    '''
    

    
    # Criterion class.
    derived = {}
    
    derived['static'] = False
    
    
    critObj = critCls()
    
    critObj.setAttr('parasObj', parasObj)
    
    critObj.setAttr('obsEconomy', obsEconomy)

    critObj.setAttr('derived', derived)
    
    critObj.lock()
    
    # Document choices.
    numPeriods = str(obsEconomy.getAttr('numPeriods'))
    
    numAgents  = str(obsEconomy.getAttr('numAgents'))
    
    fval       = str(critObj._sampleLikelihood(parasObj))

    # Write parameters.
    x = parasObj.getValues('internal', 'all')

    writeStep(x, fval, count = '---', pkl_ = False)
    
    shutil.move('stepInfo.struct.out', 'simEconomy.paras.struct.out')
    
    
    with open('simEconomy.infos.struct.out', 'w') as file_:
        
        file_.write('\n Simulated Economy\n\n')
        
        file_.write('   Number of Observations: ' + numAgents + '\n\n')

        file_.write('   Number of Periods:      ' + numPeriods + '\n\n')  

        file_.write('   Function Value:         ' + fval + '\n\n\n')  
            
        file_.write('   Choices:  \n\n') 

        file_.write('       Period     Working      Home      \n\n')
        
        for t in range(obsEconomy.getAttr('numPeriods')):
            
            working = str(np.sum(obsEconomy.getAttr('choices')[t] == 1))

            home    = str(np.sum(obsEconomy.getAttr('choices')[t] == 0))
            
            string  = '''{0[0]:>10} {0[1]:>12} {0[2]:>10}\n'''
            
            file_.write(string.format([(t + 1), working, home]))
        
        file_.write('\n\n')
        
''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
        'Simulation of an economy for the structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--update', \
                        action  = 'store_true', \
                        dest    = 'update', \
                        default = False, \
                        help    = 'update structural parameters')

    parser.add_argument('--observed', \
                        action  = 'store_true', \
                        dest    = 'observed', \
                        default = False, \
                        help    = 'write out *.txt file')

    parser.add_argument('--source', \
                        action  = 'store', \
                        dest    = 'source', \
                        default = None, \
                        help    = 'source file for agent attributes')
    
    update, observed, source = _distributeInput(parser)
    
    simulate(update = update, observed = observed, source = source)
