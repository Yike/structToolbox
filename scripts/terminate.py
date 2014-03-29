#!/usr/bin/env python
''' Terminate estimation run.
'''

# standard library.
import subprocess
import argparse
import os

import numpy as np

''' Execution of module as script.
'''
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description = 
      'Terminate estimation run.')

    args = parser.parse_args()
 
    try:
        
        pid = np.genfromtxt('.pid', dtype ='int')    
        
        os.unlink('.pid')
        
        subprocess.call(['kill', str(pid)])
        
    except :
        
        pass

