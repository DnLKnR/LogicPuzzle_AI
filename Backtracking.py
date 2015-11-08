from Constraint import *



class BacktrackingSearch:
    def __init__(self,NodeOrder,ValueOrder,Inference):
        self.NodeOrder  = NodeOrder
        self.ValueOrder = ValueOrder
        self.Inference  = Inference
    
    def Backtracking(self,csp):
        return self.Backtrack(dict(),csp)
    
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
                    result = self.Backtrack(assignment,csp)
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
