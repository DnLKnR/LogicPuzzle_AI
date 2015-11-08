from Constraint import ConstraintSatisfactionProblem



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
    

def Degree(csp):
    
    pass