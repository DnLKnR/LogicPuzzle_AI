import functools
from functools import reduce
from Backtracking import BacktrackingSearch
from Parse import PuzzleParser
from Constraint import *
from itertools import product

class AC3:
    def __init__(self):
        pass
    
    def allDiff(self, constraints, v):    
        # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
        # constraints is a preconstructed list. v is a list of ConstraintVar instances.
        # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
        fn = lambda x,y: x != y
        for i in range(len(v)):
            for j in range(len(v)):
                if ( i != j ) :
                    constraints.append(BinaryConstraint(v[i],v[j],fn))
    
    def run(self,csp):
        queue = []
        for constraint in csp.constraints:
            constraint.neighborize()
            queue.append(constraint)
        self.AC3(csp,queue)
        self.printDomains(csp.variables)
    
    def AC3(self,csp,queue):
        while len(queue) > 0:
            constraint = queue.pop(0)
            self.printDomains(csp.variables)
            if self.Revise(csp, constraint):
                if self.isEmpty(constraint):
                    return False
                for neighbor in self.getNeighbors(constraint,csp):
                    queue.extend(self.getConstraints(neighbor,csp))
        return True
    
    def Revise(self, csp, constraint):
        if isinstance(constraint, BinaryConstraint):
            return self.ReviseAC(csp, constraint)
        elif isinstance(constraint, GlobalConstraint):
            return self.ReviseGAC(csp, constraint)
        return False
            
        
    def ReviseAC(self, csp, bc):
        dom1 = list(bc.var1.domain)
        dom2 = list(bc.var2.domain)
        revised = False
        # for each value in the domain of variable 1
        for x in dom1:
            satisfy = False
            # for each value in the domain of variable 2
            for y in dom2:
                if bc.func(x,y):
                    satisfy = True
                    break
            if not satisfy:
                bc.var1.domain.remove(x)
                revised = True
        
        return revised
    
    def ReviseGAC(self, csp, gc):
        revised,chosen = False,False
        index          = -1
        domain         = []
        domains        = []
        for i,v in enumerate(gc.vars):
            if len(v.domain) > 1 and not chosen:
                index = i
                domain = list(v.domain)
                chosen = True
            domains.append(v.domain)
        for x in domain:
            satisfy = False
            domains[index] = [x]
            print(domains[index])
            for args in product(*domains):
                if gc.func(*args):
                    satisfy = True
                    break
            if not satisfy:
                gc.vars[index].domain.remove(x)
                revised = True
        return revised
        
    def isEmpty(self,constraint):
        if isinstance(constraint, BinaryConstraint):
            for var in [constraint.var1, constraint.var2]:
                if len(var.domain) == 0:
                    return True
        elif isinstance(constraint, GlobalConstraint):
            for var in constraint.vars:
                if len(var.domain) == 0:
                    return True
        return False
    
    def getNeighbors(self,constraint,csp):
        if isinstance(constraint, BinaryConstraint):
            return list(constraint.var1.neighbors)
        elif isinstance(constraint, GlobalConstraint):
            all_vars = []
            for var in constraint.vars:
                for neighbor in var.neighbors:
                    if neighbor not in all_vars:
                        all_vars.append(neighbor)
            return all_vars
    
    def getConstraints(self,variable,csp):
        constraints = []
        for constraint in csp.constraints:
            if isinstance(constraint, BinaryConstraint):
                if constraint.var2.name == variable.name:
                    constraints.append(constraint)
            elif isinstance(constraint, GlobalConstraint):
                if constraint.constains(variable):
                    constraints.append(constraint)
        return constraints
    
    
        
    def printDomains(self, vars, n=3 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k].domain,'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')