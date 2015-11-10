from Constraint import *
from itertools  import product
from time import time
   
class Consistent:
    def __init__(self):
        pass
    
    def evaluate(self, variable, csp):
        '''this function simply evalates whether or not the new variable's 
           domain creates an empty domain for another variable elsewhere.
           If it does, return false so we can test another value, otherwise
           return true.'''
        for constraint in variable.constraints:
            if isinstance(constraint, UnaryConstraint):
                if not self.isNC(variable, constraint):
                    return False
            elif isinstance(constraint, BinaryConstraint):
                if not self.isAC(variable, constraint):
                    return False
            elif isinstance(constraint, GlobalConstraint):
                if not self.isGAC(variable, constraint):
                    return False
            else:
                print("Unrecognized instance passed to Consistent.consistent()")
                return True
        return True
    
    def execute(self, variable, csp):
        '''this function is only used by Least Constraining Value Order.
           This function acts like evaluate() except it modifies all the
           domains in CSP to meet the constraints with the new domain defined
           in variable.'''
        ## THIS FUNCTION MODIFIES CSP #
        for constraint in variable.constraints:
            if isinstance(constraint, BinaryConstraint):
                self.execAC(variable, constraint)
            elif isinstance(constraint, GlobalConstraint):
                self.execGAC(variable, constraint)
    
    def execNC(self, variable, nc):
        '''Execute the variable as an addition to the constraint
           and update the domains to satisfy it'''
        domain = list(uc.var.domain)
        for x in domain[::-1]:
            if (uc.func(x) == False):
                domain.remove(x)
        if len(domain):
            inference[variable.name] = variable.copy()
            return inference
        return None
    
    def execAC(self, variable, bc):
        '''Execute the variable as an the new domain
           for the corresponding variable in the constraint
           to the constraint and update the other variables'
           domains to satisfy it'''
        reverse = (bc.var2.name == variable.name)
        var     = bc.var2
        if reverse:
            var = bc.var1
        x = variable.domain[0]
        new_domain = []
        for y in var.domain:
            if (reverse and bc.func(y,x)) or ((not reverse) and bc.func(x,y)):
                if y not in new_domain:
                    new_domain.append(y)
        var.domain = new_domain
    
    def execGAC(self, variable, gc):
        '''Execute the variable as an the new domain
           for the corresponding variable in the constraint
           to the constraint and update the other variables'
           domains to satisfy it'''
        print("execGAC was called")
        domains     = []
        new_domains = []
        index       = -1
        x           = variable.domain[0]
        for i,v in enumerate(gc.vars):
            if v.name == variable.name:
                index = i
            domains.append(v.domain)
            new_domains.append([])
        for x in variable.domain:
            domains[i] = [x]
            for arg in product(*domains):
                if gc.func(*args):
                    for i,v in enumerate(arg):
                        if v not in new_domains[i]:
                            new_domains[i].append(v)
            new_domains.insert(index,[x])
        for i,new_domain in enumerate(new_domains):
            gc.vars[i].domain = new_domain
        
    def isNC(self, variable, uc):
        '''Check if the variable's new domain is consistent
           with the unary constraint (node consistent -> nc)'''
        for x in uc.var.domain:
            if not uc.func(x):
                return False
        return True
    
    def isAC(self, variable, bc):
        '''Check if the variable's new domain is consistent
           with the binary constraint (arc consistent -> ac)'''
        reverse = (bc.var2.name == variable.name)
        if reverse:
            domain1 = list(variable.domain)
            domain2 = list(bc.var1.domain)
        else:
            domain1 = list(variable.domain)
            domain2 = list(bc.var2.domain)
        
        for x in domain1:
            satisfy = False
            for y in domain2:
                if (reverse and bc.func(y,x)) or ((not reverse) and bc.func(x,y)):
                    satisfy = True
                    break
            if not satisfy:
                return False
        
        return True
        
    def isGAC(self, variable, gc):
        '''Check if the variable's new domain is consistent
           with the global constraint (global consistent -> gc)'''
        print("isGAC was called")
        domains     = []
        index       = -1
        # Gather all of the domains, and also store the domain
        # of the variable we passed in as a parameter
        for i,v in enumerate(gc.vars):
            if v.name == variable.name:
                index = i
            domains.append(v.domain)
        # Product takes in a list of lists and returns all
        # possible forward combinations of one element in each list
        # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
        #args_list = list(product(*domains))
        for x in variable.domain:
            satisfy = False
            #Change the domain to single value for the variable we are evaluating
            domains[index] = [x]
            # iterate through all combinations
            for args in product(*domains):
                if gc.func(*args):
                    return True
            #no possible combinations with value x in n-Ary constraint
            if not satisfy:
                return False
        #if for each x, some combination args exist 
        #to satisfy constraint then we return true
        return True
    
    def inferNC(self, variable, uc, inference):
        '''Any function with 'infer' infront of them take in a dictionary
           of variables that are inferred by the adding of the variable 
           onto the global constraint.  NC means node consistent that the
           variable's domain must satisfy the unary constraint.  This function
           is probably not used.  Only present for abstraction purposes.'''
        domain = list(uc.var.domain)
        for x in domain[::-1]:
            if (uc.func(x) == False):
                domain.remove(x)
        if len(domain):
            inference[uc.var.name] = uc.var.copy()
            inference[uc.var.name].domain = domain
            return inference
        return None
    
    def inferAC(self, variable, bc, inference):
        '''Any function with 'infer' infront of them take in a dictionary
           of variables that are inferred by the adding of the variable 
           onto the global constraint. AC means arc consistent which means 
           that for each value in the variable's domain, there has
           to be some combination that satisfies in the constraint'''
        print("inferAC was called")
        new_domain = []
        if variable.name == bc.var1.name:
            for y in bc.var2.domain:
                satisfy = False
                for x in variable.domain:
                    if bc.func(x,y):
                        satisfy = True
                        break
                if satisfy and y not in new_domain:
                    new_domain.append(y)
            if len(new_domain):
                inference[bc.var2.name]        = bc.var2.copy()
                inference[bc.var2.name].domain = new_domain
                return inference
        elif variable.name == bc.var2.name:
            for x in bc.var1.domain:
                satisfy = False
                for y in variable.domain:
                    if bc.func(x,y):
                        satisfy = True
                        break
                if satisfy and x not in new_domain:
                    new_domain.append(x)
            if len(new_domain):
                inference[bc.var1.name]        = bc.var1.copy()
                inference[bc.var1.name].domain = new_domain
            return inference
        return None
            
    def inferGAC(self, variable, gc, inference):
        '''Any function with 'infer' infront of them take in a dictionary
           of variables that are inferred by the adding of the variable 
           onto the global constraint.  GAC means generalized arc consistent
           which means that for each value in the variable's domain, there has
           to be some combination that satisfies in the constraint'''
        print("inferGAC was called")
        index       = -1
        domain      = []
        domains     = []
        new_domains = []
        x           = (variable.domain)[0]
        for i,v in enumerate(gc.vars):
            if variable.name == v.name:
                index = i
            else:
                domains.append(v.domain)
                new_domains.append([])
        #args_list = list(product(*domains))
        for args in product(*domains):
            all_args = list(args)
            all_args.insert(index, x)
            if gc.func(*all_args):
                for i,v in enumerate(args):
                    if v not in new_domains[i]:
                        new_domains[i].append(v)
        new_domains.insert(index,[x])
        for i,new_domain in enumerate(new_domains):
            if len(new_domain) > 0:
                if len(new_domain) < len(gc.vars[i].domain):
                    inference[gc.vars[i].name] = gc.vars[i].copy()
                    inference[gc.vars[i].name].domain = new_domain
            else:
                return None
        
        return inference
    
    
    #########################################
    ### IGNORE THESE FUNCTIONS, UNUSED  #####
    ### TO BE DELETED                   #####
    #########################################
    
    def inferKC(self, variable, gc, inference):
        
        
        ## Gather the domains of all the variables and 
        ## instantiate the array that will contain the
        ## updated domains based on the global constraint
        domains         = []
        new_domains     = []
        for v in gc.vars:
            domains.append(v.domain)
            new_domains.append([])
        # Product takes in a list of lists and returns all
        # possible forward combinations of one element in each list
        # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
        #args_list = list(product(*domains))
        # Loop through all arg combinations, and find ones that satisfy
        # the global constraint function.  Update the new domains with
        # their respective values.
        for args in product(*domains):
            if gc.func(*args):
                for i,v in enumerate(args):
                    if v not in new_domains[i]:
                        new_domains[i].append(v)
        ## Note: we only care to update k-1 domains. The last domain remains
        ## unaltered per the definition of K-consistency in the book
        for i,new_domain in enumerate(new_domains[:-1]):
            if len(new_domain) == 0:
                return None
            inference[gc.vars[i].name] = gc.vars[i].copy()
            inference[gc.vars[i].name].domain = new_domain
        return inference  
            
    def pathConsistent(self, tc ):
        domain1 = list(tc.var1.domain)
        domain2 = list(tc.var2.domain)
        domain3 = list(tc.var3.domain)
        new_domain1 = []
        new_domain2 = []
        for x in domain1:
            satisfy_x = False
            for y in domain2:
                satisfy_y = False
                for z in domain3:
                    if tc.func(x,y,z):
                        satisfy_x = True
                        satisfy_y = True
                        break
                if satisfy_y and y not in new_domain2:
                    new_domain2.append(y)
            if satisfy_x and x not in new_domain1:
                new_domain1.append(x)
        tc.var1.domain = new_domain1
        tc.var2.domain = new_domain2
     
    def kConsistent(self, gc ):
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
            if gc.fn(*args):
                for i,v in enumerate(args):
                    if v not in new_domains[i]:
                        new_domains[i].append(v)
        ## Note: we only care to update k-1 domains. The last domain remains
        ## unaltered per the definition of K-consistency in the book
        for i,new_domain in enumerate(new_domains[:-1]):
            if len(new_domain) != len(gc.vars[i].domain):
                revised = True
                gc.vars[i].domain = new_domain
        
        return revised
    
    def isKC(self, variable, gc):
        ## Gather the domains of all the variables and 
        ## instantiate the array that will contain the
        ## updated domains based on the global constraint
        domains         = []
        ## Make sure that all combinations satisfy constraint
        for v in gc.vars:
            domains.append(v.domain)
        for args in product(*domains):
            if not gc.func(*args):
                return False
        return True
             
    