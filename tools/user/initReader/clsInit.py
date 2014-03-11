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

                if(keyword ==  'EXPERIENCE'):

                    initDict = self._processEXPERIENCE(initDict, currentLine)  
                                        
                if(keyword ==  'CHILDREN'):
                        
                    initDict = self._processCHILD(initDict, currentLine)        
        
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
        
        pos = pos + initDict['CHILD']['coeffs']['pos']
    
        pos = pos + initDict['WAGE']['coeffs']['pos']
    
        pos = pos + initDict['UTILITY']['coeffs']['pos']

        pos = pos + initDict['EXPERIENCE']['coeffs']['pos']
                
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
            
        # Finishing.
        return initDict
    
    def _processCHILD(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]

        # Construct dictionary.          
        if(keyword in ['coeff']):
            
            pos = int(flag)
            
            value, isFree = aux._processLine(currentLine[2])
                        
            initDict['CHILD']['coeffs']['pos']   = [pos]

            initDict['CHILD']['coeffs']['value'] = [value]

            initDict['CHILD']['coeffs']['free']  = [isFree]
            
        # Finishing.
        return initDict

    def _processEXPERIENCE(self, initDict, currentLine):
        ''' Process optimization details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        
        # Process information.    
        keyword = currentLine[0]
        flag    = currentLine[1]

        # Construct dictionary.          
        if(keyword in ['coeff']):
            
            pos = int(flag)
            
            value, isFree = aux._processLine(currentLine[2])
                        
            initDict['EXPERIENCE']['coeffs']['pos']   = [pos]

            initDict['EXPERIENCE']['coeffs']['value'] = [value]

            initDict['EXPERIENCE']['coeffs']['free']  = [isFree]
            
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
        
        if(keyword in ['restart']):
                            
            if(flag.upper() == 'FALSE'):
                                
                flag = False 
                            
            else:
                                
                flag = True
        
        if(keyword in ['processors']):
            
            flag = int(flag)
        
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


        initDict['EXPERIENCE']  = {}

        initDict['UTILITY']     = {}
        
        initDict['BASICS']      = {}
                
        initDict['CHILD']       = {}

        initDict['SPOUSE']      = {}

        initDict['SHOCKS']      = {}

        initDict['DERIV']       = {}

        initDict['WAGE']        = {}
                                        
        initDict['OPT']         = {}

        initDict['EST']         = {}   

        initDict['SIM']         = {}   
        
        
        initDict['EXPERIENCE']['coeffs'] = {}

        initDict['EXPERIENCE']['coeffs']['value'] = []
        
        initDict['EXPERIENCE']['coeffs']['pos']   = []

        initDict['EXPERIENCE']['coeffs']['free']  = []
                        

        initDict['CHILD']['coeffs'] = {}

        initDict['CHILD']['coeffs']['value'] = []
        
        initDict['CHILD']['coeffs']['pos']   = []

        initDict['CHILD']['coeffs']['free']  = []

        
        initDict['UTILITY']['coeffs'] = {}

        initDict['UTILITY']['coeffs']['value'] = []
        
        initDict['UTILITY']['coeffs']['pos']   = []

        initDict['UTILITY']['coeffs']['free']  = []
        
        
        initDict['UTILITY']['int'] = {}
        
        initDict['UTILITY']['int']['value'] = []

        initDict['UTILITY']['int']['free']  = []


        initDict['WAGE']['coeffs']    = {}

        initDict['WAGE']['coeffs']['value']  = []

        initDict['WAGE']['coeffs']['pos']    = []

        initDict['WAGE']['coeffs']['free']   = []


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
        
