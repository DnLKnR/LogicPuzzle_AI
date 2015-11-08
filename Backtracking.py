from Constraint import *
from Consistent import *
from Order  import NodeOrder, ValueOrder
from copy   import deepcopy

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
        variable = self.NodeOrder.get(reset=True)
        for value in self.ValueOrder.get(variable,csp):
            previous                     = dict()
            previous[variable.name]      = csp.variables[variable.name]
            csp.variables[variable.name] = [value]
            
            if self.isConsistent(variable, csp):
                inferences = self.Inference.get()
                if inferences != None:
                    self.add(csp.variables, inferences, previous)
                    result = self.Backtrack(csp)
                    if result != None:
                        return result
            self.revert(csp.variables, previous)
        return None
    
    def revert(self, variables, previous):
        for key in previous.iterkeys():
            variables[key] = previous[key]
            
    def add(self, variables, inferences, previous):
        for key in inferences.iterkeys():
            previous[key]   = variables[key]
            variables[key]  = inferences[key]
        
    def isConsistent(self, variable, csp):
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if not self.Consistent.evaluate(variable, constraint):
                    return False
        return True
    
    def isComplete(self, csp):
        for constraint in csp.constraints:
            if not constraint.complete():
                return False
        for variable   in csp.variables:
            if len(variable.domain) != 1:
                return False
        return True
    
