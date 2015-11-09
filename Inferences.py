from Consistent import *
from Constraint import *
from AC3        import *
### INFERENCES ###

class Inference:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order.replace(' ','').lower()
        #self.AC3    = AC3()
        if self.order in ["mac", "maintainingarcconsistency"]:
            self.function = self.maintainingArcConsistency
        elif self.order in ["fc","forwardchecking"]:
            self.function = self.forwardChecking
        else:
            self.function = self.noInference
    
    ## INFERENCE FUNCTIONS (BELOW)
    ## THESE SHOULD NEVER DIRECTLY BE CALLED OUTSIDE OF THE CLASS 
    def forwardChecking(self, csp, variable):
        inference = dict()
        consistent = Consistent()
        for key in csp.variables:
            inference[key] = self.copy(csp.variables[key])
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if isinstance(constraint, BinaryConstraint):
                    consistent.arcConsistent(constraint, inference)
                elif isinstance(constraint, GlobalConstraint):
                    consistent.generalizedArcConsistent(constraint, inference)
                if inference == None:
                    return None
        return inference
    
    def maintainingArcConsistency(self, csp, variable):
        inference = dict()
        consistent = Consistent()
        for key in csp.variables:
            inference[key] = self.copy(csp.variables[key])
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if isinstance(constraint, BinaryConstraint):
                    consistent.arcConsistent(constraint, inference)
                elif isinstance(constraint, GlobalConstraint):
                    consistent.generalizedArcConsistent(constraint, inference)
                if inference == None:
                    return None
        return inference
    
    def noInference(self, csp, var):
        return csp.variables
    
    ## INTERNAL UTILITY FUNCTIONS ##
    def copy(self, variable):
        return ConstraintVar(list(variable.domain), variable.name)
    ## UTILITY FUNCTIONS
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS 
    def get(self, csp, var):
        return self.function(csp, var)