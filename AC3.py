import functools
from functools import reduce
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
        # fill the queue with all the constraints
        queue = []
        
        # supply the AC3 function with the queue
        ## well shit....lets just keep looping
        while not self.isComplete(csp):
            for constraint in csp.constraints:
                constraint.neighborize()
                queue.append(constraint)
            self.AC3(csp,queue)
        # this should display the answer?
        self.printDomains(csp.variables)
    
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
                    #extend the queue
                    queue.extend(self.getConstraints(neighbor,csp))
        return True
    
    def Revise(self, csp, constraint):
        #Check to see which type of constraint the object is
        #and choose the appropriate revise function
        if isinstance(constraint, BinaryConstraint):
            return self.ReviseAC(csp, constraint)
        elif isinstance(constraint, GlobalConstraint):
            return self.ReviseGAC(csp, constraint)
        return False
            
        
    def ReviseAC(self, csp, bc):
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
    
    def ReviseGAC(self, csp, gc):
        #boolean stuffs
        revised,chosen = False,False
        #index of that random selected variable
        index          = -1
        #randomly selected variables domain
        domain         = []
        #will contain all variable domains in global constraint
        domains        = []
        for i,v in enumerate(gc.vars):
            #Here I am randomly selecting a variable to focus on
            #I dont know which I should choose in the list of
            #variables for gc (Global Constraint)
            if len(v.domain) > 1 and not chosen:
                index = i
                domain = list(v.domain)
                chosen = True
            #Collect all the variables domains
            domains.append(v.domain)
        #Go through the domain of my randomly selected variable
        for x in domain:
            satisfy = False
            #force the domain to a single value
            domains[index] = [x]
            print(domains[index])
            #Create all possible arg combinations and iterate them
            for args in product(*domains):
                #If the arg combination works, it is satisfied
                if gc.func(*args):
                    satisfy = True
                    break
            #if not arg combination found using x, remove it
            if not satisfy:
                gc.vars[index].domain.remove(x)
                revised = True
        #return whether or not I was capable of revising it
        return revised
        
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