''' Class for the processing of the initialization file.
'''

# standard library
import shutil
import shlex

# project library
from tools.clsMeta import meta

# relative import
import tools.user.initReader._interface  as aux

''' Initialization file class.
'''
class initCls(meta):
    
    def __init__(self):
        
        self.attr = {}
        
        self.attr['initDict'] = {}
        
        self.isLocked = False
    
    ''' Public Methods.
    '''
    def read(self):
        ''' Read initialization file.
        '''
        # Initialize dictionary.        
        initDict = self._initializeDictionary()
        
        # Ensure order.
        hasUtility = False
        
        hasEnviro  = False
        
        hasWage    = False
                
        # Algorithm.
        with open('model.struct.ini', 'r') as initFile:
        
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
                if(keyword == 'OBSERVED'):
                        
                    initDict = self._processOBSERVED(initDict, currentLine)
        
                if(keyword == 'ENVIRONMENT'):
                        
                    initDict  = self._processENVIRO(initDict, currentLine)        
                    
                    hasEnviro = True
                
                if(keyword == 'UTILITY'):
                    
                    assert (hasEnviro == True)
                    
                    initDict   = self._processUTILITY(initDict, currentLine)  

                    hasUtility = True

                if(keyword == 'WAGE'):

                    assert (hasUtility == True)
                                    
                    initDict = self._processWAGE(initDict, currentLine)  
                    
                    hasWage  = True

                if(keyword == 'SHOCKS'):
                    
                    assert (hasWage == True)
                    
                    initDict = self._processSHOCKS(initDict, currentLine)        

                if(keyword == 'OPTIMIZATION'):
                        
                    initDict = self._processOPT(initDict, currentLine)        

                if(keyword == 'ESTIMATION'):
                        
                    initDict = self._processEST(initDict, currentLine)  

                if(keyword == 'SIMULATION'):
                        
                    initDict = self._processSIM(initDict, currentLine)  
 
        initDict = self._additionATTR(initDict)
        
        initDict = self._intercepts(initDict)
        
        parasObj = aux._constructParas(initDict)

        treeObj = aux._constructTree(initDict)
                
                
        initDict['PARAS'] = parasObj

        initDict['TREE'] = treeObj
  
        # Finishing.                                                        
        self.attr['initDict'] = initDict

        # Checks and standardization.
        aux._checks(initDict)
        
        self._standardize()
        
    ''' Private methods.
    '''
    def _intercepts(self, initDict):
        ''' Check presence of intercepts.
        '''
        
        for key_ in ['WAGE', 'UTILITY']:

            check = (len(initDict[key_]['int']['value']) == 0)
            
            if(check):
                
                initDict[key_]['int']['value'] = [0.00]
    
                initDict[key_]['int']['free'] = [False]            
        
        # Finishing.
        return initDict
    
    def _additionATTR(self, initDict):
        ''' Process additional arguments.
        '''
        
        # Position and number of different attributes
        pos = []

        pos = pos + initDict['UTILITY']['coeffs']['pos']
        
        pos = pos + initDict['UTILITY']['child']['pos']
    
        pos = pos + initDict['WAGE']['coeffs']['pos']
        
        pos = pos + initDict['WAGE']['exper']['pos']

        pos = pos + [initDict['OBSERVED']['wage']]
        
        pos = pos + [initDict['OBSERVED']['choice']]
        
        pos = pos + [initDict['OBSERVED']['spouse']]
        
        pos = list(set(pos))
        

        initDict['DERIV']['pos'] = pos
        
        initDict['DERIV']['numAttr'] = len(pos)
        
        initDict['DERIV']['static'] = (initDict['ENVIRO']['discount'] == 0.0)
        
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
            
            pos = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
        
            initDict['WAGE']['coeffs']['pos'] += [pos] 
 
            initDict['WAGE']['coeffs']['value'] += [value] 
            
            initDict['WAGE']['coeffs']['free'] += [isFree] 
            
        if(keyword in ['exper']):
            
            pos = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['WAGE']['exper']['pos'] += [pos] 
 
            initDict['WAGE']['exper']['value'] += [value] 
            
            initDict['WAGE']['exper']['free'] += [isFree] 
                    
        if(keyword in ['int']):
            
            value, isFree = aux._processLine(currentLine[1])
 
            initDict['WAGE']['int']['value'] += [value] 

            initDict['WAGE']['int']['free'] += [isFree] 
                     
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
            
            pos = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['UTILITY']['coeffs']['pos'] += [pos] 
 
            initDict['UTILITY']['coeffs']['value'] += [value] 

            initDict['UTILITY']['coeffs']['free'] += [isFree] 
                    
        if(keyword in ['int']):
            
            value, isFree = aux._processLine(currentLine[1])
 
            initDict['UTILITY']['int']['value'] += [value] 

            initDict['UTILITY']['int']['free'] += [isFree] 

        if(keyword in ['child']):
            
            pos = int(currentLine[1])
            
            value, isFree = aux._processLine(currentLine[2])
            
            initDict['UTILITY']['child']['pos'] += [pos] 
 
            initDict['UTILITY']['child']['value'] += [value] 

            initDict['UTILITY']['child']['free'] += [isFree] 
                        
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
        if(keyword in ['rho', 'eps', 'eta']):
            
            value, isFree = aux._processLine(currentLine[1])
            
            initDict['SHOCKS'][keyword]['value'] = value
        
            initDict['SHOCKS'][keyword]['free'] = isFree
        
        # Finishing.
        return initDict

    def _processOBSERVED(self, initDict, currentLine):
        ''' Process position of observed variables.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag = currentLine[1]
        
        # Type conversion.
        flag = int(flag)
            
        # Construct dictionary.        
        initDict['OBSERVED'][keyword] = flag
        
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
        flag = currentLine[1]
        
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

        if(keyword in ['processors']):
            
            flag = int(flag)
        
        if(keyword in ['agents']):
                            
            if(flag.upper() == 'NONE'):
                                
                flag = None
                                
            else:
                                
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

        # Construct dictionary.        
        initDict['OPT'][keyword] = flag
        
        # Finishing.
        return initDict

    def _processENVIRO(self, initDict, currentLine):
        ''' Process environment details.
        '''
        # Antibugging.
        assert (isinstance(initDict, dict))
        assert (isinstance(currentLine, list))
        assert (len(currentLine) == 2)
        
        # Process information.    
        keyword = currentLine[0]
        flag = currentLine[1]
        
        if(keyword in ['subsidy', 'cost', 'discount']):
            
            flag = float(flag)

        # Construct dictionary.        
        initDict['ENVIRO'][keyword] = flag
        
        # Finishing.
        return initDict

    def _initializeDictionary(self):
        ''' Initialize dictionary.
        '''
        initDict = {}

        initDict['PARAS'] = None
        
        initDict['OBSERVED'] = {}

        initDict['UTILITY'] = {}
        
        initDict['ENVIRO'] = {}

        initDict['SHOCKS'] = {}

        initDict['DERIV'] = {}

        initDict['WAGE'] = {}
                                        
        initDict['OPT'] = {}

        initDict['EST'] = {}   

        initDict['SIM'] = {}   


        for keyword in ['coeffs', 'child']:
                     
            initDict['UTILITY'][keyword] = {}
    
            initDict['UTILITY'][keyword]['value'] = []
            
            initDict['UTILITY'][keyword]['pos'] = []
    
            initDict['UTILITY'][keyword]['free'] = []
            
        
        initDict['UTILITY']['int'] = {}
        
        initDict['UTILITY']['int']['value'] = []

        initDict['UTILITY']['int']['free'] = []


        for keyword in ['coeffs', 'exper']:

            initDict['WAGE'][keyword] = {}
    
            initDict['WAGE'][keyword]['value'] = []
    
            initDict['WAGE'][keyword]['pos'] = []
    
            initDict['WAGE'][keyword]['free'] = []
    

        initDict['WAGE']['int'] = {}
        
        initDict['WAGE']['int']['value'] = []

        initDict['WAGE']['int']['free'] = []
        
        
        initDict['SHOCKS'] = {}

        initDict['SHOCKS']['eps'] = {}

        initDict['SHOCKS']['eps']['value'] = None

        initDict['SHOCKS']['eps']['free'] = None


        initDict['SHOCKS']['eta'] = {}

        initDict['SHOCKS']['eta']['value'] = None
        
        initDict['SHOCKS']['eta']['free'] = None
        
        
        initDict['SHOCKS']['rho'] = {}

        initDict['SHOCKS']['rho']['value'] = None
        
        initDict['SHOCKS']['rho']['free'] = None
        
        # Finishing.
        return initDict
    
    def _standardize(self):
        ''' Standardize initialization file.
        '''
        # Distribute class attributes.
        initDict = self.attr['initDict']
        
        str_ = '\t {0:<8}{1:<8}\t{2:<8}\n'
        
        with open('.model.struct.ini', 'wt') as fout:
    
            # Observed, Environment.
            for key_ in ['OBSERVED', 'ENVIRO']:

                if(key_ == 'OBSERVED'): label = 'OBSERVED'
                
                if(key_ == 'ENVIRO'):   label = 'ENVIRONMENT'
                
                fout.write('\n ' + label + '\n\n')
                
                for name in initDict[key_].keys():
                    
                    pos = initDict[key_][name]
                    
                    fout.write(str_.format(name, '', pos))
            
            # Utility.
            fout.write('\n UTILITY \n\n')
            
            pos    = initDict['UTILITY']['child']['pos'][0]
            
            isFree = initDict['UTILITY']['child']['free'][0]
                        
            info   = initDict['UTILITY']['child']['value'][0]
            
            if(not isFree): info = '!' + str(info)
                        
            fout.write(str_.format('child', pos, info))
            
            fout.write('\n')
            
            for subtype in ['coeffs', 'int']:
        
                values = initDict['UTILITY'][subtype]['value']
                
                isFree = initDict['UTILITY'][subtype]['free'] 
                                
                for count, info in enumerate(values):
                    
                    pos = ''
                    
                    if(subtype == 'coeffs'): 
                        
                        pos = initDict['UTILITY'][subtype]['pos'][count]
                    
                    if(not isFree[count]): info = '!' + str(info)                   
                    
                    label = subtype.replace('s', '')
                    
                    fout.write(str_.format(label, pos, info))
            
                fout.write('\n')
                            
            # Utility.
            fout.write('\n WAGE \n\n')
            
            pos    = initDict['WAGE']['exper']['pos'][0]
            
            isFree = initDict['WAGE']['exper']['free'][0]
                        
            info   = initDict['WAGE']['exper']['value'][0]
            
            if(not isFree): info = '!' + str(info)
                        
            fout.write(str_.format('exper', pos, info))
            
            fout.write('\n')
                        
            for subtype in ['coeffs', 'int']:
        
                values = initDict['WAGE'][subtype]['value']
                
                isFree = initDict['WAGE'][subtype]['free'] 
                                
                for count, info in enumerate(values):
                    
                    pos = ''
                    
                    if(subtype == 'coeffs'): 
                        
                        pos = initDict['WAGE'][subtype]['pos'][count]
                    
                    if(not isFree[count]): info = '!' + str(info)                   
                    
                    label = subtype.replace('s', '')
                    
                    fout.write(str_.format(label, pos, info))
                
                fout.write('\n')
                            
            # Shocks 
            fout.write('\n SHOCKS \n\n')
            
            for name in ['eps', 'eta', 'rho']:
                
                info   = initDict['SHOCKS'][name]['value']
                
                isFree = initDict['SHOCKS'][name]['free']
                
                if(not isFree): info = '!' + str(info)
                
                fout.write(str_.format(name, '', info))
                                                
            # Estimation, Simulation, Optimization.
            str_ = '\t {0:<15}\t{1:<8}\n'
                    
            for key_ in ['EST', 'SIM', 'OPT']:
                
                if(key_ == 'EST'): label = 'ESTIMATION'
                
                if(key_ == 'SIM'): label = 'SIMULATION'
                
                if(key_ == 'OPT'): label = 'OPTIMIZATION'
                
                fout.write('\n ' + label + ' \n\n')
                
                for name in initDict[key_].keys():
                    
                    info = str(initDict[key_][name])

                    fout.write(str_.format(name, info))
                    
        shutil.move('.model.struct.ini', 'model.struct.ini') 
        