from Constraint import *
from Consistent import *
from Inferences import *
from Order  import NodeOrder, ValueOrder
from copy   import deepcopy
import functools
from functools import reduce

class BacktrackingSearch:
    def __init__(self,csp,NodeOrdering,ValueOrdering,InferenceName):
        self.csp        = csp
        self.NodeOrder  = NodeOrder(self.csp, NodeOrdering)
        self.ValueOrder = ValueOrder(self.csp, ValueOrdering)
        self.Inference  = Inference(self.csp, InferenceName)
        self.Consistent = Consistent()
    
    def run(self,csp):
        '''Execute backtracking search on the constraint satisfaction
           object that contains the initial start of the problem'''
        solution = self.Backtrack(csp)
        if solution == None:
            print("No Solution Exists")
        else:
            self.printDomains(solution)
        
    def Backtrack(self,csp):
        '''Recursive Backtracking search, built around the pseudocode
           that is presented on page 215 in Artificial Intelligence:
           A Modern Approach textbook'''
        if self.isComplete(csp):
            return csp.variables
        var = self.NodeOrder.pop(csp)
        for value in self.ValueOrder.get(var, csp):
            previous = dict()
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
        '''undo the changes made to the variables list by re-adding
           the values that are stored in the previous dictionary'''
        for key in previous:
            variables[key].domain = list(previous[key].domain)
            
    def add(self, variables, inferences, previous):
        '''add the inferences onto the variables dictionary and store
           the old values in previous in case they need to be undone'''
        for key in inferences:
            previous[key]           = self.copy(variables[key])
            variables[key].domain   = list(inferences[key].domain)
        
    def isConsistent(self, variable, csp):
        '''check if the variable is consistent with all constraints
           Note: in this case, we only care that the variable is
           consistent.  No domains will be altered'''
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if not self.Consistent.evaluate(variable, constraint):
                    return False
        return True
    
    def isComplete(self, csp):
        '''check through all the constraints in the constraint satisfaction
           problem to make sure that they are all met.  Also, make sure that
           every variable has a domain of only one.  This prevents giving
           multiple solutions.  We only want one solution'''
        for constraint in csp.constraints:
            if not constraint.complete():
                return False
        for key in csp.variables:
            if len(csp.variables[key].domain) != 1:
                return False
        return True
    
    def printDomains(self, vars, n=3 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k].domain,'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')