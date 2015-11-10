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
        #created = []
        for key1 in csp.variables:
            for key2 in csp.variables:
                if key1 != key2: #and [key2,key1] not in created:
                    csp.constraints.append(BinaryConstraint(csp.variables[key1],csp.variables[key2],fn))
                    csp.variables[key1].constraints.append(csp.constraints[-1])
                    csp.variables[key2].constraints.append(csp.constraints[-1])
                    #created.append([key1,key2])
                    # self.printConstraint([key1,key2], "lambda x,y: x != y")
    
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
            for constraintVar in constraintVars:
                constraintVar.constraints.append(gc)
            gc.neighborize()
        
        self.allDiff(csp)
        print("")
        print("Input: {0}".format(input))
        print("Starting Configuration:")
        printDomains(csp.variables)
        
        return csp
    
    def convertVariable(self,variable,number_base):
        ## Convert variable to something that can be used in an equation
        ## ex. send => ((s * 1000) + (e * 100) + (n * 10) + (d * 1))
        length = len(variable)
        parts  = []
        for i,char in enumerate(reversed(variable)):
            multiplier = number_base ** i
            string     = "({0} * {1})".format(char,multiplier)
            parts.insert(0,string)
        equation = "({0})".format('+'.join(parts))
        if len(parts) == 1:
            equation = "{0}".format('+'.join(parts))
        return equation
    
    def getParameters(self,equation):
        parameters = []
        alpha = "abcdefghijklmnopqrstuvwxyz"
        for char in equation:
            if char in alpha and char not in parameters:
                parameters.append(char)
        return parameters
    
    def createVariables(self,equation,csp,domain):
        variables = self.getParameters(equation)
        for variable in variables:
            csp.variables[variable] = ConstraintVar(domain,variable)
            
    def createConstraints(self,equation_parts,delim,number_base,csp):
        max_length = len(max(equation_parts[:-1],key=lambda x: len(x))) + 1
        #Make all Unary Constraints (since leading numbers cannot be 0)
        unary_var_str = []
        for part in equation_parts:
            if len(part) > 1 and part[0] not in unary_var_str:
                var = csp.variables[part[0]]
                fn  = lambda x: x != 0
                csp.constraints.append(UnaryConstraint(var,fn))
                var.constraints.append(csp.constraints[-1])
                self.printConstraint(part[0], "lambda x: x != 0")
                unary_var_str.append(part[0])
        #Make all Global Constraints, except for the final one
        for i in range(1,max_length):
            equation_arr = []
            for equation_part in equation_parts:
                equation_arr.append(self.convertVariable(equation_part[-i:],number_base))
            equation_str = "({0}) % {2} == ({1}) % {2}".format(delim.join(equation_arr[:-1]),equation_arr[-1],number_base ** i)
            #print(equation_str)
            parameters = self.getParameters(equation_str)
            param_str  = ','.join(self.getParameters(equation_str))
            lambda_fn  = "lambda {0}:{1}".format(param_str,equation_str)
            #print("Equation Part:")
            #print(lambda_fn)
            vars = self.gatherVariables(parameters,csp)
            fn   = eval(lambda_fn)
            csp.constraints.append(GlobalConstraint(vars,fn))
            for var in vars:
                var.constraints.append(csp.constraints[-1])
            self.printConstraint(parameters, lambda_fn)
    
    def gatherVariables(self,varNames,csp):
        variables = []
        for varName in varNames:
            variables.append(csp.variables[varName])
        return variables
        
    def setUpCrypt(self,input):
        ## Instantiate the CSP object ##
        csp     = ConstraintSatisfactionProblem()
        ## Input should be a single line, defining one problem ##
        input   = input.replace(' ','').replace('\r','').replace('\n','').lower()
        delim,  equation = input.split(',')
        problem,solution = equation.split('=')
        number_base     = 10
        domain          = list(range(number_base))
        ## Create the variables in the constraint satisfaction problem
        self.createVariables(equation,csp,domain)
        self.allDiff(csp)
        variables = problem.split(delim)
        self.createConstraints(variables + [solution], delim, number_base, csp)
        decimal_place = 0
        placers_str   = [[]]
        variables_str = [[]]
        # Reverse the string and evaluate it (for decimal purposes)
        for char in reversed(equation):
            if delim == char or char == '=':
                variables_str.append([])
                decimal_place = 0
            else:
                variables_str[-1].append("({0}*{1})".format(char,number_base ** decimal_place))
                decimal_place += 1
        # Reverse all the items back to normalize again
        for i,str in enumerate(variables_str):
            variables_str[i] = reversed(str)
        variables_str = reversed(variables_str)
        string = []
        for variable_strs in variables_str:
            string.append("({0})".format('+'.join(variable_strs)))
        function = '=='.join([delim.join(string[:-1]),string[-1]])
        
        #print(function)
        parameters = self.getParameters(function)
        
        param_str  = ','.join(parameters)
        lambda_fn = "lambda {0}:{1}".format(param_str,function)
        #print(lambda_fn)
        fn = eval(lambda_fn)
        
        vars = self.gatherVariables(parameters, csp)
        csp.constraints.append(GlobalConstraint(vars,fn))
        for var in vars:
            var.constraints.append(csp.constraints[-1])
        self.printConstraint(parameters, lambda_fn)
        print("Input: {0}".format(input))
        print("Starting Configuration:")
        printDomains(csp.variables)
        print("")
        return csp
    
    def printConstraint(self,variables,lambda_str):
        print("Constraint Values:")
        print("\tVariables:\t\t{0}".format(', '.join(variables)))
        print("\tLambda Function:\t{0}".format(lambda_str))
        
        
    
    