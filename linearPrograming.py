from ortools.linear_solver import pywraplp
from board import Board
import time


class Linear_Programing:
    def __init__(self, inputFileName):
        # get input from file input
        url = "input/" + inputFileName
        # read file input
        file = open(url, "r")
        line = file.readline()
        line.replace("\n", "")
        arr = line.split(" ")
        self.width = int(arr[0])
        self.height = int(arr[1])
        line = file.readline()
        line.replace("\n", "")
        self.k = int(line)
        # get end point
        self.endPoints = []
        for i in range(2 * self.k):
            line = file.readline()
            line.replace("\n", "")
            arr = line.split(" ")
            x = int(arr[0])
            y = int(arr[1])
            k = int(arr[2])
            self.endPoints.append((x, y, k))
        file.close()
        
        # create boad
        self.board = Board(inputFileName)
        # get k values
        self.k_values = []
        for ep in self.endPoints:
            if ep[2] not in self.k_values:
                self.k_values.append(ep[2])
        self.k_values.sort()
        # create main variable list
        self.vars = {}
        # create second variable list
        self.second_vars = {}
        # create solver (MIP solver) 
        self.solver = pywraplp.Solver.CreateSolver("SCIP")

    def toIndex(self, x, y):
        w = self.width
        h = self.height
        if x <= w and y <= h:
            return w * (x - 1) + y
        else:
            print("Index is invalid!")
            return -1

    def toBase(self, p):
        w = self.width
        h = self.height
        if p % w == 0:
            j = w
            i = p // h
        else:
            j = p % w
            i = (p - (p % w)) // h + 1
        return [i, j]

    def getNeighbors(self, x, y):
        w = self.width
        h = self.height
        arr = []
        if x - 1 > 0:
            arr.append((x - 1, y))
        if x + 1 <= h:
            arr.append((x + 1, y))
        if y - 1 > 0:
            arr.append((x, y - 1))
        if y + 1 <= w:
            arr.append((x, y + 1))
        return arr

    def constraints(self):
        w = self.width
        h = self.height
        k = self.k
        k_values = self.k_values
        solver = self.solver
        vars = self.vars
        grid = self.board.grid
        # x(p, k) = 0 or 1
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                for k in k_values:
                    p = self.toIndex(i, j)
                    vars[p, k] = solver.IntVar(0, 1, f"x_{p}_{k}")

        # sum(x(p, k)) = 1
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                p = self.toIndex(i, j)
                constraint = solver.Constraint(1, 1)
                for k in k_values:
                    constraint.SetCoefficient(vars[p, k], 1)

        # sum(sum(x(p, k) * x(q, k))) = 1 or 2
        
        # Version 1:
        # create second variables
        second_vars = self.second_vars
        # for i in range(1, w + 1):
        #     for j in range(1, j + 1):
        #         p = self.toIndex(i, j)
        #         for nb in self.getNeighbors(i, j):
        #             q = self.toIndex(nb[0], nb[1])
        #             if p < q:
        #                 for k in self.k_values:
        #                     x1 = vars[p, k]
        #                     x2 = vars[q, k]
        #                     # y(p, q, k) = 0 or 1
        #                     y = solver.IntVar(0, 1, f"y_{p}_{q}_{k}")
        #                     second_vars[p, q, k] = y
        #                     # y(p, q, k) <= x(p, k)
        #                     constraint_1 = solver.Constraint(-solver.infinity(), 0)
        #                     constraint_1.SetCoefficient(y, 1)
        #                     constraint_1.SetCoefficient(x1, -1)
        #                     # y(p, q, k) <= x(q, k)
        #                     constraint_2 = solver.Constraint(-solver.infinity(), 0)
        #                     constraint_2.SetCoefficient(y, 1)
        #                     constraint_2.SetCoefficient(x2, -1)
        #                     # y(p, q, k) >= x(p, k) + x(q, k) - 1
        #                     constraint_3 = solver.Constraint(-solver.infinity(), 1)
        #                     constraint_3.SetCoefficient(y, -1)
        #                     constraint_3.SetCoefficient(x1, 1)
        #                     constraint_3.SetCoefficient(x2, 1)

        # for i in range(1, w + 1):
        #     for j in range(1, j + 1):
        #         p = self.toIndex(i, j)
        #         constraint_4 = None
        #         if grid[i - 1][j - 1] != "-":
        #             constraint_4 = solver.Constraint(1, 1)
        #         else:
        #             constraint_4 = solver.Constraint(2, 2)
        #         for nb in self.getNeighbors(i, j):
        #             q = self.toIndex(nb[0], nb[1])
        #             for k in self.k_values:
        #                 if p < q:
        #                     y = second_vars[p, q, k]
        #                 else:
        #                     y = second_vars[q, p, k]
        #                 constraint_4.SetCoefficient(y, 1)
        
        
        # Version 2:
        # if x(p, k) is end_point: 
        #     sum(x(q, k)) = 1
        # else: 
        #     Each k: 2 * x(p, k) <= sum(x(q, k)) <= 2 * x(p, k) + M * (1 - x(p, k)) (M is number neghbor of x(p, k))
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                p = self.toIndex(i, j)
                constraint_1 = None
                constraint_2 = None
                list_neighbors = self.getNeighbors(i, j)
                # if x(p, k) is not end_point
                if grid[i - 1][j - 1] == "-":
                    for k in k_values:
                        M = len(list_neighbors)
                        # con_1: sum(x(q, k)) - [2 * x(p, k) + M * (1 - x(p, k))] <= 0
                        # con_2: 2 * x(p, k) - sum(x(q, k)) <= 0
                        constraint_1 = solver.Constraint(-solver.infinity(), M)
                        constraint_2 = solver.Constraint(-solver.infinity(), 0)
                        for nb in list_neighbors:
                            q = self.toIndex(nb[0], nb[1])
                            constraint_1.SetCoefficient(vars[q, k], 1)
                            constraint_2.SetCoefficient(vars[q, k], -1)
                        constraint_1.SetCoefficient(vars[p, k], M - 2)
                        constraint_2.SetCoefficient(vars[p, k], 2)
                # x(p, k) is end_point
                else:
                    k = int(grid[i - 1][j - 1])
                    # con_1: sum(x(q, k)) = 1
                    constraint_1 = solver.Constraint(1, 1)
                    for nb in list_neighbors:
                        q = self.toIndex(nb[0], nb[1])
                        constraint_1.SetCoefficient(vars[q, k], 1)
        # Version 3: Cp_SAT solver
        

        self.vars = vars
        self.second_vars = second_vars
        self.solver = solver

    def input(self):
        solver = self.solver
        vars = self.vars
        # x(p, k) = 1 if p is end point
        for ep in self.endPoints:
            x = ep[0]
            y = ep[1]
            k = ep[2]
            p = self.toIndex(x, y)
            constraint = solver.Constraint(1, 1)
            constraint.SetCoefficient(vars[p, k], 1)

        self.solver = solver
        self.vars = vars

    def solve(self):
        w = self.width
        h = self.height
        solver = self.solver

        t1 = time.time()
        # print("Time before solve: ",solver.WallTime())
        status = solver.Solve()
        # print("Time after solve: ",solver.WallTime())
        t2 = time.time()

        print("Solving time: ", (t2 - t1) * 1000, "ms.")
        grid = self.board.grid
        if status == pywraplp.Solver.OPTIMAL:
            # print("Solution:")
            # print("Objective value =", solver.Objective().Value())
            count = 0
            for v in solver.variables():
                if count >= w * h:
                    break
                if int(v.solution_value()) != 0:
                    # print(v.name(), ": ", v.solution_value())
                    count += 1
                    name = v.name()
                    data = name.split("_")
                    p = int(data[1])
                    k = int(data[2])
                    # print(data)
                    pos = self.toBase(p)
                    # replace number in cell
                    x = pos[0]
                    y = pos[1]
                    grid[x - 1][y - 1] = str(k)
            self.board.grid = grid
            # print(self.board.grid)
            self.board.writeOutputFile()
            self.board.show()

        else:
            print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    lp = Linear_Programing("3")
    lp.constraints()
    lp.input()
    print("Number of variables = ", lp.solver.NumVariables())
    print("Number of constraints = ", lp.solver.NumConstraints())
    lp.solve()
