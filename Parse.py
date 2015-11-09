from Constraint import *



def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')

class PuzzleParser:
    def __init__(self):
        pass
    
    def allDiff(self,csp):    
        # generate a list of constraints that implement the allDiff constraint for all variable combinations in v
        # constraints is a preconstructed list. v is a list of ConstraintVar instances.
        # call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
        fn = lambda x,y: x != y
        for key1 in csp.variables:
            for key2 in csp.variables:
                if key1 != key2:
                    csp.constraints.append(BinaryConstraint(csp.variables[key1], 
                                                            csp.variables[key2], 
                                                            fn))
    
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
        ## Instantiate the CSP object ##
        csp     = ConstraintSatisfactionProblem()
        ## Input should be a single line, defining one problem ##
        input   = input.replace(' ','').replace('\r','').replace('\n','')
        equations = input.split(',')
        variables   = []
        constraints = []
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
            function = "lambda {0}:{1}".format(vars_str, relation)
            constraints.append([vars,function])
            
        #Set up the domains
        length = len(variables)
        for name in variables:
            domain = list(range(1, length + 1))
            csp.variables[name] = ConstraintVar(domain, name)
        for constraint in constraints:
            constraintVars, varNames = [], constraint[0]
            for name in varNames:
                constraintVars.append(csp.variables[name])
            function = eval(constraint[1])
            gc = GlobalConstraint(constraintVars,function)
            csp.constraints.append(gc)
        
        self.allDiff(csp)
        printDomains(csp.variables)
        print("")
        
        return csp
    
    #print(csp.input)
    #print(printDomains(csp.variables))
    #print(csp.constraints)
    
    def setUpCrypt(self,input):
        ## Instantiate the CSP object ##
        csp     = ConstraintSatisfactionProblem()
        ## Input should be a single line, defining one problem ##
        input   = input.replace(' ','').replace('\r','').replace('\n','')
        #Set up the variables
        delim,  equation = csp.input.split(',')
        vars,   solution = problems.split('=')
        varNames = vars.split(delim)
        for var in varNames:
            csp.variables[var] = ConstraintVar(['Baseball','Tennis','Basketball','Soccer'],var)
        
        # establish the allDiff constraint for each column and each row
        # for AC3, all constraints would be added to the queue 
        # lambda t,o,o,l,
        # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...   
        for r in varNames:
            aRow = []
            for k in variables.keys():
                if ( str(k).startswith(r) ):
            #accumulate all ConstraintVars contained in row 'r'
                    aRow.append( variables[k] )
        #add the allDiff constraints among those row elements
            allDiff( csp.constraints, aRow )