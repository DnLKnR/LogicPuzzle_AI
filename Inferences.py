from Consistent import *
from Constraint import *

### INFERENCES ###

class Inference:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order.replace(' ','').lower()
        if self.order in ["mac", "maintainingarcconsistency"]:
            self.function = self.maintainingArcConsistency
        elif self.order in ["fc","forwardchecking"]:
            self.function = self.forwardChecking
        else:
            self.function = self.noInference
    
    ## INFERENCE FUNCTIONS (BELOW)
    ## THESE SHOULD NEVER DIRECTLY BE CALLED OUTSIDE OF THE CLASS 
    def forwardChecking(self, csp):
        pass
    
    def maintainingArcConsistency(self, csp):
        inference = dict()
        consistent = Consistent()
        for key in csp.variables:
            inference[key] = self.copy(csp.variables[key])
        for constraint in csp.constraints:
            if isinstance(constraint, BinaryConstraint):
                inference = consistent.arcConsistent(constraint, inference)
            elif isinstance(constraint, GlobalConstraint):
                inference = consistent.generalizedArcConsistent(constraint, inference)
            if inference == None:
                return None
        return inference
    
    def noInference(self, csp):
        return csp.variables
    
    ## INTERNAL UTILITY FUNCTIONS ##
    def copy(self, variable):
        return ConstraintVar(variable.domain, variable.name)
    ## UTILITY FUNCTIONS
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS 
    def get(self, csp):
        return self.function(csp)