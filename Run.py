from AC3 import *
from Backtracking import *
from Consistent import *
from Constraint import *
from Inferences import *
from Order import *
from Parse import *


puzzleParser = PuzzleParser()
f = open('Test/testCrossMath.txt','r')
#f = open('Test/testCrypt.txt','r')
text = f.read()
f.close()
for puzzle in text.split('\n'):
    if "#" in puzzle:
        break
    csp = puzzleParser.setUpCrossMath(puzzle)
    #csp = puzzleParser.setUpCrypt(puzzle)
    bts = BacktrackingSearch(csp,"no","lcv","no")
    bts.run(csp)