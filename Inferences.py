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
        for constraint in csp.constraints:
            #print("evaluating inferences...")
            #We only care about the arcs when we forward check
            if isinstance(constraint, BinaryConstraint) and constraint.contains(variable):
                #print("starting Arc Consistency")
                #start = time()
                inference = self.consistent.inferAC(variable, constraint, inference)
                #end   = time()
                #print("completed Arc Consistency in {0}".format(end-start))
                if inference == None:
                    return None
        print("...result True")
        return inference
    
    def maintainingArcConsistency(self, csp, variable):
        ## TODO: Implement after completing AC3
        inference = dict()
        consistent = Consistent()
        for key in csp.variables:
            inference[key] = csp.variables[key].copy()
        for constraint in csp.constraints:
            if constraint.contains(variable):
                if isinstance(constraint, BinaryConstraint):
                    consistent.AC(constraint, inference)
                elif isinstance(constraint, GlobalConstraint):
                    consistent.GAC(constraint, inference)
                if inference == None:
                    return None
        return inference
    
    def noInference(self, csp, var):
        return csp.variables
    
    ############################
    ## EXTERNAL USE FUNCTIONS ##
    ############################
    def get(self, csp, var):
        #print("getting inference")
        return self.function(csp, var)