''' Module that contains the parameter class.
'''

# standard library
import numpy as np

# project library
from tools.clsMeta  import meta
from clsPara        import paraCls

class parasCls(meta):
    ''' Class that holds the full set of parameters involved in the 
        maximization routine.
    '''
    def __init__(self):
        
        self.attr = {}
        
        self.attr['paraObjs'] = []
   
        # Derived attributes.     
        self.attr['dict']     = None  
   
        self.attr['numFree']  = 0
 
        self.attr['numParas'] = 0
   
        # Status attributes.
        self.isLocked = False
        
    def getParameters(self, request):
        ''' Get parameters.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        dict_ = self.attr['dict']

        # Return.
        return dict_[request]

    def addParameter(self, type_, subtype, value, isFree = None):
        ''' Add a parameter.
        '''
        # Antibugging
        assert (isFree in [True, False, None])
        
        # Default restriction.
        rest = ['free', (None, None)] 
        
        # Automatic restrictions
        if(subtype in ['subsidy', 'cost']):
            
            rest = ['fixed', (None, None)]   
                
        if(subtype in ['eps', 'eta']):

            rest = ['range', (0.01, None)] 
            
        if(subtype in ['rho']):

            rest = ['range', (-1.0, 1.0)] 
        
        # Fixed parameters.
        if(not isFree): rest = ['fixed', (None, None)]           
                
        if(rest[0] != 'fixed'):
            
            self.attr['numFree'] = self.attr['numFree'] + 1
        
        # Initialize.
        paraObj = paraCls()

        paraObj.setAttr('type', type_)

        paraObj.setAttr('subtype', subtype)

        paraObj.setAttr('start', value)

        paraObj.setAttr('rest', rest)
                
        paraObj.lock()

        # Collect.           
        self.attr['paraObjs'].append(paraObj)
        
    ''' Methods: Updating parameter objects.
    '''   
    def getValues(self, version, which):
        ''' Get all current values.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (version in ['external', 'internal'])
        assert (which in ['free', 'all'])
        
        # Distribute class attributes.
        paraObjs = self.attr['paraObjs']

        # Collect parameters.
        x = []
        
        for paraObj in paraObjs:
            
            # Check applicability/
            isFree = paraObj.getAttr('update')
            
            if(which == 'free' and (isFree == False)): continue
            
            # Collect values.
            value = paraObj.getAttr('value')
                
            if(version == 'external'):
                    
                value = self._transformToExternal(paraObj, value)
                
            x.append(value)
        
        # Type conversion
        x = np.array(x)
        
        # Finishing.
        return x
    
    def update(self, x, version, which):
        ''' Update all free parameters.
        '''
        # Antibugging.
        assert (which in ['all', 'free'])
        assert (self.getStatus() == True)
        assert (isinstance(x, np.ndarray))
        assert (np.all(np.isfinite(x)))
        assert (x.dtype == 'float')
        assert (version in ['external', 'internal'])
       
        if(which == 'free'): assert (x.shape == (self.attr['numFree'],))
        
        # Distribute class attributes.
        paraObjs = self.getAttr('paraObjs')
        
        # Update parameters.
        updates, counter = [], 0     
        
        for paraObj in paraObjs:
           
            # Check applicability.
            isFree = paraObj.getAttr('update')
            
            if((isFree == False) and (which == 'all')):
                
                assert (paraObj.getAttr('value') == x[counter])
                
                counter = counter + 1
            
            # Processing.
            if(isFree): 

                value = x[counter]
                
        
                if(version == 'external'):
                    
                    value = self._transformToInternal(paraObj, value)
                       
        
                paraObj.setValue(value)

                
                counter = counter + 1

            updates.append(paraObj)
            
        # Update.
        self.attr['paraObjs'] = updates
        
        self._updateDictionary()
          
    def _clipInternalValue(self, paraObj, internalValue):
        ''' Assure that internal value not exactly equal to bounds.
        
        '''
        # Antibugging.
        assert (isinstance(paraObj, paraCls))
        assert (isinstance(internalValue, float))
        assert (np.isfinite(internalValue))
        assert (paraObj.attr['rest'][0] in ['free', 'range'])     
                
        # Auxiliary objects.
        lowerBound, upperBound = paraObj.attr['bounds']
        
        hasLowerBound = (lowerBound is not None)
        hasUpperBound = (upperBound is not None)
        
        # Check bounds.
        if(hasLowerBound):
            
            if(internalValue == lowerBound): internalValue += 0.01

        if(hasUpperBound):
            
            if(internalValue == upperBound): internalValue -= 0.01

        # Quality Check.
        assert (isinstance(internalValue, float))
        assert (np.isfinite(internalValue))
        
        if(hasLowerBound): assert (lowerBound < internalValue) 
        if(hasUpperBound): assert (upperBound > internalValue) 
            
        # Finishing.
        return internalValue
       
    def _transformToExternal(self, paraObj, internalValue):
        ''' Transform internal paraObj for external use by maximization 
            routine.
            
        '''
        # Antibugging.
        assert (isinstance(paraObj, paraCls))
        assert (isinstance(internalValue, float))
        assert (np.isfinite(internalValue))
        assert (paraObj.attr['rest'][0] in ['free', 'range'])        
        
        # Auxiliary objects.
        lowerBound, upperBound = paraObj.attr['bounds']
        
        hasLowerBound = (lowerBound is not None)
        hasUpperBound = (upperBound is not None)
        
        # Stabilization
        internalValue = self._clipInternalValue(paraObj, internalValue)
        
        # Lower bound only.
        if((hasLowerBound) and (not hasUpperBound)):
     
            externalValue = np.log(internalValue - lowerBound)
        
        # Upper bound only.
        elif((not hasLowerBound) and (hasUpperBound)):
                    
            externalValue =  np.log(upperBound - internalValue)
        
        # Upper and lower bounds.
        elif(hasLowerBound and hasUpperBound):
            
            interval  = upperBound - lowerBound
            transform = (internalValue - lowerBound)/interval
            
            externalValue =  np.log(transform/(1.0 - transform))
        
        # No bounds.
        else:
            
            externalValue = internalValue
            
        # Quality Check.
        assert (isinstance(externalValue, float))
        assert (np.isfinite(externalValue))
        
        # Finishing.
        return externalValue
   
    def _transformToInternal(self, paraObj, externalValue):
        ''' Transform externalValues to internal paraObj.
        
        '''
        # Antibugging.
        assert (isinstance(paraObj, paraCls))
        assert (isinstance(externalValue, float))
        assert (np.isfinite(externalValue))
        assert (paraObj.attr['rest'][0] in ['free', 'range'])
        
        # Auxiliary objects.
        lowerBound, upperBound = paraObj.attr['bounds']
        
        hasLowerBound = (lowerBound is not None)
        hasUpperBound = (upperBound is not None)
        
        # Stabilization.
        hasBounds = (hasLowerBound or hasUpperBound)
        
        if(hasBounds):
            
            externalValue = np.clip(externalValue, None, 10)
        
        # Lower bound only.
        if((hasLowerBound) and (not hasUpperBound)):
            
            internalValue = lowerBound + np.exp(externalValue)
            
        # Upper bound only.
        elif((not hasLowerBound) and (hasUpperBound)):
            
            internalValue = upperBound - np.exp(externalValue)
      
        # Upper and lower bounds.
        elif(hasLowerBound and hasUpperBound):
            
            interval      = upperBound - lowerBound
            internalValue = lowerBound + interval/(1.0 + np.exp(-externalValue)) 

        # No bounds.
        else:
            
            internalValue = externalValue

        # Stabilization.
        internalValue = self._clipInternalValue(paraObj, internalValue)

        # Quality Check.
        assert (isinstance(internalValue, float))
        assert (np.isfinite(internalValue))
        
        # Finishing.
        return internalValue

    ''' Other private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        self.attr['numParas'] = len(self.attr['paraObjs'])
        
        # Update dictionary.
        self._updateDictionary()
        
    def _updateDictionary(self):
        ''' Prepare dictionary.
        '''
        # Antibugging.
        assert (self.getStatus() == True)

        # Initialize container.        
        dict_ = {}
    

        dict_['child']      = None
        
        dict_['cost']       = None

        dict_['subsidy']    = None

        dict_['experience'] = None


        dict_['utility'] = {}

        dict_['utility']['coeffs'] = None
        
        dict_['utility']['int']    = None
        
        
        dict_['wage'] = {}

        dict_['wage']['coeffs'] = None
        
        dict_['wage']['int']    = None        


        dict_['shocks'] = None

        dict_['xi'] = None


        dict_['eps'] = None

        dict_['eta'] = None
        
        dict_['rho'] = None


        dict_ = self._originalParameters(dict_); self.attr['dict'] = dict_
        
        dict_ = self._derivedParameters(dict_) ; self.attr['dict'] = dict_
        
    def _derivedParameters(self, dict_):
        ''' Construct dictionary with derived parameters.
        '''
        # Select ingredients.
        cov = dict_['shocks']
            
        # Construct output.
        eps = {}
            
        eps['sd']   = np.sqrt(cov[0,0])
                
        eps['mean'] = 0.00
            
        # Finished.
        dict_['eps'] =  eps

        # Select ingredients.
        cov = dict_['shocks']
            
        # Construct output.
        eta = {}
            
        eta['sd']   = np.sqrt(cov[1,1])
                
        eta['mean'] = 0.00

        # Finished.            
        dict_['eta'] = eta
  
  
        cov = dict_['shocks']
            
        eps = dict_['eps']
            
        eta = dict_['eta']
                       
        rho = cov[1,0]/(eps['sd']*eta['sd'])
        
        dict_['rho'] = rho
        
        ''' Xi
        ''' 
        # Select ingredients.
        eps = self.getParameters('eps')
            
        eta = self.getParameters('eta')
            
        rho = self.getParameters('rho')
            
        # Construct output.
        xi = {}
           
        xi['sd']   = np.sqrt(eps['sd']**2 + eta['sd']**2 - 2*rho*eps['sd']*eta['sd'])
                
        xi['mean'] = 0.0
                       
            
        xi['cov'] = {}
            
        xi['cov']['eta'] =  eta['sd']**2 -  dict_['shocks'][1,0]
        xi['cov']['eps'] = -eps['sd']**2 + rho*eps['sd']*eta['sd']
                
            
        xi['rho'] = {}
            
        xi['rho']['eta'] = xi['cov']['eta']/(xi['sd']*eta['sd'])   

        xi['rho']['eps'] = xi['cov']['eps']/(xi['sd']*eps['sd'])   
        
        
        dict_['xi'] = xi

        # Finished.
        return dict_
        
    def _originalParameters(self, dict_):
        ''' Construct dictionary with original parameters.
        '''
        paraObjs = self.attr['paraObjs']
        
        ''' Cost, Subsidy, Child
        '''
        for key_ in ['cost', 'subsidy', 'discount']:
            
            for paraObj in paraObjs:
                        
                type_ = paraObj.getAttr('type')
         
                if(type_ != 'BASICS'): 
                            
                    continue
                        
                else:
                        
                    subtype = paraObj.getAttr('subtype')
                        
                    value   = paraObj.getAttr('value')
                    
                    if(subtype == key_):
                      
                        dict_[key_] = value
                        
        for key_ in ['child', 'experience']:
            
            tag = key_.upper()
            
            for paraObj in paraObjs:
                
                type_ = paraObj.getAttr('type')
         
                if(type_ != tag): 
                            
                    continue
                        
                else:
                   
                    value   = paraObj.getAttr('value')
                    
                    dict_[key_] = value
                                    
        ''' Shocks
        '''
        rslt = []
            
        for request in ['eps', 'eta', 'rho']:
                
            for paraObj in paraObjs:
                    
                subtype = paraObj.getAttr('subtype') 

                if(subtype != request): 
                        
                    continue
                    
                else:
                        
                    value = paraObj.getAttr('value')
                        
                    rslt = rslt + [value] 
        
        rslt[2] = rslt[2]*rslt[0]*rslt[1]
          
        cov = np.array([[rslt[0]**2, rslt[2]],[rslt[2], rslt[1]**2]])
        
        dict_['shocks'] = cov
        
        ''' Wages
        '''
        for key_ in ['wage', 'utility']:
        
            tag = key_.upper()
            
            coeffs, int_ = [], None
                    
            for paraObj in paraObjs:
                            
                type_ = paraObj.getAttr('type')
                 
                if(type_ != tag): 
                                
                    continue
                            
                else:
                            
                    subtype = paraObj.getAttr('subtype')
                            
                    value   = paraObj.getAttr('value')
             
           
                    if(subtype == 'coeffs'): coeffs = coeffs + [value]
                            
                    if(subtype == 'int'):    int_   = value
                
                            
            dict_[key_] = (np.array(coeffs, ndmin = 2), int_)
     
        return dict_