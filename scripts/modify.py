#!/usr/bin/env python
''' This script allows to conveniently modify the parametrization of the 
    estimation.
    
    Examples:
    
        structToolbox-modify --action free --identifiers 9 15
        
        structToolbox-modify --action fix --identifiers 9 15 

        structToolbox-modify --action change --identifiers 0 5 --value 0.1 0.5
                 
'''
# Check for appropriate Python version.
import sys

assert (sys.version_info[:2][0] == 3), \
'''\n\n The structToolbox is targeted towards Python 3.x.x. Please
 change your Python Interpreter accordingly.\n'''
 
 
# standard library
import argparse
import shutil
import shlex
import os

# Pythonpath
dir_ = os.path.dirname(os.path.realpath(__file__)).replace('/scripts', '')
sys.path.insert(0, dir_)

# project library
from tools.user.interface   import *
from tools.auxiliary        import readStep
from tools.auxiliary        import writeStep

''' Auxiliary functions.
''' 
def _distributeInput(parser):
    ''' Check input for modification script.
    '''
    def _processArgs(input_, type_):
        ''' Process arguments.
        '''
        # Antibugging.
        assert (isinstance(input_, list))
        assert (type_ in ['int', 'float'])
 
        # Split elements.
        str_, input_ = ','.join(input_), []
        
        for substring in str_.split(','):
                    
            if(type_ == 'int'):   substring = int(substring)

            if(type_ == 'float'): substring = float(substring)
                
            input_ = input_ + [substring]

        # Finishing. 
        return input_
    
    # Parse arguments.
    args = parser.parse_args()

    # Distribute arguments.
    action      = args.action 
                
    identifiers = args.identifiers 

    values      = args.values 
    
    # Process identifier and values.
    identifiers = _processArgs(identifiers, 'int')
    
    if(values is not None): values = _processArgs(values, 'float')
    
    if(action == 'change'): assert (values is not None)
    
    # Finishing.        
    return action, identifiers, values

def _processCases(currentLine):
    ''' Process special cases and parameters.
    '''
    # Parametrization
    isPara, type_, pos, value = False, None, None, None
    
    # Deal with empty lines.        
    isEmpty = (len(currentLine) == 0)
     
    if(not isEmpty):
        
        type_  = currentLine[0]
        
        isPara = (type_ in ['coeff', 'int', 'exper', 'child', 'eps', 'eta', \
                            'rho', 'subsidy', 'cost', 'discount'])
        
        value = currentLine[-1]
        
        pos = ''
                
        if(len(currentLine) == 3): pos = currentLine[1]
                
    # Antibugging.
    assert (isPara in [True, False]) 
    
    # Finishing
    return isPara, type_, pos, value

def _valueChange(action, info, value):
    ''' Modify the value of a parameter.
    '''
    # Antibugging
    assert (action in ['change'])
    
    # Auxiliary information.
    isFixed = (info[0] == '!')

    # Modifications.
    info = str(value)
    
    if(isFixed): info = '!' + info
   
    # Finishing.
    return info

def _statusChange(action, info):
    ''' Modify the status of a parameter.
    '''
    # Antibugging
    assert (action in ['free', 'fix'])

    # Modifications.                
    if(action == 'free'):

        try:
                        
            info = info.replace('!','')
                        
        except:
                        
            pass
                
    elif(action == 'fix'):
                    
        if(info[0] != '!'):
                        
            info = '!' + info

    # Finishing.
    return info

def _checkQuality(identifiers):
    ''' Check quality of new material.
    '''
    # Checks.
    initObj = initCls()
    
    initObj.read()
    
    initObj.lock()
    
    
    initDict = initObj.getAttr('initDict')
    
    parasObj = initDict['PARAS']

    if(os.path.exists('stepInfo.struct.out')):
        
        parasObj.update(readStep('paras'), 'internal', 'all')

    assert (all(identifier in range(parasObj.getAttr('numParas')) \
                for identifier in identifiers))
        
''' Main function.
'''
def modify(action, identifiers, values = None):
    ''' Modify parameters.
    '''                                          
    # Antibugging.
    assert (action in ['free', 'fix', 'change'])
    assert (isinstance(identifiers, list))

    # Auxiliary objects.
    str_ = '\t {0:<8}{1:<8}\t{2:<8}\n'
    
    for i, id_ in enumerate(identifiers):
        
        fin, fout = open('model.struct.ini'), open('.model.struct.ini', 'wt')
    
        if(action == 'change'): value = values[i]
                        
                        
        count = -1
        
        for line in fin:
            
            # Process line.
            currentLine = shlex.split(line)
        
            # Check for parameters.
            isPara, type_, pos, info = _processCases(currentLine)
                    
            if(isPara): count = count + 1    
            
            # Check for relevance
            isRelevant = ((count == id_) and (isPara))

            if(not isRelevant):
                
                fout.write(line)
                        
            else:

                if(action in ['free','fix']):
                 
                    assert (type_ not in ['subsidy', 'cost', 'discount'])
                    
                    info = _statusChange(action, info)

                elif(action in ['change']):
                    
                    info = _valueChange(action, info, value)
                                
                fout.write(str_.format(type_, pos, info))
        
                ''' Update stepInfo.log 
                '''
                if(os.path.exists('stepInfo.struct.out')):
                
                    updatedValue = info.replace('!', '')
                
                    new = readStep('paras')
                    
                    new[id_] = float(updatedValue)
                    
                    writeStep(new)
                                          
        fin.close(); fout.close()
                
        shutil.move('.model.struct.ini', 'model.struct.ini')                            
        
    # Check quality.
    _checkQuality(identifiers)
        
''' Execution of module as script.
'''
if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description = 
      'Modify parameters for estimation using structToolbox.', 
      formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--action', \
                        action   = 'store', \
                        dest     = 'action', \
                        default  = 'init.ini', \
                        choices  = ['fix', 'free', 'change'], \
                        help     = 'action requested',\
                        required = True)
    
    parser.add_argument('--identifiers', \
                        action   = 'store', \
                        dest     = 'identifiers', \
                        nargs    = '*', \
                        default  =  None, \
                        help     = 'identifiers of parameters',\
                        required = True)

    parser.add_argument('--values', \
                        action   = 'store', \
                        nargs    = '*', \
                        dest     = 'values', \
                        default  =  None, \
                        help     = 'updated parameter values')

    action, identifiers, values = _distributeInput(parser)
    
    modify(action = action, identifiers = identifiers, values = values)
