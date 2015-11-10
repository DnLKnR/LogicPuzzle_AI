from Consistent import *
from Constraint import *
from AC3        import *
### INFERENCES ###

class Inference:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order.replace(' ','').lower()
        self.consistent = Consistent()
        #self.AC3    = AC3()
        if self.order in ["mac", "maintainingarcconsistency"]:
            self.function = self.maintainingArcConsistency
        elif self.order in ["fc","forwardchecking"]:
            self.function = self.forwardChecking
        else:
            self.function = self.noInference
    
    ############################    
    ## INTERNAL USE FUNCTIONS ##
    ############################  
    def forwardChecking(self, csp, variable):
        inference = dict()
        for constraint in variable.constraints:
            if isinstance(constraint, BinaryConstraint):
                inference = self.consistent.inferAC(variable, constraint, inference)
                if inference == None:
                    return None
        return inference
    
    def maintainingArcConsistency(self, csp, variable):
        ## TODO: Implement after completing AC3
        ac3 = AC3()
        csp_copy = csp.copy()
        ac3.AC3(csp_copy, variable.constraints)
        return csp_copy.variables
    
    def noInference(self, csp, var):
        return csp.variables
    
    ############################
    ## EXTERNAL USE FUNCTIONS ##
    ############################
    def get(self, csp, var):
        #print("getting inference")
        return self.function(csp, var)