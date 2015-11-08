import functools
from functools import reduce
import itertools

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

class GlobalConstraint:
    # vars should be a list of ConstraintVar objects
    # fn is the lambda expression for the constraint
    # instantiate example: GlobalConstraint( [A1, A2, A3], lambda A1,A2,A3: x + y + z == 10 ) 
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

### HUERISTICS ###
def AnyValue(csp):
    pass

def MinimumRemainingValues(csp):
    min = -1
    var = ""
    for key in csp.variables.iterkeys():
        length = len(csp.variables[key])
        if min < length:
            var,max = key,length
    return csp.variables[key]
    
    
def LeastConstrainingValues(csp):
    min = inf
    var = ""
    for key in csp.variables.iterkeys():
        length = len(csp.variables[key])
        if min > length:
            var,max = key,length
    return var
        

def Degree(csp):
    
    pass

### INFERENCES ###
def ForwardChecking(heuristicFn):
    pass

def MaintainingArcConsistency(heuristicFn):
    pass

def allDiff( constraints, v ):    
    # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
    # constraints is a preconstructed list. v is a list of ConstraintVar instances.
    # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in range(len(v)):
        for j in range(len(v)):
            if ( i != j ) :
                constraints.append(BinaryConstraint( v[i],v[j],fn ))

class PuzzleParser:
    def __init__(self):
        pass
    
    def getVars(self,equation):
        special_char = "!@#$%^&*()_+-=[]\\{}|;\':\",./<>? "
        start,end,vars,is_special = 0, 0, [], False
        length = len(equation)
        while end <= length:
            #Find the start index of a variable
            while start < length and equation[start] in special_char:
                start   += 1
            #Find the end index of a variable
            end = start + 1
            while end < length and equation[end] not in special_char:
                end     += 1
            #if the range is greater than 0, we found a variable
            if end - start > 0 and end <= length:
                vars.append(equation[start:end])
            #reset start to where we left off
            start = end
        
        return vars
    
    def setUpCrossMath(self,input):
        csp     = ConstraintSatisfactionProblem()
        input   = input.replace(' ','').replace('\r','').replace('\n','')
        equations = input.split(',')
        variables = []
        #Set up the variables and constraints
        for equation in equations:
            problem, solution = equation.split('=')
            vars = self.getVars(problem)
            for var in vars:
                if var not in variables:
                    variables.append(var)
            vars_str = ','.join(vars)
            # print(vars_str)
            relation = equation.replace('=','==')
            function = eval("lambda {0}:{1}".format(vars_str,relation))
            # print(stringFn)
            csp.constraints.append(GlobalConstraint(vars, function))
            
        #Set up the domains
        length = len(variables)
        for name in variables:
            domain = list(range(1, length + 1))
            csp.variables[name] = ConstraintVar(domain, name)
        
        printDomains(csp.variables, 3)
        print("")
        
        return csp
    
    #print(csp.input)
    #print(printDomains(csp.variables))
    #print(csp.constraints)
    
    def setUpCrypt(self,csp):
        # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
        # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object
    
        # Note that I could accomplish the same by hard coding the variables, for example ...
        # A1 = ConstraintVar( [1,2,3],'A1' )
        # A2 = ConstraintVar( [1,2,3],'A2' ) ...
        # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
        # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
        #   but you can see how tedious this would be.
        # Get rid of spaces and carriage returns from input
        
        delim,  equation = csp.input.split(',')
        vars,   solution = problems.split('=')
        varNames = vars.split(delim)
        for var in varNames:
            csp.variables[var] = ConstraintVar(['Baseball','Tennis','Basketball','Soccer'],var)
        
        # establish the allDiff constraint for each column and each row
        # for AC3, all constraints would be added to the queue 
        
        # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...   
        for r in varNames:
            aRow = []
            for k in variables.keys():
                if ( str(k).startswith(r) ):
            #accumulate all ConstraintVars contained in row 'r'
                    aRow.append( variables[k] )
        #add the allDiff constraints among those row elements
            allDiff( csp.constraints, aRow )


def AC3(csp):
    queue = []
    
    
    # for example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
    # for c in cols:
        # aCol = []
        # for k in variables.keys():
            # key = str(k)
            # the column is indicated in the 2nd character of the key string
            # if ( key[1] == c ):
        # accumulate all ConstraintVars contained in column 'c'
                # aCol.append( variables[k] )
        # allDiff( constraints, aCol )
#--------------------------------------------------------------------------------------------
#########################            COMPLETE REVISE               ##########################
def Revise3( bc ):
    dom1 = list(bc.var1.domain)
    dom2 = list(bc.var2.domain)
    dom3 = list(bc.var3.domain)
    # for each value in the domain of variable 1
    new = [[],[],[]]
    for x in dom1:
        satisfy_x = False
        for y in dom2:
            satisfy_y = False
            
            for z in dom3:
                
                if bc.func(x,y,z):
                    satisfy_x,satisfy_y = True
                    if z not in new_z:
                        new_z.append(z)
                    
            if satisfy_y and y not in new_y:
                new_y.append(y)
                
        if satisfy_x:
            new_x.append(x)
        
        
    bc.var1.domain = new_x
    bc.var2.domain = new_y
    bc.var3.domain = new_z
    
    
def Revise( bc ):
    # The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
    # A single BinaryConstraint instance is passed in to this function. 
    # MISSSING the part about returning sat to determine if constraints need to be added to the queue
    
    # copy domains for use with iteration (they might change inside the for loops)
    dom1 = list(bc.var1.domain)
    dom2 = list(bc.var2.domain)
    
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
        # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
#>>>>>
        
def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

def generalizedArcConsistent( gc, name ):
    domains     = []
    new_domain  = []
    index       = -1
    for i,v in enumarate(gc.vars):
        if name == v.name:
            index = i
        domains.append(var.domain)
    args_list = list(itertools.product(*domains))
    for args in args_list:
        if args[index] in new_domain:
            continue
        elif gc.fn(*args):
            new_domain.append(args[index])
    gc.vars[index].domain = new_domain
    return (len(new_domain) > 0)
    

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')



class BacktrackingSearch:
    def __init__(self,NodeOrder,ValueOrder,Inference):
        self.NodeOrder  = NodeOrder
        self.ValueOrder = ValueOrder
        self.Inference  = Inference
    
    def Backtracking(self,csp):
        return Backtrack(dict(),csp)
    
    def Backtrack(self,assignment,csp):
        if self.IsComplete(assignment):
            return assignment
        var = self.NodeOrder(csp)
        for val in self.ValueOrder(var, assignment, csp):
            if self.IsConsistent(var,assignment):
                assignment[var.name] = val
                inferences = self.Inference(csp, var, val)
                if len(inferences) > 0:
                    assignment.extend(inferences)
                    result = Backtrack(assignment,csp)
                    if len(result) > 0:
                        return result
            #Remove inferences and the new var from assignment
            for key in assignment.iterkeys():
                del assignment[key]
            del assignment[var.name]
        return None

    def IsConsistent(self,var,assignment):
        return True
    
    def IsComplete(self,assignment):
        for key in assignment.iterkeys():
            if len(assignment[key].domain) != 1:
                return False
        return True    
    
    def IsFailure(self,var):
        for key in var:
            pass
    
    
def AC3(csp):
    queue = []
    
    while len(queue) > 0:
        var = queue.pop(0)
        if Revise(csp,var):
            if len(var.domain) == 0:
                return False
            for n in var.n:
                queue.append(n)
    return True
    
def tryAC3():
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    variables = dict()
    constraints = []
    
    setUpKenKen( variables, constraints)
    
    print("initial domains")
    printDomains( variables )

    nodeConsistent( UnaryConstraint( variables['A3'], lambda x: x==2 ) )
    print("unary constraint A3")
    printDomains( variables )
    # KenKen
    ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    constraints.append( BinaryConstraint( variables['A1'], variables['A2'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['A2'], variables['A1'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: (x/y == 2) or (x/y == 1/2) ) )
    constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: (x/y == 2) or (x/y == 1/2) ) )
    constraints.append( BinaryConstraint( variables['B2'], variables['B3'], lambda x,y: (x/y == 3) or (x/y == 1/3) ) )
    constraints.append( BinaryConstraint( variables['B3'], variables['B2'], lambda x,y: (x/y == 3) or (x/y == 1/3) ) )
    constraints.append( BinaryConstraint( variables['C2'], variables['C3'], lambda x,y: abs(x-y) == 1 ) )
    constraints.append( BinaryConstraint( variables['C3'], variables['C2'], lambda x,y: abs(x-y) == 1 ) )
    
    allDiff(constraints, [variables['A1'], variables['A2'], variables['A3']])
    allDiff(constraints, [variables['B1'], variables['B2'], variables['B3']])
    allDiff(constraints, [variables['C1'], variables['C2'], variables['C3']])
    allDiff(constraints, [variables['A1'], variables['B1'], variables['C1']])
    allDiff(constraints, [variables['A2'], variables['B2'], variables['C2']])
    allDiff(constraints, [variables['A3'], variables['B3'], variables['C3']])
    allDiff(constraints, [variables['A1'], variables['A2'], variables['A3']])
    allDiff(constraints, [variables['B1'], variables['B2'], variables['B3']])
    allDiff(constraints, [variables['C1'], variables['C2'], variables['C3']])
    allDiff(constraints, [variables['A1'], variables['B1'], variables['C1']])
    allDiff(constraints, [variables['A2'], variables['B2'], variables['C2']])
    allDiff(constraints, [variables['A3'], variables['B3'], variables['C3']])
    
    for c in constraints:
        Revise( c )
    print("all constraints pass 1")
    printDomains( variables )
    
    for c in constraints:
        Revise( c )
    print("all constraints pass 2")
    printDomains( variables )

    for c in constraints:
        Revise( c )
    print("all constraints pass 3")
    printDomains( variables )
    
    variables = dict()
    constraints = []
    setUpLogicPuzzle1(variables, constraints)
    
    print("initial domains")
    printDomains( variables )

    #nodeConsistent( UnaryConstraint( variables['Jessica'], lambda x: x not in ['Soccer', 'Basketball']))
    print("unary constraint A3")
    printDomains( variables )
    #Logic Puzzle 1
    ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    constraints.append( UnaryConstraint( variables['Jessica'], lambda x: x not in ['Soccer', 'Basketball']) )
    constraints.append( UnaryConstraint( variables['Ryan'], lambda x: x not in ['Basketball','Baseball','Soccer']) )
    constraints.append( UnaryConstraint( variables['Alex'], lambda x: x not in ['Soccer']) )
    allDiff(constraints, [variables['Alex'], variables['Jessica'], variables['Ryan'], variables['Sophie']])
    
    for c in constraints:
        if isinstance(c,UnaryConstraint):
            nodeConsistent( c )
        else:
            Revise( c )
    print("all constraints pass 1")
    printDomains( variables )
    
    for c in constraints:
        if isinstance(c,UnaryConstraint):
            nodeConsistent( c )
        else:
            Revise( c )
    print("all constraints pass 2")
    printDomains( variables )
    '''
    #Logic Puzzle 2
    ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    constraints.append( BinaryConstraint( variables['A1'], variables['A2'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['A2'], variables['A1'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: (x/y == 2) or (x/y == 1/2) ) )
    constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: (x/y == 2) or (x/y == 1/2) ) )
    constraints.append( BinaryConstraint( variables['B2'], variables['B3'], lambda x,y: (x/y == 3) or (x/y == 1/3) ) )
    constraints.append( BinaryConstraint( variables['B3'], variables['B2'], lambda x,y: (x/y == 3) or (x/y == 1/3) ) )
    constraints.append( BinaryConstraint( variables['C2'], variables['C3'], lambda x,y: abs(x-y) == 1 ) )
    constraints.append( BinaryConstraint( variables['C3'], variables['C2'], lambda x,y: abs(x-y) == 1 ) )
    
    allDiff(constraints, [variables['A1'], variables['A2'], variables['A3']])
    allDiff(constraints, [variables['B1'], variables['B2'], variables['B3']])
    allDiff(constraints, [variables['C1'], variables['C2'], variables['C3']])
    allDiff(constraints, [variables['A1'], variables['B1'], variables['C1']])
    allDiff(constraints, [variables['A2'], variables['B2'], variables['C2']])
    allDiff(constraints, [variables['A3'], variables['B3'], variables['C3']])
    
    for c in constraints:
        Revise( c )
    print("all constraints pass 1")
    printDomains( variables )
    
    for c in constraints:
        Revise( c )
    print("all constraints pass 2")
    printDomains( variables )

    for c in constraints:
        Revise( c )
    print("all constraints pass 3")
    printDomains( variables )
    #print('----------------------------------------------------------')
    #print('TO DO:')
    #print('1) Write the function revise().')
    #print('2) Complete the binary constraints for KenKen puzzle.')
    #print('3) Run code and confirm that all domains are reduced to single value.')
    #print('')
    #print('4) Create the variables and constraints for the sport logic puzzle.')
    #print('-- Do not hand edit the domains based on Unary constraints. Define those as part of the puzzle.')
    #print('5) Solve the puzzle using nodeConsistent() and revise().')

    #print(' IF you finish all of that, see if you can frame the person-animal-color puzzle for AC3')

    #print('NOTE, the implementation of AC3 requires a queue on which you pop a constraint, then push neighbors if necessary')
    #print('   Since this is not implemented here, you can create a "hack" by repeatedly calling Revise.')
    #print('----------------------------------------------------------')
    #print(' SUBMIT your code via TurnItIn (whatever state it is in when class is over is fine.')
    '''
puzzleParser = PuzzleParser()
f = open('Test/testCrossMath.txt','r')
text = f.read()
f.close()
for puzzle in text.split('\n'):
    csp = puzzleParser.setUpCrossMath(puzzle)
    
    

    

    
    



