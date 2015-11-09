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
        #Set up the variables
        # read in the file with constraints for KenKen puzzles (1 line per puzzle)
        lines = open('testCrypt.txt').readlines()
        testLine = 4 # test this line in file
        l = lines[testLine]
        #remove white space
        l=re.sub('[ ]','',l)
        print('l ',l)
    
        # determine operator and remove, find "answer"
        op = re.findall('^\W',l)
        print('op ',op)
        l = re.sub('^\W,','',l)
        answer = re.findall('=\w+',l)
        answer = re.sub('=','',answer[0])
        print('l ',l,'answer ',answer)
    
        # start a dictionary of variables and a list of constraints
        Cons = []
    
        vars = []
        # separate values
        words = re.findall('\w+',l)
        for w in words:
            letters = re.findall('\w',w)
            for letter in letters:
                if letter not in vars: vars.append(letter)
        print('vars ',vars)
    
    