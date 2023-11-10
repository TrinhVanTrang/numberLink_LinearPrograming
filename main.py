from linearPrograming import Linear_Programing
from cp_sat import CP_SAT
import os
import numpy as np

def mean(s):
    return np.nanmean(s)

def std(s):
    return np.nanstd(s)

if __name__=="__main__":
    
    round=100
    url="./input/"
    inputArr=os.listdir(url)
    timeArr={}
    # print("Linear programing:")
    # for f in inputArr:
    #     inputFile=url+f
    #     print("file: ",inputFile)
    #     lp=Linear_Programing(f)
    #     lp.constraints()
    #     lp.input()
    #     print("Number of variables = ", lp.solver.NumVariables())
    #     print("Number of constraints = ", lp.solver.NumConstraints())
    #     lp.solve()
    #     print("Solving time: ",lp.getSolvingTime()," ms.")
    print("CP-SAT:")
    for r in range(round):
        for f in inputArr:
            inputFile=url+f
            # print("file: ",inputFile)
            cs=CP_SAT(f)
            cs.constraints()
            cs.input()
            # print("Number of variables = ", cs.model.NumVariables())
            # print("Number of constraints = ", cs.model.NumConstraints())
            cs.solve()
            if cs.getSolvingTime=="TIME OUT":
                time=np.nan
            else:
                time=float(cs.getSolvingTime())
            timeArr[r,f]=time
        print("Round ",r," finish!")
    
    for f in inputArr:
        time=[timeArr[r,f] for r in range(round)]
        # print(time)
        print("FIle ",f," solving time (mean): ",mean(time),"ms with deviation: ",std(time),".")
        