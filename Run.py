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
parser.add_argument("-f",   metavar="FILE", dest="testfile",  nargs=1, default=["testCrossMath.txt"], type=str,help="Specify a test file")
parser.add_argument("--inf",metavar="NAME", dest="infer",     nargs=1, default=["fc"],    type=str, help="specify a inference to use (fc, mac)")
parser.add_argument("--vo", metavar="NAME", dest="valueorder",nargs=1, default=["none"],  type=str, help="specify a volue order to use (randomorder, LCV, none)")
parser.add_argument("--no", metavar="NAME", dest="nodeorder", nargs=1, default=["degree"],type=str, help="specify a node order to use (randomorder,mrv,degree,none)")
parser.add_argument("--test",metavar="INT", dest="testnum",   nargs=1, default=[-1], type=int,help="specify a test number to be ran")
parser.add_argument("--log",metavar="FILE", dest="log",       nargs=1, default=[""], type=str,help="Specify a log file (Not functional yet)")
parser.add_argument("-sp", dest="sp", action='store_true', default=False, help="Execute Solution analysis (TBA for data collection)")
parser.add_argument("-rt", dest="rt", action='store_true', default=False, help="Execute Run-Time analysis (TBA for data collection)")
parser.add_argument("-mu", dest="mu", action='store_true', default=False, help="Execute Memory Usage analysis (TBA for data collection)")
parser.add_argument("--use",metavar="NAME",dest="search", nargs=1, default=["bts"],type=str, help="Specify a search to use (ac3, bts)")
parser.add_argument("--no-gac", dest="gac", action='store_false', default=True, help="Disable Generalized Arc Consistency")


if __name__ == '__main__':
    inputs = Inputs()
    parser.parse_args(sys.argv[1:], namespace=inputs)
    
    testfile    = inputs.testfile[0]
    inference   = inputs.infer[0]
    valueorder  = inputs.valueorder[0]
    nodeorder   = inputs.nodeorder[0]
    logfile     = inputs.log[0]
    testnum     = inputs.testnum[0] - 1
    searchop    = inputs.search[0]
    gac         = inputs.gac
    ## These will be implemented 
    ## when it comes to metrics
    #RUN_SP  = inputs.sp
    #RUN_RT  = inputs.rt
    #RUN_MU  = inputs.mu
    
    
    puzzleParser = PuzzleParser()
    f = open(testfile,'r')
    text = f.read()
    f.close()
    for i,puzzle in enumerate(text.split('\n')):
        if testnum > 0 and i != testnum:
            continue
        if "#" in puzzle:
            # Ain't doin that extra stuff
            break
        if "crossmath" in testfile.lower():
            csp = puzzleParser.setUpCrossMath(puzzle)
        elif "crypt" in testfile.lower():
            csp = puzzleParser.setUpCrypt(puzzle)
        search = None
        if searchop.lower() in ["bts","backtracking","backtrack","backtrackingsearch"]:
            search = BacktrackingSearch(csp,nodeorder,valueorder,inference,GACEnabled=gac)
        elif searchop.lower() in ["ac3","ac-3"]:
            search = AC3(gac)
            
        search.run(csp)