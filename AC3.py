import functools
from functools import reduce
from Backtracking import BacktrackingSearch
from Parse import PuzzleParser




class AC3:
    def __init__(self):
        pass
    
    def allDiff( constraints, v ):    
        # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
        # constraints is a preconstructed list. v is a list of ConstraintVar instances.
        # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
        fn = lambda x,y: x != y
        for i in range(len(v)):
            for j in range(len(v)):
                if ( i != j ) :
                    constraints.append(BinaryConstraint(v[i],v[j],fn))
    
    def run(self,csp):
        pass
    
    def AC3(self,csp,queue):
        while len(queue) > 0:
            var = queue.pop(0)
            if Revise(csp,var):
                if len(var.domain) == 0:
                    return False
                for n in var.n:
                    queue.append(constraint)
        return True
        
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
    def Revise(self, gc):
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
        
        
    def Revise(self, bc):
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
    def printDomains( vars, n=3 ):
        count = 0
        for k in sorted(vars.keys()):
            print( k,'{',vars[k].domain,'}, ',end="" )
            count = count+1
            if ( 0 == count % n ):
                print(' ')
        
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

    
    

    

    
    



