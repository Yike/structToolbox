#!/usr/bin/env python
''' Terminate estimation run.
'''

# standard library.
import subprocess
import os

import numpy as np

''' Terminate process and clean up.
'''
try:
    pid = np.genfromtxt('.pid', dtype ='int')    
    
    os.unlink('.pid')
    
    subprocess.call(['kill', str(pid)])
    
except :
    
    pass
