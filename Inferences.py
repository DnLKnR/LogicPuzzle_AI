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
    def forwardChecking(self, csp, var, val):
        pass
    
    def maintainingArcConsistency(self, csp, var, val):
        pass
    
    def noInference(self, csp, var, val):
        pass
    
    ## UTILITY FUNCTIONS, 
    ## THESE SHOULD ONLY BE CALLED OUTSIDE OF THE CLASS 
    def get(self, csp, var, val):
        return self.function(csp, var, val)