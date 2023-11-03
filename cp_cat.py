from ortools.sat.python import cp_model
from board import Board
import time


class CP_SAT:
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
        # create variable list
        self.vars = {}
        # create CP model
        self.model = cp_model.CpModel()
        # create CP solver
        # solver = cp_model.CpSolver()

    # def exactlyKConditions(self, xp, nbOfP, k):
    #     model = self.model
    #     vars = self.vars
    #     w = self.width
    #     h = self.height
    #     k_values = self.k_values
    #     if k == 1:
    #         model.AddBoolOr(xp == xq for xq in nbOfP)
    #     elif k == 2:
    #         for i in range(0, len(nbOfP) - 1):
    #             for j in range(i + 1, len(nbOfP)):
    #                 print()

    #     self.model = model
    #     return

    def constraints(self):
        #  bien phap nghiep vu ^~^
        w = self.width
        h = self.height
        k = self.k
        # k_values = self.k_values
        model = self.model
        vars = self.vars
        grid = self.board.grid

        # create vars
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                p = self.toIndex(i, j)
                var = model.NewIntVar(1, k, f"x_{p}")
                vars[p] = var
        # sum(1 | xp == xq) = 1 (p is end_point) or 2 (otherwise)
        #  q : q | Neightbor(p,q)
        second_vars = {}
        for i in range(1, w + 1):
            for j in range(1, h + 1):
                p = self.toIndex(i, j)
                # condition: xp == xq
                sum_val = []
                for nb in self.getNeighbors(i, j):
                    q = self.toIndex(nb[0], nb[1])
                    second_vars[p, q] = model.NewBoolVar(f"val_{p}_{q}")
                    model.Add((vars[p] == vars[q])).OnlyEnforceIf(second_vars[p, q])
                    model.Add((vars[p] != vars[q])).OnlyEnforceIf(second_vars[p, q].Not())
                    sum_val.append(second_vars[p, q])
                if grid[i - 1][j - 1] == "-":
                    model.Add(sum(sum_val) == 2)
                else:
                    model.Add(sum(sum_val) == 1)

        self.vars = vars
        self.model = model

        return

    def input(self):
        endPoints = self.endPoints
        vars = self.vars
        model = self.model
        k_values = self.k_values
        # x(p) = k if p is end point
        for ep in endPoints:
            x = ep[0]
            y = ep[1]
            k = ep[2]
            model.Add(vars[self.toIndex(x, y)] == k_values.index(k) + 1)

        self.model = model
        self.vars = vars

        return

    def solve(self):
        w = self.width
        h = self.height
        model = self.model
        vars = self.vars
        k_values = self.k_values
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        t1 = time.time()
        # print("Time before solve: ",solver.WallTime())
        status = solver.Solve(model)
        # print("Time after solve: ",solver.WallTime())
        t2 = time.time()

        print("Solving time: ", (t2 - t1) * 1000, "ms.")
        grid = self.board.grid
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # for i in range(w*h):

            for i in range(1, w + 1):
                for j in range(1, h + 1):
                    p = self.toIndex(i, j)
                    k = solver.Value(vars[p])
                    grid[i - 1][j - 1] = str(k_values[k - 1])
            self.board.grid = grid
            self.board.writeOutputFile()
            self.board.show()

        else:
            print("The problem does not have an optimal solution.")
        return

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


if __name__ == "__main__":
    cp_sat = CP_SAT("5")
    cp_sat.constraints()
    cp_sat.input()
    # print(cp_sat.model.ModelStats())
    cp_sat.solve()
