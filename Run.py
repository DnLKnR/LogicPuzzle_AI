from AC3 import *
from Backtracking import *
from Consistent import *
from Constraint import *
from Inferences import *
from Order import *
from Parse import *


puzzleParser = PuzzleParser()
f = open('Test/testCrypt.txt','r')
text = f.read()
f.close()
for puzzle in text.split('\n'):
    if "#" in puzzle:
        break
    csp = puzzleParser.setUpCrypt(puzzle)
    bts = BacktrackingSearch(csp,"mrv","no","fc")
    bts.run(csp)