from Constraint import *
from itertools  import product
    
def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            uc.var.domain.remove(x)

def arcConsistent( bc ):
    domain1 = list(bc.var1.domain)
    domain2 = list(bc.var2.domain)
    for x in domain1:
        satisfy = False
        for y in domain2:
            if bc.func(x,y):
                satisfy = True
                break
        if not satisfy:
            bc.var1.domain.remove(x)

def generalizedArcConsistent( gc ):
    domain      = list(gc.var[0].domain)
    domains     = []
    for v in gc.vars[1:]:
        domains.append(v.domain)
    # Product takes in a list of lists and returns all
    # possible forward combinations of one element in each list
    # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
    args_list = list(product(*domains))
    # Loop through all arg combinations, and find ones where the first
    # variable cannot satisfy the defined function and remove it 
    # from the domain of the first variable
    for x in domain:
        satisfy = False
        for args in args_list:
            if gc.fn(x,*args):
                satisfy = True
                break
        if not satisfy:
            gc.var1.domain.remove(x)
    
def pathConsistent( tc ):
    domain1 = list(tc.var1.domain)
    domain2 = list(tc.var2.domain)
    domain3 = list(tc.var3.domain)
    new_domain1 = []
    new_domain2 = []
    for x in domain1:
        satisfy_x = False
        for y in domain2:
            satisfy_y = False
            for z in domain3:
                if tc.func(x,y,z):
                    satisfy_x = True
                    satisfy_y = True
                    break
            if satisfy_y and y not in new_domain2:
                new_domain2.append(y)
        if satisfy_x and x not in new_domain1:
            new_domain1.append(x)
    tc.var1.domain = new_domain1
    tc.var2.domain = new_domain2

def kConsistent( gc ):
    ## Gather the domains of all the variables and 
    ## instantiate the array that will contain the
    ## updated domains based on the global constraint
    domains         = []
    new_domains     = []
    for v in gc.vars:
        domains.append(v.domain)
        new_domains.append([])
    # Product takes in a list of lists and returns all
    # possible forward combinations of one element in each list
    # ex. [[1,2,3],[2,3,4],[4,5,6]] => [(1,2,4),(1,2,5),...(3,4,6)]
    args_list = list(product(*domains))
    # Loop through all arg combinations, and find ones that satisfy
    # the global constraint function.  Update the new domains with
    # their respective values.
    for args in args_list:
        if gc.fn(*args):
            for i,v in enumerate(args):
                if v not in new_domains[i]:
                    new_domains[i].append(v)
    ## Note: we only care to update k-1 domains. The last domain remains
    ## unaltered per the definition of K-consistency in the book
    for i,new_domain in enumerate(new_domains[:-1]):
        gc.vars[i] = new_domain