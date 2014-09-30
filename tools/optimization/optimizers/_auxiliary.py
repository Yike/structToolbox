''' Collection of auxiliary functions for the optimization process.
'''

# standard library
import shutil
import atexit
import uuid
import os

from signal import signal
from signal import SIGTERM 

''' Auxiliary functions.
'''
def cleanup():
    ''' Clean estimation directory.
    '''
    
    try:
        
        os.remove('.optimization.struct.out')
        
    except:
        
        pass
    
def setup():
    ''' Setup directory for estimation run.
    '''
    
    # Working directory.        
    dir_= '.slave-' + str(uuid.uuid4()) + '.struct.out'

    os.mkdir(dir_)
    
    os.chdir(dir_)
    
    # Copy information.
    shutil.copy('../optimizers.struct.ini', '.')

    shutil.copy('../model.struct.ini', '.')

    # Running.
    open('.optimization.struct.out', 'w').close()
    
    atexit.register(cleanup,)
                
    signal(SIGTERM, lambda signum, stack_frame: exit(1))
    

