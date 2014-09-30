''' Collection of auxiliary functions.
'''
# standard library
import shlex

import numpy  as np
import pickle as pkl

''' Auxiliary 
'''
def readStep(which):
    ''' Process restart information.
    '''
    # Antibugging.
    assert (which in ['paras', 'fval'])
    
    if(which == 'paras'):
        
        rslt = np.genfromtxt('stepInfo.struct.out', skip_header = 8)
    
    else:
        
        rslt = float(shlex.split(open('stepInfo.struct.out', 'r').readlines()[3])[1])
    
    # Finishing.
    return rslt

def writeStep(vals, fval = '---', count = '---', pkl_ = False):
    ''' Write out step information.
    '''
    with open('stepInfo.struct.out', 'w') as file_:
                
        file_.write('\n Step ' + str(count) + '\n\n')

        str_  = '{0:<10}\n'
                
        file_.write(' Fval ' + str_.format(fval) + '\n\n')

        file_.write(''' Parameters \n\n''')
            
        str_  = ' {0:15.10f}\n'
        
        for i in range(len(vals)):
                
            file_.write(str_.format(vals[i]))
                
        file_.write('\n')
    
    # High precision version.
    if(pkl_):

        dict_ = {}
        
        dict_['fval'] = fval
            
        dict_['vals'] = vals
        
        pkl.dump(dict_, open('stepInfo.struct.pkl', 'wb'))