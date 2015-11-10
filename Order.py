from Constraint import *
from Consistent import *
from random     import random
## Domain Value Ordering functions for Backtracking Search ##
class ValueOrder:
    def __init__(self,csp,order):
        self.csp = csp
        self.order = order.replace(' ','').lower()
        self.consistent = Consistent()
        if self.order in ["lcv", "leastconstrainingvalue"]:
            self.function = self.leastConstrainingOrder
        elif self.order in ["r","random"]:
            self.function = self.randomOrder
        else:
            self.function = self.noOrder
   
    ############################    
    ## INTERNAL USE FUNCTIONS ##
    ############################ 
    def noOrder(self, var, csp):
        '''Returns the values as they are present in the domain'''
        return var.domain
    
    def randomOrder(self, var, csp):
        '''Returns a random value order for the variable'''
        return sorted(var.domain, key=lambda x: random())
    
    def leastConstrainingOrder(self, var, csp):
        '''Computes and returns a list that is ordered based on
           the number of values that will be ruled out if a certain
           value is chosen....very high in time-complexity '''
        value_pair = []
        for value in var.domain:
            #print("For value - " + str(value))
            copy_csp = csp.copy()
            copy_csp.variables[var.name].domain = [value]
            variable = copy_csp.variables[var.name]
            self.consistent.execute(variable, copy_csp)
            count = 0
            for key in copy_csp.variables:
                count += (len(csp.variables[key].domain) - len(copy_csp.variables[key].domain))
                #print("Domain changes from:\t" + str(csp.variables[key].domain))
                #print("Domain changes to:\t" + str(copy_csp.variables[key].domain))
            value_pair.append([value,count])
            del copy_csp
        value_pair = sorted(value_pair,key=lambda x: x[1])
        #print(value_pair)
        sorted_domain = []
        for v in value_pair:
            sorted_domain.append(v[0])
        return sorted_domain
    
    ############################
    ## EXTERNAL USE FUNCTIONS ##
    ############################
    def get(self, var, csp):
        return self.function(var, csp)



## Node Ordering functions for Backtracking Search ##
class NodeOrder:
    def __init__(self,csp,order):
        self.csp    = csp
        self.order  = order.replace(' ','').lower()
        if order in ["mrv","minimumremainingvalues"]:
            self.function = self.minimumRemainingValuesOrder
        elif order in ["r","random"]:
            self.function = self.randomOrder
        elif order in ["d","degree"]:
            self.function = self.degreeOrder
        else:
            self.function = self.noOrder
            
        self.function(csp,True)

    ############################    
    ## INTERNAL USE FUNCTIONS ##
    ############################  
    def randomOrder(self,csp, create=False):
        '''generate a randomly sorted queue through
           the use of the random number generator'''
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])
        
        self.queue = sorted(self.queue, key=lambda x: random())

    def noOrder(self,csp, create=False):
        '''leave the queue as it is, collect all the variables
           from the dictionary and then never touch the queue
           again'''
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])

    def minimumRemainingValuesOrder(self,csp, create=False):
        '''this ordering returns the most constrained variable
           which is interpreted as the value with the least amount
           of domain values that is left in the queue.'''
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])
        
        self.queue = sorted(self.queue, key=lambda x: len(x.domain))

    def degreeOrder(self, csp, create=False):
        '''sort the queue based upon the evaluate degree function value
           which computes the number of constraints that a variable is
           involved with that also still has unassigned values'''
        if create:
            self.queue = []
            for key in csp.variables:
                self.queue.append(csp.variables[key])
        
        self.queue = sorted(self.queue, key=lambda x: self.evaluateDegree(x, csp.constraints), reverse=True)
    
    ####################################    
    ## INTERNAL USE UTILITY FUNCTIONS ##
    #################################### 
    def evaluateDegree(self,variable,constraints):
        '''evaluate how many constraints the variable is involved with 
           that still have unassigned (length of domain > 1) variables
           attached to them'''
        count = 0
        for constraint in constraints:
            count += constraint.unassigned(variable)
        return count
    
    ############################
    ## EXTERNAL USE FUNCTIONS ##
    ############################
    def get(self,csp,index=0,reset=False):
        '''Simply resorts the list through the function that was defined
           when the class was instantiated, and returns the first element'''
        self.function(csp,reset)
        return self.queue[index]
        
    def pop(self,csp,index=0,reset=False):
        '''Simply resorts the list through the function that was defined
           when the class was instantiated, and removes and returns the 
           first element'''
        self.function(csp,reset)
        return self.queue.pop(index)
    
    def push(self,csp,var,index=0,reset=False):
        '''Simply adds the variable passed in to the function to the list
           and resorts the list through the function that was defined
           when the class was instantiated'''
        self.queue.insert(0,var)
        self.function(csp,reset)
        
        
    
    
        