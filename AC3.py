import functools
from functools import reduce
from Constraint import *
from itertools import product
from Consistent import *

class AC3:
    def __init__(self):
        self.consistent = Consistent
    
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
        # fill the queue with all the constraints
        queue = []
        for constraint in csp.constraints:
            queue.append(constraint)
        # supply the AC3 function with the queue
        ## well shit....lets just keep looping
        while not self.isComplete(csp) and not self.isFail(csp):
            self.AC3(csp,queue)
            self.printDomains(csp.variables)
            if len(queue) == 0:
                break
        # this should display the answer?
        self.printDomains(csp.variables)
    
    def AC3(self,csp,queue):
        while len(queue) > 0:
            #Get a constraint from the queue
            constraint = queue.pop(0)
            self.printDomains(csp.variables)
            #Revise the domains based on the constraint
            if self.Revise(csp, constraint):
                #if a revised domain becomes empty, we failed
                if self.isEmpty(constraint):
                    return False
                #otherwise, collect all the neighbors of the variables
                #in the constraint
                for neighbor in self.getNeighbors(constraint,csp):
                    for constraint in self.getConstraints(neighbor,csp):
                        queue.append(constraint)
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
    
    
    def Revise(self, csp, constraint):
        #Check to see which type of constraint the object is
        #and choose the appropriate revise function
        if isinstance(constraint, BinaryConstraint):
            return self.ReviseAC(constraint)
        elif isinstance(constraint, GlobalConstraint):
            return self.ReviseGAC(constraint)
        return False
            
        
    def ReviseAC(self, bc):
        #The basic AC Binary Constraint Revise function
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
    
    def ReviseGAC(self, gc):
        ## Gather the domains of all the variables and 
        ## instantiate the array that will contain the
        ## updated domains based on the global constraint
        revised         = False
        domains         = []
        new_domains     = []
        for v in gc.vars:
            domains.append(v.domain)
            new_domains.append([])
        # Product takes in a list of lists and returns all
        # possible forward combinations of one element in each list
        # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
        # Loop through all arg combinations, and find ones that satisfy
        # the global constraint function.  Update the new domains with
        # their respective values.
        for args in product(*domains):
            if gc.func(*args):
                for i,v in enumerate(args):
                    new_domains[i].append(v)
        
        ## Note: we only care to update k-1 domains. The last domain remains
        ## unaltered per the definition of K-consistency in the book
        for i,new_domain in enumerate(new_domains):
            new_domain = list(set(new_domain))
            if len(new_domain) != len(gc.vars[i].domain):
                revised = True
            gc.vars[i].domain = new_domain
        
        return revised
    
    def isFail(self,csp):
        for constraint in csp.constraints:
            if self.isEmpty(constraint):
                return True
        return False
    
    def isEmpty(self,constraint):
        # check if a domain is empty for any variable within
        # a binary or global constraint
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
        # collect all the neighbors from a constraint's variables
        constraint.neighborize()
        if isinstance(constraint, BinaryConstraint):
            return constraint.var1.neighbors + constraint.var2.neighbors
        elif isinstance(constraint, GlobalConstraint):
            all_vars = []
            for var in constraint.vars:
                for neighbor in var.neighbors:
                    all_vars.append(neighbor)
            return all_vars
    
    def getConstraint(self,variable1,variable2,csp):
        for constraint in csp.constraints:
            if isinstance(constraint, BinaryConstraint):
                if constraint.contains(variable1) and constraint.contains(variable2):
                    return constraint
            elif isinstance(constraint, GlobalConstraint):
                if constraint.contains(variable1) and constraint.contains(variable2):
                    return constraint
        return constraints
    
    def getConstraints(self,variable,csp):
        constraints = []
        for constraint in csp.constraints:
            if isinstance(constraint, BinaryConstraint):
                if constraint.var2.name == variable.name:
                    constraints.append(constraint)
            elif isinstance(constraint, GlobalConstraint):
                if constraint.contains(variable):
                    constraints.append(constraint)
        return constraints
        
    def printDomains(self, vars, n=3 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k].domain,'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')