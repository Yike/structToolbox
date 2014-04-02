''' Class for the processing of the initialization file.
'''

# standard library
import shlex

# project library
from tools.clsMeta import meta

# relative import
import _interface  as aux

''' Initialization file class.
'''
class initCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        self.attr['initDict'] = {}
        
        self.isLocked = False
    
    ''' Public Methods.
    '''
    def read(self, configFile = 'init.ini'):
        ''' Read initialization file.
        '''
        # Initialize dictionary.        
        initDict = self._initializeDictionary()
           
        # Algorithm.
        with open(configFile, 'r') as initFile:
        
            for line in initFile:
            
                currentLine = shlex.split(line)

                ''' Preprocessing.
                '''
                isEmpty, isKeyword = aux._processCases(currentLine)
                
                if(isEmpty):    
                    
                    continue
               
                elif(isKeyword):  
                    
                    keyword = currentLine[0]
                
                    continue

                ''' Process major blocks.
                '''
                if(keyword ==  'SPOUSE'):
                        
                    initDict = self._processSPOUSE(initDict, currentLine) 
        
                if(keyword ==  'BASICS'):
                        
                    initDict = self._processBASICS(initDict, currentLine)        
        
                if(keyword == 'SHOCKS'):

                    initDict = self._processSHOCKS(initDict, currentLine)        

                if(keyword ==  'UTILITY'):
                        
                    initDict = self._processUTILITY(initDict, currentLine)  

                if(keyword ==  'WAGE'):
                        
                    initDict = self._processWAGE(initDict, currentLine)  
                    
                if(keyword ==  'OPTIMIZATION'):
                        
                    initDict = self._processOPT(initDict, currentLine)        

                if(keyword ==  'ESTIMATION'):
                        
                    initDict = self._processEST(initDict, currentLine)  

                if(keyword ==  'SIMULATION'):
                        
                    initDict = self._processSIM(initDict, currentLine)  
 
        initDict = self._additionATTR(initDict)
        
        initDict = self._intercepts(initDict)
        
        parasObj = aux._constructParas(initDict)

        treeObj  = aux._constructTree(initDict)
                
                
        initDict['PARAS'] = parasObj

        initDict['TREE']  = treeObj
 
        # Checks.
        aux._checks(initDict)
 
        # Finishing.                                                        
        self.attr['initDict'] = initDict

    ''' Private methods.
    '''
    def _intercepts(self, initDict):
        ''' Check presence of intercepts.
        '''
        
        for key_ in ['WAGE', 'UTILITY']:

            check = (len(initDict[key_]['int']['value']) == 0)
            
            if(check):
                
                initDict[key_]['int']['value'] = [0.00]
    
                initDict[key_]['int']['free']  = [False]            
        
        # Finishing.
        return initDict
    
    def _additionATTR(self,initDict):
        ''' Process additional arguments.
        '''
        
        # Position and number of different attributes
        pos = []

        pos = pos + initDict['UTILITY']['coeffs']['pos']
        
        pos = pos + initDict['UTILITY']['child']['pos']
    
        pos = pos + initDict['WAGE']['coeffs']['pos']
        
        pos = pos + initDict['WAGE']['exper']['pos']
                
        pos = list(set(pos))
        

        initDict['DERIV']['pos']     = pos
        
        initDict['DERIV']['numAttr'] = len(pos)
        
        initDict['DERIV']['static']  = (initDict['BASICS']['discount'] == 0.0)
        
        # Finishing.
        return initDict
        
    def _processWAGE(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        
        # Process information.    
        keyword = currentLine[0]

        # Construct dictionary.   
        if(keyword in ['coeff']):
            
            pos   = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['WAGE']['coeffs']['pos']   += [pos] 
 
            initDict['WAGE']['coeffs']['value'] += [value] 
            
            initDict['WAGE']['coeffs']['free']  += [isFree] 
            
        if(keyword in ['exper']):
            
            pos   = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['WAGE']['exper']['pos']   += [pos] 
 
            initDict['WAGE']['exper']['value'] += [value] 
            
            initDict['WAGE']['exper']['free']  += [isFree] 
                    
        if(keyword in ['int']):
            
            value, isFree = aux._processLine(currentLine[1])
 
            initDict['WAGE']['int']['value'] += [value] 

            initDict['WAGE']['int']['free']  += [isFree] 
                     
        # Finishing.
        return initDict
    
    def _processUTILITY(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        
        # Process information.    
        keyword = currentLine[0]

        # Construct dictionary.   
        if(keyword in ['coeff']):
            
            pos   = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['UTILITY']['coeffs']['pos']   += [pos] 
 
            initDict['UTILITY']['coeffs']['value'] += [value] 

            initDict['UTILITY']['coeffs']['free']  += [isFree] 
                    
        if(keyword in ['int']):
            
            value, isFree = aux._processLine(currentLine[1])
 
            initDict['UTILITY']['int']['value'] += [value] 

            initDict['UTILITY']['int']['free']  += [isFree] 

        if(keyword in ['child']):
            
            pos   = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['UTILITY']['child']['pos']   += [pos] 
 
            initDict['UTILITY']['child']['value'] += [value] 

            initDict['UTILITY']['child']['free']  += [isFree]             
        # Finishing.
        return initDict
    
    def _processSHOCKS(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        
        # Process information.    
        keyword = currentLine[0]
            
        # Construct dictionary.   
        if(keyword == 'sd'):
            
            value, isFree = aux._processLine(currentLine[2])
            
            subtype = currentLine[1]
            
            initDict['SHOCKS'][subtype]['value'] = value

            initDict['SHOCKS'][subtype]['free']  = isFree
        
        if(keyword == 'rho'):
            
            value, isFree = aux._processLine(currentLine[1])
            
            initDict['SHOCKS']['rho']['value'] = value
        
            initDict['SHOCKS']['rho']['free']  = isFree
        
        # Finishing.
        return initDict
    
    def _processSIM(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]
        
        # Type conversion.
        if(keyword in ['file']):
            
            flag = str(flag)
        
        else:
            
            flag = int(flag)
            
        # Construct dictionary.        
        initDict['SIM'][keyword] = flag
        
        # Finishing.
        return initDict

    def _processEST(self, initDict, currentLine):
        ''' Process estimation details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]
        
        if(keyword in ['restart', 'accelerated']):
                            
            if(flag.upper() == 'FALSE'):
                                
                flag = False 
                            
            else:
                                
                flag = True
        
        if(keyword in ['processors']):
            
            flag = int(flag)
        
        if(keyword in ['parallelization', 'file']):
            
            flag = str(flag)
        
        # Construct dictionary.        
        initDict['EST'][keyword] = flag
        
        # Finishing.
        return initDict

    def _processOPT(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]
        
        if(keyword == 'optimizer'):
                            
            toolbox  = currentLine[1].split('-')[0]
                        
            algorithm = currentLine[1].split('-')[1]
                        
            initDict['OPT']['algorithm'] = algorithm
                            
            initDict['OPT']['toolbox']   = toolbox
            
            initDict['OPT']['optimizer'] = flag
            
            return initDict
        
        # Special treatment.
        if(keyword == 'maxiter'):
                            
            if(flag.upper() == 'NONE'):
                                
                flag = None
                                
            else:
                                
                flag = int(flag)
                        
        if(keyword in ['reps', 'cpus']):
        
            flag = int(flag)        
        
        # Construct dictionary.        
        initDict['OPT'][keyword] = flag
        
        # Finishing.
        return initDict

    def _processSPOUSE(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]
        
        if(keyword in ['income']):
            
            flag = float(flag)
    
        # Construct dictionary.        
        initDict['SPOUSE'][keyword] = flag
        
        # Finishing.
        return initDict
        
    def _processBASICS(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]
        
        if(keyword in ['subsidy', 'cost', 'discount']):
            
            flag = float(flag)
                
        if(keyword == 'periods'):
                        
            flag = int(flag)

        # Construct dictionary.        
        initDict['BASICS'][keyword] = flag
        
        # Finishing.
        return initDict

    def _initializeDictionary(self):
        ''' Initialize dictionary.
        '''
        initDict = {}

        initDict['PARAS']   = None


        initDict['UTILITY']     = {}
        
        initDict['BASICS']      = {}

        initDict['SPOUSE']      = {}

        initDict['SHOCKS']      = {}

        initDict['DERIV']       = {}

        initDict['WAGE']        = {}
                                        
        initDict['OPT']         = {}

        initDict['EST']         = {}   

        initDict['SIM']         = {}   


        for keyword in ['coeffs', 'child']:
                     
            initDict['UTILITY'][keyword] = {}
    
            initDict['UTILITY'][keyword]['value'] = []
            
            initDict['UTILITY'][keyword]['pos']   = []
    
            initDict['UTILITY'][keyword]['free']  = []
            
        
        initDict['UTILITY']['int'] = {}
        
        initDict['UTILITY']['int']['value'] = []

        initDict['UTILITY']['int']['free']  = []


        for keyword in ['coeffs', 'exper']:

            initDict['WAGE'][keyword] = {}
    
            initDict['WAGE'][keyword]['value']  = []
    
            initDict['WAGE'][keyword]['pos']    = []
    
            initDict['WAGE'][keyword]['free']   = []
    

        initDict['WAGE']['int']    = {}
        
        initDict['WAGE']['int']['value']  = []

        initDict['WAGE']['int']['free']   = []
        
        
        initDict['SHOCKS'] = {}

        initDict['SHOCKS']['eps'] = {}

        initDict['SHOCKS']['eps']['value'] = None

        initDict['SHOCKS']['eps']['free']  = None


        initDict['SHOCKS']['eta'] = {}

        initDict['SHOCKS']['eta']['value'] = None
        
        initDict['SHOCKS']['eta']['free']  = None
        
        
        initDict['SHOCKS']['rho'] = {}

        initDict['SHOCKS']['rho']['value'] = None
        
        initDict['SHOCKS']['rho']['free']  = None
        
        # Finishing.
        return initDict
        
