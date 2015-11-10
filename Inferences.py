from Consistent import *
from Constraint import *
from AC3        import *
### INFERENCES ###

class Inference:
    def __init__(self,csp,order,GACEnabled):
        self.GACEnabled = GACEnabled
        self.csp = csp
        self.order = order.replace(' ','').lower()
        self.consistent = Consistent(GACEnabled)
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
        '''Forward Checking Inference function'''
        inference = dict()
        for constraint in variable.constraints:
            if isinstance(constraint, BinaryConstraint):
                inference = self.consistent.inferAC(variable, constraint, inference)
                if inference == None:
                    return None
        return inference
    
    def maintainingArcConsistency(self, csp, variable):
        '''Maintaining Arc Consistency Inference function'''
        ac3 = AC3(self.GACEnabled)
        csp_copy = csp.copy()
        queue = []
        for var in ac3.getNeighbors(variable):
            queue.extend(ac3.getConstraints(var,variable))
        ac3.AC3(csp_copy, [queue[0]])
        return csp_copy.variables
    
    def noInference(self, csp, var):
        return csp.variables
    
    ############################
    ## EXTERNAL USE FUNCTIONS ##
    ############################
    def get(self, csp, var):
        return self.function(csp, var)