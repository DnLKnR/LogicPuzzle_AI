from Constraint import *

## These functions have to return a list ##

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