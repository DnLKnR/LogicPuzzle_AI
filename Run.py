from AC3 import *
from Backtracking import *
from Consistent import *
from Constraint import *
from Inferences import *
from Order import *
from Parse import *


puzzleParser = PuzzleParser()
f = open('Test/testCrossMath.txt','r')
text = f.read()
f.close()
for puzzle in text.split('\n'):
    csp = puzzleParser.setUpCrossMath(puzzle)
    bts = BacktrackingSearch(csp,"no","no","mac")
    bts.run(csp)
    break