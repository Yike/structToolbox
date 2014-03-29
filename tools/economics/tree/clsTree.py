''' This module contains classes for the construction of decision tree.
'''

# standard library
import collections

# project library
from tools.clsMeta import meta

from clsNode      import nodeCls


class treeCls(meta):
    ''' Tree class that holds summary information about the tree which is 
        constructed using the nodesCls.   
    '''
    
    def __init__(self):
        ''' Constructor for treeCls.
        '''
        # Antibugging.
        
        # Initialize root node.
        rootNode               = nodeCls()
        rootNode.attr['name']  = '0'
        
        rootNode.lock()
        
        self.attr = {}
        
        self.attr['rootNode'] = rootNode

        self.attr['terminalNodes'] = None
        self.attr['allDepths']     = None
        self.attr['allNodes']      = None

        self.attr['nodeDepths'] = None
        self.attr['maxDepths']  = None
        
        self.attr['names']  = None
        
        # Status.
        self.isLocked = False
        
        # Maintenance.
        self._constructAttributes()
        
        self._checkIntegrity()
    
    def __str__(self):
        ''' String representation of treeCls. It allows for easy checking of 
            the tree structure.
        
        '''
        
        treeDict = {}
        
        allNodes = self.getAllNodes()
        
        for node in allNodes:
            
            treeDict[node.name] = []
            
            if(node.upper is not None):
                
                treeDict[node.name].append(node.upper.name)
                
            if(node.lower is not None):
                
                treeDict[node.name].append(node.lower.name)
        
        return str(treeDict)

    def _constructAttributes(self):
        ''' Construction of class attributes.
        
        '''
    
        self.attr['terminalNodes']  = self.getTerminalNodes()
        self.attr['allNodes']       = self.getAllNodes()
        self.attr['allDepths']      = self.getAllDepths()
        self.attr['maxDepths']      = max(self.attr['allDepths'])
        
        self.attr['nodeDepths']     = self._createNodeDepths()  
        self.attr['names']      = self._getnames()
 
    def addNode(self, nodeName, parentName, location):
        ''' Add a node to an existing treeObj.
        
        '''
        # Antibugging.
        assert isinstance(nodeName, str)
        assert (parentName in self.attr['names'])
        assert (nodeName not in self.attr['names'])
        assert (location in ['lower', 'upper'])
            
        nodeObj = nodeCls()
        nodeObj.attr['name'] = nodeName
        
        parentObj = self.getNodes(parentName)
        
        assert (parentObj.attr['numBranches'] in [0,1])
        
        nodeObj.attr['parent'] = parentObj
        
        # Attach node.
        if(location == 'lower'):
            
            assert (parentObj.attr['lower'] is None)

            parentObj.attr['lower']       = nodeObj            
            parentObj.attr['lower'].attr['depth'] = parentObj.attr['depth'] + 1 
            parentObj.attr['isTerminal']  = False
            
        if(location == 'upper'):
            
            assert (parentObj.attr['upper'] is None)
            
            parentObj.attr['upper']       = nodeObj
            parentObj.attr['upper'].attr['depth'] = parentObj.attr['depth'] + 1
            parentObj.attr['isTerminal']  = False
            
        parentObj.attr['numBranches'] += 1
               
        # Update tree information.
        self._constructAttributes()
        
        self._checkIntegrity()

        nodeObj.lock()

    ''' Helpful functions for working with an instance of the treeCls.
    
    '''

    def getNodes(self, names):
        ''' Get node corresponding to names.
        
        '''
        
        isList = isinstance(names, list)
        
        if(isList == False): names = [names]
        
        rslt = []
        
        allNodes = self.attr['allNodes']
       
        for nodeName in names:
           
            for node in allNodes:
                
                if(node.attr['name'] == nodeName): rslt.append(node)
        
        if(isList == False): rslt = rslt[0]
        
        return rslt
    
    def getAllNodes(self):
        ''' Get a list of all nodes.
        
        '''
        def getAllNodesRecursive(node,listAllNodes):
                
            listAllNodes.append(node)
                
            if(node.attr['lower'] != None): 
                    
                getAllNodesRecursive(node.attr['lower'],listAllNodes)
        
            if(node.attr['upper'] != None): 
                    
                getAllNodesRecursive(node.attr['upper'],listAllNodes)
                     
            return listAllNodes
        
        listAllNodes = []
           
        listAllNodes = getAllNodesRecursive(self.attr['rootNode'],listAllNodes)
       
        return  sorted(listAllNodes)
    
    def getTerminalNodes(self):

        def getTerminalNodesRecursive(node, listTerminalNodes):

            if((node.attr['lower'] == None) and (node.attr['upper'] == None)):
                
                listTerminalNodes.append(node)
        
            if(node.attr['lower'] != None): 
                    
                getTerminalNodesRecursive(node.attr['lower'],listTerminalNodes)
                
            if(node.attr['upper'] != None): 
                
                getTerminalNodesRecursive(node.attr['upper'],listTerminalNodes)
                 
            return listTerminalNodes

        listTerminalNodes = []
            
        rootNode = self.attr['rootNode']
            
        listTerminalNodes = getTerminalNodesRecursive(rootNode,listTerminalNodes)
    
        return listTerminalNodes
    
    def getNodeDepths(self, requestedDepths):
        ''' Currently does not stop after depth is completed. contiues
            through whole tree.
            
        '''
        def getNodeDepthsRecursive(node, requestedDepths, listNodeDepths):
            ''' Currently does not stop after depth is completed. continues
                through whole tree.
               
            '''
                
            if(node.attr['depth'] == requestedDepths):
         
                listNodeDepths.append(node)
        
            if(node.attr['lower'] != None): 
                    
                getNodeDepthsRecursive(node.attr['lower'],requestedDepths, listNodeDepths)
        
            if(node.attr['upper'] != None): 
                    
                getNodeDepthsRecursive(node.attr['upper'],requestedDepths, listNodeDepths)
                
            return listNodeDepths
        
        err = (requestedDepths not in self.attr['allDepths'])
        
        if(err): raise simMethodsError('error in treeMod: requested depth not available')
        
        node = self.attr['rootNode']
    
        listNodeDepths = []        
            
        listNodeDepths = getNodeDepthsRecursive(node, requestedDepths, listNodeDepths)
    
        return listNodeDepths

    def getnames(self, nodes):
        ''' Extract names from a collection of nodes.
        
        '''      
        names = []
        
        for node in nodes:
            
            names.append(node.attr['name'])
            
        return sorted(names)

    def getNextNodes(self, node):
        ''' Routine returns a list of the next nodes.
            
        '''
        listNextNodes = []
            
        if(node.attr['lower'] != None):
                
            listNextNodes.append(node.attr['lower'])
            
        if(node.attr['upper'] != None):
                
            listNextNodes.append(node.attr['upper'])
    
        return listNextNodes

    def getAllDepths(self):
        
        def getAllDepthsRecursive(node, listAllDepths):
                
            listAllDepths.append(node.attr['depth'])
                
            if(node.attr['lower'] != None): 
                    
                getAllDepthsRecursive(node.attr['lower'],listAllDepths)
        
            if(node.attr['upper'] != None): 
                    
                getAllDepthsRecursive(node.attr['upper'],listAllDepths)
                     
            return listAllDepths
        
        listAllDepths = []
            
        listAllDepths = getAllDepthsRecursive(self.attr['rootNode'], listAllDepths)
        
        listAllDepths = sorted(list(set(listAllDepths)))  
            
        return listAllDepths                     
    
    ''' Private housekeeping functions.
    
    '''
    def _getnames(self):
        ''' Create a list with the names of all nodes.
        
        '''
        names = []
        
        for node in self.attr['allNodes']:
            
            names.append(node.attr['name'])
        
        return names
    
    def _createNodeDepths(self):
        ''' Generate a list with nodes for each level of depth.
        
        ''' 
        nodeDepths = []
        
        for depth in range(self.attr['maxDepths'] + 1):
   
            nodeDepths.append(self.getNodeDepths(depth))
            
        return nodeDepths
                     


                    