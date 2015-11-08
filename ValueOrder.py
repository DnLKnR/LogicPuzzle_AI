from Constraint import *

## These functions have to return a list ##

def Default(var, assignment, csp):
    pass

def RandomValue(var, assignment, csp):
    pass

def LeastConstrainingValue(var, assignment, csp):
    min = 1000000000
    var = ""
    for key in csp.variables.iterkeys():
        length = len(csp.variables[key])
        if min > length:
            var,max = key,length
    return var