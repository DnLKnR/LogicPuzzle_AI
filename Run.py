from AC3 import *
from Backtracking import *
from Parse import *
from time import time

import timeit, argparse, sys

## CLASS FOR STORING COMMAND LINE ARGUMENTS ##
class Inputs:
    pass

## CREATE ARGUMENT PARSING OBJECT ##
parser = argparse.ArgumentParser(description="This program executes puzzles ")
parser.add_argument("-f",   metavar="FILE", dest="testfile",  nargs=1, default=["testCrossMath"], type=str,help="Specify a test file")
parser.add_argument("--inf",metavar="NAME", dest="infer",     nargs=1, default=["fc"],    type=str, help="specify a test from the test file")
parser.add_argument("--vo", metavar="NAME", dest="valueorder",nargs=1, default=["none"],  type=str, help="specify a test from the test file")
parser.add_argument("--no", metavar="NAME", dest="nodeorder", nargs=1, default=["degree"],type=str, help="specify a test from the test file")
parser.add_argument("-r",   metavar="INT",  dest="runs",      nargs=1, default=[1],  type=int,help="Number of executions for Run-Time Analysis")
parser.add_argument("--test",metavar="INT", dest="testnum",   nargs=1, default=[-1], type=int,help="Number of Towers (default is 3)")
parser.add_argument("--log",metavar="FILE", dest="log",       nargs=1, default=[""], type=str,help="Specify a log file (default will print to terminal)")
parser.add_argument("-sp", dest="sp", action='store_true', default=False, help="Execute Solution analysis")
parser.add_argument("-rt", dest="rt", action='store_true', default=False, help="Execute Run-Time analysis")
parser.add_argument("-mu", dest="mu", action='store_true', default=False, help="Execute Memory Usage analysis")
parser.add_argument("--use",metavar="NAME",dest="search", nargs=1, default=["bts"],type=str, help="Specify a search to use")

if __name__ == '__main__':
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    
    testfile    = inputs.testfile[0]
    inference   = inputs.infer[0]
    valueorder  = inputs.valueorder[0]
    nodeorder   = inputs.nodeorder[0]
    logfile     = inputs.log[0]
    testnum     = inputs.testnum[0]
    searchop    = inputs.search[0]
    
    ## Not implemented yet
    #RUN_SP  = inputs.sp
    #RUN_RT  = inputs.rt
    #RUN_MU  = inputs.mu
    
    
    puzzleParser = PuzzleParser()
    #f = open('Test/testCrossMath.txt','r')
    f = open('Test/' + testfile + '.txt','r')
    text = f.read()
    f.close()
    for i,puzzle in enumerate(text.split('\n')):
        if testnum > 0 and i != testnum:
            continue
        if "#" in puzzle:
            # Ain't doin that extra shit
            break
        if "crossmath" in testfile.lower():
            csp = puzzleParser.setUpCrossMath(puzzle)
        elif "crypt" in testfile.lower():
            csp = puzzleParser.setUpCrypt(puzzle)
        search = None
        if searchop.lower() in ["bts","backtracking","backtrack","backtrackingsearch"]:
            search = BacktrackingSearch(csp,nodeorder,valueorder,inference)
        elif searchop.lower() in ["ac3","ac-3"]:
            search = AC3()
        start = time()
        search.run(csp)
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