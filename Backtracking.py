from Constraint import *
from Consistent import *
from Inferences import *
from Order  import NodeOrder, ValueOrder
from copy   import deepcopy

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')

class BacktrackingSearch:
    def __init__(self,csp,NodeOrdering,ValueOrdering,InferenceName):
        self.csp        = csp
        self.NodeOrder  = NodeOrder(self.csp, NodeOrdering)
        self.ValueOrder = ValueOrder(self.csp, ValueOrdering)
        self.Inference  = Inference(self.csp, InferenceName)
        self.Consistent = Consistent()
    
    def run(self,csp):
        solution = self.Backtrack(csp)
        if solution == None:
            print("Failed")
        else:
            printDomains(solution)
        
    def Backtrack(self,csp):
        if self.isComplete(csp):
            return csp.variables
        var = self.NodeOrder.pop(csp)
        for value in self.ValueOrder.get(var, csp):
            previous           = dict()
            previous[var.name] = self.copy(csp.variables[var.name])
            csp.variables[var.name].domain = [value]
            if self.isConsistent(var, csp):
                inferences = self.Inference.get(csp, var)
                if inferences != None:
                    self.add(csp.variables, inferences, previous)
                    result = self.Backtrack(csp)
                    if result != None:
                        return result
            self.revert(csp.variables, previous)
        self.NodeOrder.push(csp,var)
        return None
    
    def copy(self, variable):
        return ConstraintVar(list(variable.domain), variable.name)
    
    def revert(self, variables, previous):
        for key in previous:
            variables[key].domain = list(previous[key].domain)
            
    def add(self, variables, inferences, previous):
        for key in inferences:
            previous[key]           = self.copy(variables[key])
            variables[key].domain   = list(inferences[key].domain)
        
    def isConsistent(self, variable, csp):
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if not self.Consistent.evaluate(variable, constraint):
                    #print("faileddddd")
                    return False
        return True
    
    def isComplete(self, csp):
        for constraint in csp.constraints:
            if not constraint.complete():
                return False
        for key   in csp.variables:
            if len(csp.variables[key].domain) != 1:
                return False
        return True
    
