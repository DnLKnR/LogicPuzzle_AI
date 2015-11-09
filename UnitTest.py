from AC3            import *
from Backtracking   import *
from Consistent     import *
from Constraint     import *
from Inferences     import *
from Order          import *
from Parse          import *
import unittest


class TestConstraint(unittest.TestCase):
    def test_uc_contains(self):
        c1      = ConstraintVar([30],"test1")
        uc      = UnaryConstraint(c1, None)
        ctrue   = ConstraintVar([1],"test1")
        cfalse  = ConstraintVar([1],"test2")
        self.assertTrue(uc.contains(ctrue))
        self.assertFalse(uc.contains(cfalse))
        
    def test_uc_complete(self):
        c1 = ConstraintVar([30],"test1")
        uc = UnaryConstraint(c1, lambda x: x % 13 == 4)
        self.assertTrue(uc.complete())
        
    def test_bc_contains(self):
        c1 = ConstraintVar([1],"test1")
        c2 = ConstraintVar([1],"test3")
        bc = BinaryConstraint(c1, c2, None)
        ctrue   = ConstraintVar([1],"test1")
        cfalse  = ConstraintVar([1],"test2")
        self.assertTrue(bc.contains(ctrue))
        self.assertFalse(bc.contains(cfalse))
        
    def test_bc_complete(self):
        c1 = ConstraintVar([30],"test1")
        c2 = ConstraintVar([7], "test3")
        bc = BinaryConstraint(c1, c2, lambda x,y: x // y == 4)
        self.assertTrue(bc.complete())
        
    def test_gc_contains(self):
        c1 = ConstraintVar([1], "test1")
        c2 = ConstraintVar([1], "test2")
        c3 = ConstraintVar([1], "test3")
        gc = GlobalConstraint([c1,c2,c3], None) 
        ctrue   = ConstraintVar([1],"test1")
        cfalse  = ConstraintVar([1],"test4")
        self.assertTrue(gc.contains(ctrue))
        self.assertFalse(gc.contains(cfalse))
        
    def test_gc_complete_1(self):
        c1 = ConstraintVar([30],"test1")
        c2 = ConstraintVar([5], "test2")
        c3 = ConstraintVar([7], "test3")
        gc = GlobalConstraint([c1,c2,c3], lambda x,y,z: x+y-z == 28) 
        self.assertTrue(gc.complete())
        
    def test_gc_complete_2(self):
        c1 = ConstraintVar([30],"test1")
        c2 = ConstraintVar([5], "test2")
        c3 = ConstraintVar([7,9], "test3")
        gc = GlobalConstraint([c1,c2,c3], lambda x,y,z: x+y+z>0)
        self.assertFalse(gc.complete())
        
    def test_gc_complete_3(self):
        c1 = ConstraintVar([30],"test1")
        c2 = ConstraintVar([5], "test2")
        c3 = ConstraintVar([7], "test3")
        gc = GlobalConstraint([c1,c2,c3], lambda x,y,z: x+y+z==43)
        self.assertFalse(gc.complete())
        
class TestConsistent(unittest.TestCase):
    def test_isNC(self):
        con = Consistent()
        c1 = ConstraintVar([10,20,23,30],"test1")
        uctrue  = UnaryConstraint(c1, lambda x: x<31)
        ucfalse = UnaryConstraint(c1, lambda x: x<29)
        self.assertTrue(con.evaluate(c1,uctrue))
        self.assertFalse(con.evaluate(c1,ucfalse))
        
    def test_isAC(self):
        con = Consistent()
        c1 = ConstraintVar([10,20,22,30], "test1")
        c2 = ConstraintVar([11,23,29,28], "test2")
        uc1  = BinaryConstraint(c1, c2, lambda x,y: (x + y) % 2 == 1)
        uc2  = BinaryConstraint(c1, c2, lambda x,y: x < y)
        self.assertTrue(con.evaluate(c1,uc1))
        self.assertFalse(con.evaluate(c2,uc1))
        self.assertFalse(con.evaluate(c1,uc2))
        self.assertTrue(con.evaluate(c2,uc2))
         
    def test_isGAC(self):
        con = Consistent()
        c1 = ConstraintVar([36,38,40], "test1")
        c2 = ConstraintVar([33,29,31,32], "test2")
        c3 = ConstraintVar([34,14,12,10,18,2], "test3")
        uc1  = GlobalConstraint([c1,c2,c3], lambda x,y,z: (x + y + z) % 2 == 1)
        uc2  = GlobalConstraint([c1,c2,c3], lambda x,y,z: x < y + z)
        uc3  = GlobalConstraint([c1,c2,c3], lambda x,y,z: x > y and y > z)
        ## Part 1 ##
        self.assertTrue(con.evaluate(c1,uc1))
        self.assertFalse(con.evaluate(c2,uc1))
        self.assertTrue(con.evaluate(c3,uc1))
        ## Part 2 ##
        self.assertTrue(con.evaluate(c1,uc2))
        self.assertTrue(con.evaluate(c2,uc2))
        self.assertFalse(con.evaluate(c3,uc2))
        ## Part 3 ##
        self.assertTrue(con.evaluate(c1,uc3))
        self.assertTrue(con.evaluate(c2,uc3))
        self.assertFalse(con.evaluate(c3,uc3))

class TestParse(unittest.TestCase):
    def test_crossmath(self):
        pass
    
    #def test_crypt(self):
    
        
if __name__ == '__main__':
    unittest.main()