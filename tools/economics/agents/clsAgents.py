''' Module that contains the agents class.
'''
# project library
from tools.clsMeta  import meta

import tools.computation.performance.performance    as perf

class agentCls(meta):
    ''' Class instance that represents the agent.
    '''    
    def __init__(self):
        
        self.attr = {}
      
        # Exogenous attributes.
        self.attr['attr']    = {}

        self.attr['attr']['experience'] = None

        self.attr['attr']['children']   = None
        
        self.attr['attr']['utility']    = None

        self.attr['attr']['spouse']     = None
                
        self.attr['attr']['wage']       = None
                
        # Economic Environment.
        self.attr['parasObj'] = None

        self.attr['treeObj']  = None
        
        # Endogenous objects.
        self.attr['u'] = {}

        self.attr['u']['exAnte']  = {}

        self.attr['u']['exPost']  = {}


        self.attr['v'] = {}

        self.attr['v']['exAnte']  = {}



        self.attr['w'] = {}

        self.attr['w']['exAnte']  = {}


        self.attr['emax']     = {}

        self.attr['probs']    = {}
                
                
        # Histories.
        self.attr['wages']    = []

        self.attr['choices']  = []
        
        self.attr['states']   = ['0']
                    
        # Positions.
        self.attr['steps']    = 0

        self.attr['position'] = '0'

        # Status indicator.
        self.isLocked = False
        
    ''' Public methods.
    '''
    def step(self):
        ''' Step through period
        '''
        # Antibugging.
        assert (self.getStatus() == True)
      
        # Draw random components.
        eps, eta = self._drawShocks()

        # Update work experience
        self._update()

        # Calculate wages.
        wage = self._wage(eta)
        
        # Calculate utilities.
        str_ = self.attr['position']
      
        working = self.attr['v']['exAnte'][str_ + '1'] + eta

        home    = self.attr['v']['exAnte'][str_ + '0'] + eps
        
        # Determine state.
        state = 0       
        
        if(working > home): state = 1

        self.attr['choices'] = self.attr['choices'] + [state] 
                
        # Collect information.
        self.attr['wages'] = self.attr['wages'] + [wage] 
        
        if(working < home): self.attr['wages'][-1] = perf.nan
        
        # Count steps.
        self.attr['steps'] = self.attr['steps'] + 1
        
        # Update position.
        self.attr['position'] = self.attr['position'] + str(state)
        
        self.attr['states'] =  self.attr['states'] + [self.attr['position']]
         
    ''' Private methods.
    '''
    def _derivedAttributes(self):
        ''' Construct derived attributes.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        self._evaluateNodes()

    def _evaluateNodes(self):
        ''' Evaluate nodes for current parametrization.
        '''
        # Distribute class attributes.
        treeObj  = self.attr['treeObj']

        # Auxiliary objects.
        depths = treeObj.getAttr('allDepths')
        
        # Backward induction.
        for depth in reversed(depths):
            
            if(depth == 0): continue
            
            nodes = treeObj.getAttr('nodeDepths')[depth]
               
            for node in nodes:
                
                self._calculateU(node)
                
                self._calculateProbs(node)
                
                self._calculateEmax(node)
                
                self._calculateV(node)
                
    def _calculateU(self, node):
        ''' Calculate the instantaneous utility.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (node.getStatus() == True)
      
        # Distribute auxiliary objects.                
        parasObj = self.attr['parasObj']

        # Auxiliary objects.
        name = node.getAttr('name')
        
        t    = len(name) - 2

        # Attributes.
        spouse   = self.attr['attr']['spouse'][t]
            
        children = self.attr['attr']['children'][t]
                 
        # Initialize containers.
        self.attr['w']['exAnte'][name] = perf.nan
         
        # Compute relevant utility. 
        if(name[-1] == '1'):
            
            cost    = parasObj.getParameters('cost')
                
            subsidy = parasObj.getParameters('subsidy')
            
            # Process wage.
            attr         = self.getAttr('attr')['wage'][t]
            
            coeffs, int_ = parasObj.getParameters('wage')
            
            idxWage      = perf.dot(attr, coeffs.T) + int_
                                       
            # Returns to experience.
            exp    = name[:-1].count('1')
                           
            coeffs = parasObj.getParameters('experience')
                    
            wage   = idxWage + coeffs*exp
            
            # Collect information.
            self.attr['w']['exAnte'][name] = wage
            
            self.attr['u']['exAnte'][name] = spouse + wage - (cost - subsidy)*children   
            
        else:
            
            # Process utilities.
            attr         = self.attr['attr']['utility'][t]
                    
            coeffs, int_ = parasObj.getParameters('utility')
            
            idxUtility   = perf.dot(attr, coeffs.T) + int_ 

            # Pleasure of children.
            coeffs     = parasObj.getParameters('child')
                    
            idxUtility = idxUtility + perf.dot(children, coeffs) 
            
            # Collect information
            self.attr['u']['exAnte'][name] = spouse + idxUtility              
        
        # Type conversion.
        self.attr['u']['exAnte'][name] = float(self.attr['u']['exAnte'][name])

    def _calculateProbs(self, node):
        ''' Calculate probabilities.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (node.getStatus() == True)       

        # Check applicability.
        if(node.getAttr('isTerminal')): return
                
        # Distribute attributes.
        parasObj = self.attr['parasObj']
        
        # Auxiliary objects.        
        xi = parasObj.getParameters('xi')
        
        
        names = {}
        
        names['upper'] = node.getAttr('upper').getAttr('name')

        names['lower'] = node.getAttr('lower').getAttr('name')        


        v = {}
        
        v['upper'] = self.attr['v']['exAnte'][names['upper']]

        v['lower'] = self.attr['v']['exAnte'][names['lower']]
            
                        
        prob = perf.norm_cdf(-(v['upper'] - v['lower']), 0.0, xi['sd'])
        
        self.attr['probs'][names['upper']] = 1.0 - prob 

        self.attr['probs'][names['lower']] = prob 

    def _calculateEmax(self, node):
        ''' Calculate the EMAX.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (node.getStatus() == True)
      
        # Distribute attributes.
        name     = node.getAttr('name')
        
        parasObj = self.attr['parasObj']
        
        # Check applicability.
        self.attr['emax'][name] = 0.0
        
        if(node.getAttr('isTerminal')): return
        
        # Calculate expected future values.    
        names = {}
        
        names['upper'] = node.getAttr('upper').getAttr('name')
    
        names['lower'] = node.getAttr('lower').getAttr('name')
    
    
        probs = {}
    
        probs['upper'] = self.attr['probs'][names['upper']]
    
        probs['lower'] = self.attr['probs'][names['lower']]
      
      
        v = {}
            
        v['upper'] = self.attr['v']['exAnte'][names['upper']]
            
        v['lower'] = self.attr['v']['exAnte'][names['lower']]
        
        
        eps, eta = self._conditionalExpectations(parasObj, v)
                
        self.attr['emax'][name]= probs['upper']*(v['upper'] + eta) \
                + probs['lower']*(v['lower'] + eps)
                                                                   
    def _calculateV(self, node):
        ''' Calculate value function.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        assert (node.getStatus() == True)       
        
        # Distribute attributes.
        parasObj = self.attr['parasObj']
    
        # Auxiliary objects.
        discount = parasObj.getParameters('discount')
        
        name     = node.getAttr('name')

        # Calculate ex-ante value Function.
        self.attr['v']['exAnte'][name] = self.attr['u']['exAnte'][name] + discount*self.attr['emax'][name]

    def _conditionalExpectations(self, parasObj, v):
        ''' Calculate the conditional expectation of the unobservables 
            for each alternative choice.
        '''
        def conditionalExpectation(self, u, v, rho, cutoff, direction):
            ''' Calculate the conditional expectation
            '''
            
            eval_ = (cutoff - v['mean'])/v['sd']
            
            cdf   = perf.norm_cdf(eval_, 0.00, 1.0)
            
            pdf   = perf.norm_pdf(eval_, 0.00, 1.0)
            
            # Stabilization
            cdf   = perf.clip(cdf, 1e-10, 1.0 - 1e-10)
            
            # Request.
            if(direction == 'lower'):
        
                rslt = u['mean'] - rho*u['sd']*(pdf/cdf)
        
            if(direction == 'upper'):
                
                rslt = u['mean'] + rho*u['sd']*(pdf/(1.0 - cdf))
        
            # Finishing.
            return rslt
        
        # Distribute information
        xi  = parasObj.getParameters('xi')
    
        eps = parasObj.getParameters('eps')
    
        eta = parasObj.getParameters('eta')
                
        # Calculate auxiliary objects.
        eval_ = v['upper'] - v['lower']
        
        # Compute expectations.
        rho = xi['cov']['eps']/(xi['sd']*eps['sd'])
        
        eps = conditionalExpectation(self, eps, xi, rho, eval_, 'lower')
        
           
        rho = xi['cov']['eta']/(xi['sd']*eta['sd'])
        
        eta = conditionalExpectation(self, eta, xi, rho, eval_, 'upper')
        
        # Quality checks.
        assert (perf.isfinite(eps))
        assert (perf.isfinite(eta))
            
        # Finishing.
        return eps, eta

    def _update(self):
        ''' Update work experience.
        ''' 
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        steps = self.attr['steps']

        # Update information.
        if(steps > 0):

            experience = self.attr['attr']['experience'][-1]

            choice     = self.attr['choices'][-1]
            
            experience = experience + choice


            self.attr['attr']['experience'] = self.attr['attr']['experience'] + [experience]

    def _wage(self, eta):
        ''' Calculate wage offer.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        steps    = self.attr['steps']
        
        parasObj = self.attr['parasObj']

        attr     = self.attr['attr']['wage'][steps]
        
        exp      = self.attr['attr']['experience'][-1]
        
        # Calculate wage.
        coeffs, int_ = parasObj.getParameters('wage')

        wage         = perf.dot(attr, coeffs.T) + int_ + eta
        
        
        coeffs       = parasObj.getParameters('experience')
        
        wage         = wage + coeffs*exp
        
        # Type conversion
        wage = float(wage)
        
        # Finishing.
        return wage

    def _drawShocks(self):
        ''' Draw shocks.
        '''
        # Antibugging.
        assert (self.getStatus() == True)
        
        # Distribute class attributes.
        parasObj = self.attr['parasObj']
        
        # Draw disturbances.
        cov = parasObj.getParameters('shocks')
        
        eps, eta = perf.random_multivariate_normal(mean = [0.0, 0.0], cov = cov)
        
        # Finishing.
        return eps, eta