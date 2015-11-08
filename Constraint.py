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
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.var = v
        self.func = fn

class BinaryConstraint:
    # v1 and v2 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y ) 
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

class TernaryConstraint:
    # v1, v2, v3 should be of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiate example: TernaryConstraint( A1, A2, A3, lambda x,y,z: x+y+z==10 ) 
    def __init__(self, v1, v2, v3, fn):
        self.var1 = v1
        self.var2 = v2
        self.var3 = v3

class GlobalConstraint:
    # vars should be a list of ConstraintVar objects
    # fn is the lambda expression for the constraint
    # instantiate example: GlobalConstraint( [A1, A2, A3], lambda A1,A2,A3: A1+A2+A3==10 ) 
    def __init__(self, vars, fn):
        self.vars   = vars
        self.fn     = fn
    
class ConstraintSatisfactionProblem:
    # This class contains the following variables:
    # input:       definition string,    ex. "+,basic+logic=pascal"
    # variables:   a set of variables,   ex. ['a','b','c','d','e','f','g','h',....]
    # domains:     a set of domains,     ex. {'a' : [1..26], 'b' : [1..26],....}
    # constraints: a set of constraints, ex. [Constraint Object,...]
    def __init__(self, variables=dict(), constraints=[]):
        self.variables      = variables
        self.constraints    = constraints