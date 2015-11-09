from AC3 import *
from Backtracking import *
from Parse import *
from time import time
x = 2
puzzleParser = PuzzleParser()
#f = open('Test/testCrypt.txt','r')
f = open('Test/testCrossMath.txt','r')
text = f.read()
f.close()
for count,puzzle in enumerate(text.split('\n')):
    #if count != x:
       # continue
    if "#" in puzzle:
        break
    csp = puzzleParser.setUpCrossMath(puzzle)
    #csp = puzzleParser.setUpCrypt(puzzle)
    bts = BacktrackingSearch(csp,"mrv","ro","fc")
    #ac3 = AC3()
    
    start = time()
    #ac3.run(csp)
    bts.run(csp)
    end = time()
    print("With constraint sorting:\t{}".format(end-start))
    #===========================================================================
    
    # csp = puzzleParser.setUpCrossMath(puzzle)
    # start = time()
    # bts = BacktrackingSearch(csp,"d","ro","fc", False)
    # end   = time()
    # print("Without constraint sorting:\t{}".format(end-start))
    #===========================================================================
    #break