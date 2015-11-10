from Constraint import *
from Consistent import *
from Inferences import *
from Order  import NodeOrder, ValueOrder
from copy   import deepcopy
import functools
from functools import reduce

class BacktrackingSearch:
    def __init__(self,csp,NodeOrdering,ValueOrdering,InferenceName, sort=True):
        self.csp        = csp
        if sort: csp.sort()
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
        '''Recursive Backtracking search, built around the pseudo-code
           that is presented on page 215 in Artificial Intelligence:
           A Modern Approach textbook'''
        if self.isComplete(csp):
            return csp.variables
        var = self.NodeOrder.pop(csp)
        for value in self.ValueOrder.get(var, csp):
            previous = dict()
            previous[var.name] = csp.variables[var.name].copy()
            csp.variables[var.name].domain = [value]
            if self.Consistent.evaluate(var, csp):
                inferences = self.Inference.get(csp, var)
                if inferences != None:
                    self.add(csp.variables, inferences, previous)
                    result = self.Backtrack(csp)
                    if result != None:
                        return result
            self.revert(csp.variables, previous)
        self.NodeOrder.push(csp,var)
        return None
    
    def revert(self, variables, previous):
        '''undo the changes made to the variables list by re-adding
           the values that are stored in the previous dictionary'''
        for key in previous:
            variables[key].domain = list(previous[key].domain)
            
    def add(self, variables, inferences, previous):
        '''add the inferences onto the variables dictionary and store
           the old values in previous in case they need to be undone'''
        for key in inferences:
            previous[key]           = variables[key].copy()
            variables[key].domain   = list(inferences[key].domain)
    
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