''' Construct tree object.
'''

# project library
from tools.economics.tree.clsTree import treeCls

def _constructTree(initDict):
    ''' Construct tree from model.cfg.
    '''
    # Distribute information.
    numPeriods = initDict['BASICS']['periods']
    
    # Algorithm.
    treeObj = treeCls()

    for _ in range(numPeriods):
    
        terminalNodes = treeObj.getTerminalNodes()
        
        for terminalNode in terminalNodes:
            
            name = terminalNode.getAttr('name')
            
            treeObj.addNode(name + '1', name, 'upper')
    
            treeObj.addNode(name + '0', name, 'lower')

    treeObj.lock()
    
    # Finishing.
    return treeObj