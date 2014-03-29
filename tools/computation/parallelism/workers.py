''' Script for parallel execution.
'''
# standard library
import  cPickle as      pkl
import  numpy   as      np

from    mpi4py  import  MPI
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../../')

from tools.economics.economy.clsEconomy             import economyCls

from tools.optimization.criterions.mle.calculations import _scalarEvaluations

import _auxiliary as aux

''' Auxiliary functions.
'''


''' Communicators.
'''
comm       = MPI.Comm.Get_parent()

size, rank = comm.Get_size(), comm.Get_rank()

''' Distribute attributes.
'''
obsEconomy = pkl.load(open('obsEconomy.pkl', 'r'))

agentObjs  = obsEconomy.getAttr('agentObjs')

parasObj   = obsEconomy.getAttr('parasObj')

''' Set up small economy.
'''
agentObjs = aux.splitList(agentObjs, size)[rank]


economyObj = economyCls()

economyObj.setAttr('agentObjs', agentObjs)

economyObj.setAttr('parasObj', parasObj)

economyObj.lock()


numParas = parasObj.getAttr('numParas')

''' Core of algorithm.
'''
while True:
    
    # Waiting.    
    cmd = np.array(0, dtype = 'int32')
    
    comm.Bcast([cmd, MPI.INT], root = 0)    

    # Compute likelihood.
    if(cmd == 1):

        # Process new parametrization.
        paraVals = np.tile(np.nan, numParas) 

        comm.Bcast([paraVals, MPI.FLOAT], root = 0) 
        
        parasObj.update(paraVals, 'internal', 'all')

        # Evaluate likelihood.
        likl =  _scalarEvaluations(economyObj, parasObj)

        # Reduce operation.
        comm.Reduce([likl, MPI.DOUBLE], None, op = MPI.SUM, root = 0)

    # Terminate.           
    if(cmd == -1): 
        
        comm.Disconnect()
        
        break
    