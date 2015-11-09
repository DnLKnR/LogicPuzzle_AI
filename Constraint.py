from copy import deepcopy
# This is demonstrating a "class" implementation of AC3. You can accomplish the same with lists. For the project, you can choose either.

# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value


class ConstraintVar:
    # instantiation example: ConstraintVar( [1,2,3],'A1' )
    # MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__(self, d, n ):
        self.domain     = [ v for v in d ]
        self.name       = n
        self.neighbors  = []
        
    def add(self,new):
        exists = False
        for neighbor in self.neighbors:
            if neighbor.name == new.name:
                exists = True
                break
        if not exists:
            self.neighbors.append(new)
            
    def copy(self):
        new_copy = ConstraintVar(list(self.domain),self.name)
        #new_copy.neighbors = list(self.neighbors)
        return new_copy

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.var = v
        self.func = fn
        
    def contains(self,var):
        if self.var.name == var.name:
            return True
        return False
    
    def complete(self):
        if len(self.var.domain) != 1:
            return False
        elif not self.func(self.var.domain[0]):
            return False
        else:
            return True
    
    def neighborize(self):
        # Awww :(
        pass
    
    def copy(self):
        return UnaryConstraint(self.var.copy(), self.func)
    
    def link(self,variables):
        self.var = variables[self.var.name]

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y ) 
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn
    
    def contains(self,var):
        if var.name in [self.var1.name, self.var2.name]:
            return True
        return False
    
    def complete(self):
        if len(self.var1.domain) != 1 or len(self.var2.domain) != 1:
            return False
        elif not self.func(self.var1.domain[0],self.var2.domain[0]):
            return False
        else:
            return True
    
    def unassigned(self, variable):
        if variable.name == self.var1.name:
            if len(self.var2.domain) > 1:
                return 1
        elif variable.name == self.var2.name:
            if len(self.var1.domain) > 1:
                return 1
        return 0
    
    def neighborize(self):
        self.var1.add(self.var2)
        self.var2.add(self.var1)
    
    def copy(self):
        return BinaryConstraint(self.var1.copy(), self.var2.copy(), self.func)
        
    def link(self,variables):
        self.var1 = variables[self.var1.name]
        self.var2 = variables[self.var2.name]
        
class GlobalConstraint:
    # vars should be a list of ConstraintVar objects
    # fn is the lambda expression for the constraint
    # instantiate example: GlobalConstraint( [A1, A2, A3], lambda A1,A2,A3: A1+A2+A3==10 ) 
    def __init__(self, vars, fn):
        self.vars = vars
        self.func = fn
    
    def unassigned(self, variable):
        unassigned  = False
        exists      = False
        for var in self.vars:
            if var.name == variable.name:
                exists = True
            elif len(var.domain) > 1:
                unassigned = True
            if exists and unassigned:
                return 1
        return 0
    
    def contains(self, var):
        for v in self.vars:
            if var.name == v.name:
                return True
        return False
        
    def complete(self):
        args = []
        for var in self.vars:
            if len(var.domain) != 1:
                return False
            args.append(var.domain[0])
            
        if not self.func(*args):
            return False
        else:
            return True
    
    def neighborize(self):
        for var1 in self.vars:
            for var2 in self.vars:
                if var1.name != var2.name:
                    var1.add(var2)
    
    def copy(self):
        copy_vars = []
        for var in self.vars:
            copy_vars.append(var.copy())
        return GlobalConstraint(copy_vars, self.func)
    
    def link(self,variables):
        for var in self.vars:
            var = variables[var.name]
        
class ConstraintSatisfactionProblem:
    # This class contains the following variables:
    # input:       definition string,    ex. "+,basic+logic=pascal"
    # variables:   a set of variables,   ex. ['a','b','c','d','e','f','g','h',....]
    # domains:     a set of domains,     ex. {'a' : [1..26], 'b' : [1..26],....}
    # constraints: a set of constraints, ex. [Constraint Object,...]
    def __init__(self, variables=None, constraints=None):
        self.variables      = variables
        if self.variables == None:
            self.variables  = dict()
        self.constraints    = constraints
        if self.constraints == None:
            self.constraints = []
    
    def copy(self):
        copy_variables   = dict()
        copy_constraints = []
        for key in self.variables:
            copy_variables[key] = self.variables[key].copy()
        for constraint in self.constraints:
            copy_constraint = constraint.copy()
            copy_constraint.link(copy_variables)
            copy_constraints.append(copy_constraint)
        return ConstraintSatisfactionProblem(copy_variables, copy_constraints)
    
    
    
    
    