from Constraint import *
from AC3        import *

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
    def noOrder(self, var, assignment, csp):
        return var.domain
    
    def randomOrder(self, var, assignment, csp):
        return var.domain
    
    def leastConstrainingOrder(self, var, assignment, csp):
        min = 1000000000
        var = ""
        for key in csp.variables.iterkeys():
            length = len(csp.variables[key])
            if min > length:
                var,max = key,length
        return var
    
    ## UTILITY FUNCTIONS, 
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS   
    def get(self, var, assignment, csp):
        self.function(var, assignment, csp)



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
            
        self.queue = self.function(csp)

    ## NODE ORDERING FUNCTIONS (BELOW)
    ## THESE SHOULD NEVER DIRECTLY BE CALLED OUTSIDE OF THE CLASS  
    def randomOrder(self, csp):
        pass

    def noOrder(self, csp):
        pass

    def minimumRemainingValuesOrder(self, csp):
        queue = []
        for key in csp.variables.iterkeys():
            queue.append(csp.variables[key])
        queue = sorted(queue, key=lambda x: len(x.domain))
        return queue

    def degreeOrder(self, csp):
        pass
    
    ## UTILITY FUNCTIONS, 
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS
    def get(self,index,reset=False):
        if reset:
            self.queue = self.function(csp)
        return self.queue[index]
        
    def pop(self,index=0,reset=False):
        if reset:
            self.queue = self.function(csp)
        return self.queue.pop(index)
        
    
    
        