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

import tools.computation.performance.performance    as     perf

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

numParas   = parasObj.getAttr('numParas')

numFree    = parasObj.getAttr('numFree')


    
''' Strategy.
'''
cmd = np.array(0, dtype = 'int32')
    
comm.Bcast([cmd, MPI.INT], root = 0)    

strategy = 'function'

if(cmd == 1): strategy = 'gradient'

''' Performance enhancements.
'''
cmd = np.array(0, dtype = 'int32')
    
comm.Bcast([cmd, MPI.INT], root = 0)    

accelerated = False

if(cmd == 1): accelerated = True

perf.initialize(accelerated)


''' Set up small economy.
'''
if(strategy == 'function'):
    
    agentObjs = aux.splitList(agentObjs, size)[rank]

    
    economyObj = economyCls()
    
    economyObj.setAttr('agentObjs', agentObjs)
    
    economyObj.setAttr('parasObj', parasObj)
    
    economyObj.lock()

else:

    packets  = range(numFree)
    
    packet   = aux.splitList(packets, size)[rank]
    
    numEvals = len(packet)
    

    economyObj = obsEconomy

numSubset = economyObj.getAttr('numAgents')

numAgents = obsEconomy.getAttr('numAgents')

''' Core of algorithm.
'''
while True:
    
    # Waiting.    
    cmd = np.array(0, dtype = 'int32')
    
    comm.Bcast([cmd, MPI.INT], root = 0)    

    # Compute likelihood.
    if(cmd == 1):
        
        if(strategy == 'function'):

            # Process new parametrization.
            paraVals = np.tile(np.nan, numParas) 
    
            comm.Bcast([paraVals, MPI.FLOAT], root = 0) 
            
            parasObj.update(paraVals, 'internal', 'all')
    
            # Evaluate likelihood.
            likl = _scalarEvaluations(economyObj, parasObj)
    
            # Scaling.
            likl = (numSubset*likl)/float(numAgents)
            
            likl = np.array(likl)
            
            # Reduce operation.
            comm.Reduce([likl, MPI.DOUBLE], None, op = MPI.SUM, root = 0)
        
        else:
            
            # Process new parametrization.
            paraVals = np.tile(np.nan, numParas) 
    
            comm.Bcast([paraVals, MPI.FLOAT], root = 0) 
            
            parasObj.update(paraVals, 'internal', 'all')
            
            # Epsilon.
            epsilon = np.tile(np.nan, 1)
            
            comm.Bcast([epsilon, MPI.FLOAT], root = 0) 
            
            # Get baseline evaluation.
            f0 = np.tile(np.nan, 1)
            
            comm.Bcast([f0, MPI.FLOAT], root = 0) 
            
            
            x = parasObj.getValues('external', 'free')
            
            
            rslt = np.zeros(numFree, dtype = 'float')
           
            ei   = np.zeros(numFree, dtype = 'float')
            
            pack = np.zeros(numEvals, dtype = 'float')

            # Evaluate gradient.
            count = 0
            
            for k in packet:
                
                ei[k]    = 1.0
                
                d        = epsilon*ei
                
                paraVals = x + d
                
                parasObj.update(paraVals, 'external', 'free')
    
                f1      = _scalarEvaluations(economyObj, parasObj)
                
                rslt[k] = (f1 - f0)/d[k]
                
                ei[k]   = 0.0
            
            
                pack[count] = rslt[k]
            
                count       = count + 1

            comm.Send([pack, MPI.DOUBLE], dest = 0, tag = rank)
            
    # Terminate.           
    if(cmd == -1): 
        
        comm.Disconnect()
        
        break
    