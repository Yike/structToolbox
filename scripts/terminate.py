#!/usr/bin/env python
''' Terminate estimation run.
'''

# standard library.
import numpy as np

import subprocess
import argparse
import os
import sys

# Check for appropriate version.
assert (sys.version_info[:2] == (2,7)), \
'''\n\n This release of the structToolbox is targeted towards Python 2.7.x,
 we will update to Python 3.x.x in our next iteration. Please change
 your default Python Interpreter accordingly.\n'''

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
      'Terminate estimation run of structToolbox.', 
      formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()
 
    try:
        
        pid = np.genfromtxt('.struct.pid', dtype ='int')    
        
        os.unlink('.struct.pid')
        
        subprocess.call(['kill', str(pid)])
        
    except :
        
        pass

