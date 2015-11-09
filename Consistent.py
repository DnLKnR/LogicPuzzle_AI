from Constraint import *
from itertools  import product
   
   
class Consistent:
    def __init__(self):
        pass
    
    def evaluate(self, variable, constraint):
        if isinstance(constraint, UnaryConstraint):
            return self.isNC(variable, constraint)
            
        elif isinstance(constraint, BinaryConstraint):
            return self.isAC(variable, constraint)
            
        elif isinstance(constraint, GlobalConstraint):
            return self.isGAC(variable, constraint)
            
        else:
            print("Unrecognized instance passed to Consistent.consistent()")
            return None
    
    def execute(self, variable, csp):
        ## THIS FUNCTION MODIFIES CSP #
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if isinstance(constraint, BinaryConstraint):
                    self.execAC(variable, constraint)
                elif isinstance(constraint, GlobalConstraint):
                    self.execGAC(variable, constraint)
    
    def execAC(self, variable, bc):
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
        index       = -1
        domain      = []
        domains     = []
        new_domains = []
        x           = variable.domain[0]
        for i,v in enumerate(gc.vars):
            if variable.name == v.name:
                index = i
            else:
                domains.append(v.domain)
                new_domains.append([])
        args_list = list(product(*domains))
        for args in args_list:
            arg = list(args)
            arg.insert(index, x)
            if gc.func(*arg):
                for i,v in enumerate(args):
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
        # Product takes in a list of lists and returns all
        # possible forward combinations of one element in each list
        # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
        args_list = list(product(*domains))
        # Loop through all arg combinations, and find ones where the first
        # variable cannot satisfy the defined function and remove it 
        # from the domain of the first variable
        for x in domain:
            satisfy = False
            for args in args_list:
                args = list(args)
                args.insert(index, x)
                if gc.func(*args):
                    satisfy = True
                    break
            if not satisfy:
                return False
        
        return True
    
    def GAC(self, gc, inference):
        domains = []
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
            if len(domain):
                inference[variable.name].domain = domain
            else:
                return None
        return inference
    
    def NC(self, uc, inference):
        domain = list(uc.var.domain)
        for x in domain:
            if ( False == uc.func(x) ):
                uc.var.domain.remove(x)
    
    def AC(self, bc, inference):
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
        if len(new_domain_x) and len(new_domain_y):
            inference[bc.var1.name].domain = new_domain_x
            inference[bc.var2.name].domain = new_domain_y
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
        args_list = list(product(*domains))
        # Loop through all arg combinations, and find ones that satisfy
        # the global constraint function.  Update the new domains with
        # their respective values.
        for args in args_list:
            if gc.fn(*args):
                for i,v in enumerate(args):
                    if v not in new_domains[i]:
                        new_domains[i].append(v)
        ## Note: we only care to update k-1 domains. The last domain remains
        ## unaltered per the definition of K-consistency in the book
        for i,new_domain in enumerate(new_domains[:-1]):
            gc.vars[i] = new_domain
             
             
    