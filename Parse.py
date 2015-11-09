from Constraint import *
import re
import operator

# Thanks StackOverflow: http://stackoverflow.com/questions/1740726/python-turn-string-into-operator
ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv,
       '==': operator.eq,
       '!=': operator.ne,
       '<': operator.lt,
       '<=': operator.le,
       '>': operator.gt,
       '>=': operator.ge,
       'abs': operator.abs,
       '^': operator.pow
       }


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
        start,end,is_special = 0, 0, False
        vars      = []
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
    
    def getOps(self,equation):
        operators = ["+","-","*","/","^"]
        ops_list  = []
        for char in equation:
            if char in operators:
                ops_list.append(char)
        return ops_list
    
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
            parens  = ("(" in problem)
            vars    = self.getVars(problem)
            opers   = self.getOps(problem)
            for var in vars:
                if var not in variables:
                    variables.append(var)
            vars_str = ','.join(vars)
            ## If the problem has parenthesis, follow their order of operation
            if parens:
                function = "lambda {0}:{1}=={2}".format(vars_str,problem,solution)
            ## Otherwise follow game rules, make sure to ignore order of operation 
            ## and go left to right
            else:
                problem_1 = opers[0].join(vars[:2])
                problem_2 = opers[1] + vars[2]
                function = "lambda {0}:({1}){2}=={3}".format(vars_str,problem_1,problem_2,solution)
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
            gc.neighborize()
        
        self.allDiff(csp)
        print("")
        print("Input: {0}".format(input))
        print("Starting Configuration:")
        printDomains(csp.variables)
        
        return csp
    
    def setUpCrypt(self,input):
        ## Instantiate the CSP object ##
        csp     = ConstraintSatisfactionProblem()
        ## Input should be a single line, defining one problem ##
        input   = input.replace(' ','').replace('\r','').replace('\n','')
        delim,  equation = input.split(',')
        problem,solution = equation.split('=')
        
        variables = problem.split(delim)
        characters = []
        var_str = ''.join(variables) + solution
        for char in var_str:
            if char not in characters:
                characters.append(char)
        variables_str = [[]]
        for char in equation:
            if delim == char or char == '=':
                variables_str.append([])
            else:
                variables_str[-1].append("str({0})".format(char))
        string = []
        for variable_strs in variables_str:
            string.append("int({0})".format('+'.join(variable_strs)))
        
        
        function = '=='.join([delim.join(string[:-1]),
                              string[-1]])
        print(function)
        lambda_fn = "lambda {0}:{1}".format(','.join(characters),function)
        cv = []
        for char in characters:
            domain = list(range(0,10))
            cv.append(ConstraintVar(domain,char))
            csp.variables[char] = cv[-1]
        fn = eval(lambda_fn)
        csp.constraints = [GlobalConstraint(cv,fn)]
        return csp
    
    