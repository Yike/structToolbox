#!/usr/bin/env python
''' Script to provide information about the economy at the current point of
    evaluation.
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
 
# standard library
import pickle as pkl
import numpy  as np

import argparse
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface import initCls
from scripts.simulate     import simulate
from tools.auxiliary      import readStep

''' Auxiliary functions.
'''
def _processRestriction(initDict, name, subtype = None, pos = None):
    ''' Process restrictions.
    '''
    
    if(name == 'child'):
        
        isFree = initDict['UTILITY']['child']['free'][0]
                
    if(name == 'experience'):
                 
        isFree = initDict['WAGE']['exper']['free'][pos]  

    if(name == 'utility'):
                 
        isFree = initDict['UTILITY'][subtype]['free'][pos]

    if(name == 'wage'):
                 
        isFree = initDict['WAGE'][subtype]['free'][pos]

    if(name == 'shocks'):
        
        isFree = initDict['SHOCKS'][subtype]['free']
        
    # Process.
    rest = ''
        
    if(not isFree): rest = '!'
    
    # Finishing.
    return rest

def _distributeInput(parser):
    ''' Check input for estimation script.
    '''
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    detailed = args.detailed 

    # Assertions.
    assert (detailed in [True, False])

    # Finishing.
    return detailed

def _getInfo(list_):
    ''' Calculate mean even if all 
    '''
    # Antibugging.
    assert (isinstance(list_, np.ndarray))
    
    # Auxiliary objects.
    isEmpty = (sum(np.isnan(list_)) == len(list_))

    # Construct mean.
    if(isEmpty):

        stat = '      ----'
        
    else:
                        
        stat = np.nanmean(list_)
        
        stat = '{:10.2f}'.format(stat)

    # Finishing.
    return stat

def _writeDescriptive(obsEconomy, simEconomy):
    ''' Write out the descriptives at the current point of evaluation.
    '''
    # Antibugging.
    assert (obsEconomy.getStatus() == True)
    assert (simEconomy.getStatus() == True)
    
    # Auxiliary objects.
    numPeriods = obsEconomy.getAttr('numPeriods')
        
    obsAgents  = obsEconomy.getAttr('numAgents')

    simAgents  = simEconomy.getAttr('numAgents')
    
    # Write to logging.
    with open('inform.struct.out', 'a') as file_:      
        
        ''' Model Fit
        '''
        file_.write('\n Model Fit\n --------- \n\n')

        # Basics.
        str_ = '   {0:<10}     {1:<15}\n'
            
        file_.write(str_.format('Observed', obsAgents))
            
        file_.write('\n')
            
        file_.write(str_.format('Simulated', simAgents))
    
        file_.write('\n\n')
                    
        # State probabilities.      
        file_.write('   Working \n\n')
            
        str_ = '     {0:<5}{1:10.2f}     {2:10.2f}\n'
        
        file_.write('   Period     Observed      Simulated \n\n')
            
        for t in range(numPeriods):
            
            obs = np.sum(obsEconomy.getAttr('choices')[t] == 1)/float(obsAgents)
                            
            sim = np.sum(simEconomy.getAttr('choices')[t] == 1)/float(simAgents)
                
            file_.write(str_.format(t, obs, sim))
                
        file_.write('\n\n')
                
        # Outcomes.
        file_.write('   Wages \n\n')
            
        file_.write('   Period     Observed      Simulated \n\n')
        
        str_ = '     {0:<5}{1:<10}     {2:<10}\n'
                
        for t in range(numPeriods):
            
            obs = _getInfo(obsEconomy.getAttr('wages')[t])

            sim = _getInfo(simEconomy.getAttr('wages')[t])
              
            file_.write(str_.format(t, obs, sim))           

        file_.write('\n\n')     
        
def _writeParameters(parasObj, initDict):
    ''' Write parameters.
    '''         

    # Write information.       
    with open('inform.struct.out', 'a') as file_:     
               
        file_.write('\n Parametrization\n --------------- ')
        
        # Auxiliary objects.
        paras   = parasObj.getAttr('dict')

        utility = paras['utility']

        wage    = paras['wage']
                
        id_     = 0
        
        # Environment.
        str_ = '  {0:>3}   {1:<10}{2:7.2f}\n'

        file_.write('\n\n Environment \n\n')
        
        for key_ in ['subsidy', 'cost', 'discount']:
            
            file_.write(str_.format(id_, key_, paras[key_]))
            
            id_ = id_ + 1
            
        # Utility.
        str_ = '  {0:>3}   {1:<10}{2:7.2f}  {3:<1}\n'
        
        file_.write('\n Utility \n\n')

        rest = _processRestriction(initDict, 'child')

        file_.write(str_.format(id_, 'child', paras['child'], rest))

        id_ = id_ + 1

        file_.write('\n')
            
        coeffs, int_ = utility 

        for count, coeff in enumerate(coeffs[0]):

            rest = _processRestriction(initDict, 'utility', 'coeffs', count)
            
            file_.write(str_.format(id_, 'coeff', coeff, rest))
            
            id_ = id_ + 1
            
        file_.write('\n')
    
        rest = _processRestriction(initDict, 'utility', 'int', 0)

        file_.write(str_.format(id_, 'int', int_, rest))      
                        
        id_ = id_ + 1
        
        # Wage.
        str_ = '  {0:>3}   {1:<10}{2:7.2f}  {3:<1}\n'
            
        file_.write('\n Wage \n\n')
        
        rest = _processRestriction(initDict, 'child')

        file_.write(str_.format(id_, 'experience', paras['experience'], rest))

        id_ = id_ + 1

        file_.write('\n')
            
        coeffs, int_ = wage
            
        for coeff in coeffs[0]:
                
            rest = _processRestriction(initDict, 'wage', 'coeffs', 0)
            
            file_.write(str_.format(id_, 'coeff', coeff, rest))
            
            id_ = id_ + 1
            
        file_.write('\n')
        
        rest = _processRestriction(initDict, 'wage', 'int', 0)
        
        file_.write(str_.format(id_, 'int', int_, rest))    
        
        id_ = id_ + 1
        
        # Shocks.
        str_ = '  {0:>3}   {1:<10}{2:7.2f}  {3:<1}\n'
                    
        file_.write('\n Shocks \n\n')        
        
        for shock in ['eps', 'eta']:

            rest = _processRestriction(initDict, 'shocks', shock, 0)
        
            file_.write(str_.format(id_, shock, paras[shock]['sd'], rest))

            id_ = id_ + 1
        
        rest = _processRestriction(initDict, 'shocks', 'rho', 0)
        
        file_.write(str_.format(id_, 'rho', paras['rho'], rest))       
            
        file_.write('\n')
          
''' Main function.
'''
def inform(detailed = False):
    ''' Inform about current point of evaluation.
    ''' 
    # Antibugging.
    assert (detailed in [True, False])
    
    # Initialize.
    initObj = initCls()
    
    initObj.read()
    
    initObj.lock()
    
    initDict = initObj.getAttr('initDict')
    
    # Auxiliary objects.
    parasObj = initDict['PARAS']
    
    open('inform.struct.out', 'w').close()

    # Detailed information.
    if(detailed):

        simEconomy = simulate(update = True, observed = False, inform = True)
        
        obsEconomy = pkl.load(open(initDict['EST']['file']))
    
        _writeDescriptive(simEconomy, obsEconomy)
        
    # Parametrization.
    if(os.path.exists('stepInfo.struct.out')):
        
        parasObj.update(readStep('paras'), 'internal', 'all')
    
    _writeParameters(parasObj, initDict)
        
''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
        'Inform about evaluation point of structToolbox.', 
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--detailed', \
                        action  = 'store_true', \
                        dest    = 'detailed', \
                        default = False, \
                        help    = 'detailed information')

    detailed = _distributeInput(parser)
    
    inform(detailed = detailed)