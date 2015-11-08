from Constraint import *
from AC3 import *

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
        ## Instantiate the CSP object ##
        csp     = ConstraintSatisfactionProblem()
        ## Input should be a single line, defining one problem ##
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
            function = eval("lambda {0}:{1}".format(vars_str, relation))
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