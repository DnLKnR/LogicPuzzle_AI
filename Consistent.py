from Constraint import *
from itertools  import product
from time import time
   
class Consistent:
    def __init__(self):
        pass
    
    
    ### Probably delete this function
    def infer(self, variable, inference, csp):
        for constraint in csp.constraints:
            #print("evaluating inferences...")
            if isinstance(constraint, BinaryConstraint) and constraint.contains(variable):
                #if isinstance(constraint, UnaryConstraint):
                #    print("starting Node Consistency")
                #    start = time()
                #    inference = self.inferNC(variable, constraint, inference)
                #    end   = time()
                #    print("completed Node Consistency in {0}".format(end-start))
                #print("evaluating inferences that contain variable...")
                #if :
                print("starting Arc Consistency")
                start = time()
                inference = self.inferAC(variable, constraint, inference)
                end   = time()
                print("completed Arc Consistency in {0}".format(end-start))
                #elif isinstance(constraint, GlobalConstraint):
                #    print("starting Generalized Arc Consistency")
                #    start = time()
                #    inference = self.inferGAC(variable, constraint, inference)
                #    end   = time()
                #    print("completed Generalized Arc Consistency in {0}".format(end-start))
                if inference == None:
                    print("...result False")
                    return None
        print("...result True")
        return inference
    
    def evaluate(self, variable, csp):
        #print(len(csp.constraints))
        for constraint in csp.constraints:
            #print("evaluating...")
            if constraint.contains(variable):
                if isinstance(constraint, UnaryConstraint):
                    print("evaluating Node Consistency",end="")
                    if not self.isNC(variable, constraint):
                        print("...result: false")
                        return False
                    print("...result: true")
                elif isinstance(constraint, BinaryConstraint):
                    print("evaluating Arc Consistency",end="")
                    if not self.isAC(variable, constraint):
                        print("...result: false")
                        return False
                    print("...result: true")
                elif isinstance(constraint, GlobalConstraint):
                    print("evaluating Generalized Arc Consistency",end="")
                    if not self.isGAC(variable, constraint):
                        print("...result: false")
                        return False
                    print("...result: true")
                else:
                    print("Unrecognized instance passed to Consistent.consistent()")
                    return True
        return True
    
    def execute(self, variable, csp):
        ## THIS FUNCTION MODIFIES CSP #
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if isinstance(constraint, BinaryConstraint):
                    self.execAC(variable, constraint)
                elif isinstance(constraint, GlobalConstraint):
                    self.execGAC(variable, constraint)
    
    def execNC(self, variable, nc):
        domain = list(uc.var.domain)
        for x in domain[::-1]:
            if (uc.func(x) == False):
                domain.remove(x)
        if len(domain):
            inference[variable.name] = ConstraintVar(domain, variable.name)
            return inference
        return None
    
    def execAC(self, variable, bc):
        reverse = (bc.var2.name == variable.name)
        var     = bc.var2
        if reverse:
            var = bc.var1
        x = (variable.domain)[0]
        new_domain = []
        for y in var.domain:
            if (reverse and bc.func(y,x)) or ((not reverse) and bc.func(x,y)):
                if y not in new_domain:
                    new_domain.append(y)
        var.domain = new_domain
    
    def execGAC(self, variable, gc):    
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
        for arg in product(*domains):
            args = list(arg)
            args.insert(index, x)
            if gc.func(*args):
                for i,v in enumerate(arg):
                    if v not in new_domains[i]:
                        new_domains[i].append(v)
        new_domains.insert(index,[x])
        for i,new_domain in enumerate(new_domains):
            gc.vars[i].domain = new_domain
        
    def isNC(self, variable, uc):
        for x in uc.var.domain:
            if not uc.func(x):
                return False
        return True
    
    def isAC(self, variable, bc):
        reverse = (bc.var2.name == variable.name)
        if reverse:
            domain1 = list(bc.var2.domain)
            domain2 = list(bc.var1.domain)
        else:
            domain1 = list(bc.var1.domain)
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
        index       = -1
        domain      = []
        domains     = []
        for i,v in enumerate(gc.vars):
            if variable.name == v.name:
                index = i
                domain = list(gc.vars[i].domain)
            else:
                domains.append(v.domain)
                
        args_iter = product(*domains)
        for x in domain:
            satisfy = False
            for args in args_iter:
                args = list(args)
                args.insert(index, x)
                if gc.func(*args):
                    satisfy = True
                    break
            if not satisfy:
                return False
        
        return True
    
    def isKC(self, variable, gc):
        ## Gather the domains of all the variables and 
        ## instantiate the array that will contain the
        ## updated domains based on the global constraint
        domains         = []
        for v in gc.vars:
            domains.append(v.domain)
        for args in product(*domains):
            if not gc.func(*args):
                return False
        return True
    
    def inferGAC(self, variable, gc, inference):
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
                    inference[gc.vars[i].name] = ConstraintVar(new_domain, gc.vars[i].name)
            else:
                return None
        
        return inference
    
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
            inference[gc.vars[i].name] = ConstraintVar(new_domain, gc.vars[i].name)
        return inference  
            
    def inferNC(self, variable, uc, inference):
        domain = list(uc.var.domain)
        for x in domain[::-1]:
            if (uc.func(x) == False):
                domain.remove(x)
        if len(domain):
            inference[variable.name] = ConstraintVar(domain, variable.name)
            return inference
        return None
    
    def inferAC(self, variable, bc, inference):
        new_domain_x = []
        new_domain_y = []
        for x in bc.var1.domain:
            satisfy = False
            for y in bc.var2.domain:
                if bc.func(x,y):
                    satisfy = True
                    if y not in new_domain_y:
                        new_domain_y.append(y)
            if satisfy:
                new_domain_x.append(x)
        if len(new_domain_x) and bc.var1.name != variable.name:
            inference[bc.var1.name] = ConstraintVar(new_domain_x, variable.name)
            return inference
        elif len(new_domain_y) and bc.var2.name != variable.name:
            inference[bc.var2.name] = ConstraintVar(new_domain_y, variable.name)
            return inference
        else:
            return None
    
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
            gc.vars[i] = new_domain
             
             
    