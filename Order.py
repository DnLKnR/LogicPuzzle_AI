from Constraint import *


## Domain Value Ordering functions for Backtracking Search ##
class ValueOrder:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order
        if self.order in ["LCV", "LeastConstrainingValueOrder"]:
            self.function = self.leastConstrainingValueOrder
        elif self.order in ["RandomValue","Random"]:
            self.function = self.randomValueOrder
        else:
            self.function = self.noValueOrder
        
        
    def noValueOrder(self, var, assignment, csp):
        return var.domain
    
    def randomValueOrder(self, var, assignment, csp):
        return var.domain
    
    def leastConstrainingValueOrder(self, var, assignment, csp):
        min = 1000000000
        var = ""
        for key in csp.variables.iterkeys():
            length = len(csp.variables[key])
            if min > length:
                var,max = key,length
        return var
        
    def generateOrder(self, var, assignment, csp):
        self.function(var, assignment, csp)



## Node Ordering functions for Backtracking Search ##
class NodeOrder:
    def __init__(self,csp,order):
        self.csp    = csp
        self.order  = order
        if order == "MRV":
            self.queue = self.MinimumRemainingValues(csp)
        elif order == "RandomOrder":
            self.queue = self.RandomOrder(csp)
        elif order == "Degree":
            self.queue = self.Degree(csp)
        else:
            self.queue = self.NoOrder(csp)
        
    def RandomOrder(self, csp):
        pass

    def NoOrder(self, csp):
        pass

    def MinimumRemainingValues(self, csp):
        minimum = -1
        varKey = ""
        for key in csp.variables.iterkeys():
            length = len(csp.variables[key])
            if minimum < length or minimum == -1:
                varKey  = key
                minimum = length
        if minimum == -1:
            return None
        else:
            return csp.variables[key]
    

    def Degree(self, csp):
        
        pass
    
    def get(self,index):
        return self.queue[index]
        
    def pop(self,index):
        return self.queue.pop(index)
        