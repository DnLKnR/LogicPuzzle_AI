from Constraint import *

## Domain Value Ordering functions for Backtracking Search ##
class ValueOrder:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order.replace(' ','').lower()
        if self.order in ["lcv", "leastconstrainingvalue"]:
            self.function = self.leastConstrainingOrder
        elif self.order in ["r","random"]:
            self.function = self.randomOrder
        else:
            self.function = self.noOrder
        
    ## VALUE ORDERING FUNCTIONS (BELOW)
    ## THESE SHOULD NEVER DIRECTLY BE CALLED OUTSIDE OF THE CLASS   
    def noOrder(self, var, csp):
        return var.domain
    
    def randomOrder(self, var, csp):
        return var.domain
    
    def leastConstrainingOrder(self, var, csp):
        #=======================================================================
        # min = 1000000000
        # for key in csp.variables:
        #     length = len(csp.variables[key])
        #     if min > length:
        #         max = length
        #=======================================================================
        return var.domain
    
    ## UTILITY FUNCTIONS, 
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS   
    def get(self, var, csp):
        return self.function(var, csp)



## Node Ordering functions for Backtracking Search ##
class NodeOrder:
    def __init__(self,csp,order):
        self.csp    = csp
        self.order  = order.replace(' ','').lower()
        if order in ["mrv","minimumremainingvalues"]:
            self.function = self.minimumRemainingValuesOrder
        elif order in ["r","random"]:
            self.function = self.randomOrder
        elif order in ["d","degree"]:
            self.function = self.degreeOrder
        else:
            self.function = self.noOrder
            
        self.function(csp,True)

    ## NODE ORDERING FUNCTIONS (BELOW)
    ## THESE SHOULD NEVER DIRECTLY BE CALLED OUTSIDE OF THE CLASS  
    def randomOrder(self,csp,create=False):
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])

    def noOrder(self,csp,create=False):
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])

    def minimumRemainingValuesOrder(self,csp,create=False):
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])
        
        self.queue = sorted(self.queue, key=lambda x: len(x.domain))

    def degreeOrder(self, csp):
        pass
    
    ## UTILITY FUNCTIONS, 
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS
    def get(self,csp,index=0,reset=False):
        self.function(csp,reset)
        return self.queue[index]
        
    def pop(self,csp,index=0,reset=False):
        self.function(csp,reset)
        return self.queue.pop(index)
    
    def push(self,csp,var,index=0,reset=False):
        self.queue.insert(0,var)
        self.function(csp,reset)
        
        
    
    
        