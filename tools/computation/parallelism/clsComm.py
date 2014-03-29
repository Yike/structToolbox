''' Class for MPI communication.
'''

# standard library
import sys
import os

import numpy as np

try:
    
    from mpi4py     import MPI

except ImportError:
    
    pass

# project library
from tools.clsMeta import meta


class commCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        self.attr['numProcs'] = None
        
        # Derived attributes.
        self.attr['comm'] = None
        
        # Status indicator.
        self.isLocked = False
    
    def initialize(self):
        ''' Initialize the MPI ring.
        '''
        
        file_ =  os.path.dirname(os.path.realpath(__file__)) + '/workers.py'
        
        numSlaves = self.attr['numProcs'] - 1
        
        comm = MPI.COMM_SELF.Spawn(sys.executable, args = [file_], \
                maxprocs = numSlaves)
        
        self.attr['comm'] = comm
    
    def terminate(self):
        ''' Terminate MPI ring.
        '''
        # Distribute class attributes.
        comm  = self.attr['comm']

        # Terminate process.
        comm.Bcast([np.array(-1, dtype = 'int32'), MPI.INT], root = MPI.ROOT)    
                
        comm.Disconnect()     
    
    def evaluate(self, parasObj):
        ''' Evaluate likelihood using MPI ring.
        '''
        # Distribute class attributes.
        comm  = self.attr['comm']
            
        
        comm.Bcast([np.array(1, dtype = 'int32'), MPI.INT], root = MPI.ROOT)    

        values = parasObj.getValues('internal', 'all')

        comm.Bcast([values, MPI.FLOAT], root = MPI.ROOT)
    
        likl = np.array(0.0, 'float64')
        
        comm.Reduce(None, [likl, MPI.DOUBLE], op = MPI.SUM, root = MPI.ROOT)

        # Finishing.
        return likl
    
    def _derivedAttributes(self):
        ''' Derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
