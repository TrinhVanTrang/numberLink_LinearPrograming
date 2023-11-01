from linearPrograming import Linear_Programing

lp = Linear_Programing("4")
lp.constraints()
lp.input()
print("Number of variables = ", lp.solver.NumVariables())
print("Number of constraints = ", lp.solver.NumConstraints())
lp.solve()