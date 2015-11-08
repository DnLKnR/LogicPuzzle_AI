

## PSEUDOCODE FROM THE BOOK ##

def Backtracking_Search(csp):
    return Backtrack({},csp)

def Backtrack(assignment, csp):
    if assignment is complete:
        return assignment
    var = Hueristic(csp)
    for value in Order_Domain_Values(var, assignment, csp):
        if value is consistent with assignment:
            add {var = value} to assignment
            inferences = Inference(csp, var, value)
            if inferences != failure:
                add inferences to assignment
                result = Backtrack(assignment, csp)
                if result != failure:
                    return result
        remove {var = value} and inferences from assignment
    return failure
