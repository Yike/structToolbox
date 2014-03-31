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

import _auxiliary as aux

class commCls(meta):
    
    def __init__(self):
        
        self.attr = {}

        self.attr['strategy']    = None
        
        self.attr['numProcs']    = None

        self.attr['accelerated'] = None

        # Derived attributes.
        self.attr['comm']       = None
        
        # Status indicator.
        self.isLocked = False
    
    def initialize(self):
        ''' Initialize the MPI ring.
        '''
        
        # Distribute class attributes.
        strategy    = self.attr['strategy']

        accelerated = self.attr['accelerated']
        
        
        file_ =  os.path.dirname(os.path.realpath(__file__)) + '/workers.py'
        
        numSlaves = self.attr['numProcs'] - 1
        
        comm = MPI.COMM_SELF.Spawn(sys.executable, args = [file_], \
                maxprocs = numSlaves)
        
        # Broadcast strategy information.
        cmd = 0
        
        if(strategy == 'gradient'): cmd = 1
            
        comm.Bcast([np.array(cmd, dtype = 'int32'), MPI.INT], root = MPI.ROOT)  

        # Broadcast performance information.
        cmd = 0
        
        if(accelerated): cmd = 1
            
        comm.Bcast([np.array(cmd, dtype = 'int32'), MPI.INT], root = MPI.ROOT)  
                
        # Finishing.
        self.attr['comm'] = comm
    
    def terminate(self):
        ''' Terminate MPI ring.
        '''
        # Distribute class attributes.
        comm = self.attr['comm']

        # Terminate process.
        comm.Bcast([np.array(-1, dtype = 'int32'), MPI.INT], root = MPI.ROOT)    
                
        comm.Disconnect()     

    def evaluateFunction(self, parasObj):
        ''' Evaluate likelihood using MPI ring.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (self.attr['strategy'] == 'function')

        # Evaluate function.
        rslt = self._function(parasObj)
        
        # Finishing.
        return rslt
        
    def evaluateGradient(self, parasObj, f0, epsilon):
        ''' Evaluate likelihood using MPI ring.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (self.attr['strategy'] == 'gradient')
        
        # Evaluate gradient.
        rslt = self._gradient(parasObj, f0, epsilon)
        
        # Finishing.
        return rslt
    
    ''' Private functions.
    '''
    def _gradient(self, parasObj, f0, epsilon):
        ''' Evaluate gradient.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (f0 is not None)
        
        # Distribute class attributes.
        comm      = self.attr['comm']

        numSlaves = self.attr['numProcs'] - 1
         
        # Auxiliary objects.
        numFree = parasObj.getAttr('numFree')
        
        packets  = aux.splitList(range(numFree), numSlaves) 
        
        # Command.       
        comm.Bcast([np.array(1, dtype = 'int32'), MPI.INT], root = MPI.ROOT)    
    
        # Current parametrization.
        values = parasObj.getValues('internal', 'all')
    
        comm.Bcast([values, MPI.FLOAT], root = MPI.ROOT)

        # Epsilon.
        epsilon = np.array(epsilon)
        
        comm.Bcast([epsilon, MPI.FLOAT], root = MPI.ROOT)
                
        # Baseline function value.
        f0 = np.array(f0)
        
        comm.Bcast([f0, MPI.FLOAT], root = MPI.ROOT)
        
        # Collect result.
        rslt = np.zeros(numFree, dtype = 'float')

        for rank in range(numSlaves):
            
            numRecv = len(packets[rank])
            
            recv    = np.zeros(numRecv, dtype = 'float')
            
            comm.Recv([recv, MPI.DOUBLE], source = rank, \
                        tag = MPI.ANY_TAG)
            
            rslt[packets[rank]] = recv
     
        # Finishing.
        return rslt
        
    def _function(self, parasObj):
        ''' Evaluate criterion function.
        '''
        # Antibugging.
        assert (self.getStatus() == True)

        # Distribute class attributes. 
        comm      = self.attr['comm']
                    
        # Construct likelihood.        
        comm.Bcast([np.array(1, dtype = 'int32'), MPI.INT], root = MPI.ROOT)    
    
        values = parasObj.getValues('internal', 'all')
    
        comm.Bcast([values, MPI.FLOAT], root = MPI.ROOT)
        
        likl = np.array(0.0, 'float64')
            
        comm.Reduce(None, [likl, MPI.DOUBLE], op = MPI.SUM, root = MPI.ROOT)
            
        # Scaling.
        rslt = likl
        
        # Finishing.
        return rslt
        
    def _derivedAttributes(self):
        ''' Derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
