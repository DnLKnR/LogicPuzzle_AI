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
            if isinstance(constraint, BinaryConstraint):
                queue.append(constraint)
            elif isinstance(constraint, GlobalConstraint):
                queue.append(constraint)
        self.AC3(csp,queue)
        self.printDomains(csp.variables)
    
    def AC3(self,csp,queue):
        while len(queue) > 0:
            constraint = queue.pop(0)
            if self.Revise(csp, constraint):
                if self.isEmpty(constraint):
                    return False
                for variable in self.getNeighbors(constraint,csp):
                    queue.extend(self.getConstraints(variable,csp))
        return True
    
    def isEmpty(self,constraint):
        if isinstance(constraint, BinaryConstraint):
            for var in [constraint.var1, constraint.var2]:
                if len(var.domain) == 0:
                    return True
            return False
        elif isinstance(constraint, GlobalConstraint):
            for var in constraint.vars:
                if len(var.domain) == 0:
                    return True
            return False
    
    def getNeighbors(self,constraint,csp):
        constraint.neighborize()
        if isinstance(constraint, BinaryConstraint):
            return list(constraint.var1.neighbors + constraint.var2.neighbors)
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
            if constraint.contains(variable):
                constraints.append(constraint)
        return constraints
                
                
    
    def Revise(self, csp, constraint):
        if isinstance(constraint, BinaryConstraint):
            return self.ReviseAC(csp, constraint)
        elif isinstance(constraint, GlobalConstraint):
            return self.ReviseGAC(csp, constraint)
            
        
    def ReviseAC(self, csp, bc):
        # The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
        # A single BinaryConstraint instance is passed in to this function. 
        # MISSSING the part about returning sat to determine if constraints need to be added to the queue
        
        # copy domains for use with iteration (they might change inside the for loops)
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
        domains     = []
        new_domains = []
        revised     = False
        for v in gc.vars:
            domains.append(v.domain)
        last = len(domains) - 1
        for index,variable in enumerate(gc.vars):
            domain  = domains[index]
            new_domain = []
            others  = []
            if index == 0:
                others = domains[1:]
            elif index == last:
                others = domains[:-1]
            else:
                others = domains[:index] + domains[index + 1:]
            args_list = list(product(*others))
            for x in domain:
                satisfy = False
                for args in args_list:
                    arg_list = list(args)
                    arg_list.insert(index, x)
                    if gc.func(*arg_list):
                        satisfy = True
                        break
                if satisfy:
                    new_domain.append(x)
                if not satisfy:
                    revised = True
            new_domains.append(new_domain)
        for i,v in enumerate(gc.vars):
            v.domain = new_domains[i]
        return revised
        
    def printDomains(self, vars, n=3 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k].domain,'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')