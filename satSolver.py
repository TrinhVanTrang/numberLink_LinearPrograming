from pysat.formula import CNF
from pysat.solvers import Solver
import math
import time
from board import Board


class SATSolver:
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
        self.second_vars = {}
        # create SAT solver
        self.solver = None
        self.cnf = ""
        self.num_vars = 0
        self.num_clauses = 0
        # solving time
        self.solvingTime = ""

    def getSolvingTime(self):
        
        return self.solvingTime

    def constraints(self):
        w = self.width
        h = self.height
        grid = self.board.grid
        Xs = self.vars
        Ys = self.second_vars
        K = self.k
        k_values = self.k_values
        cnf = self.cnf
        num_vars = self.num_vars
        num_clauses = self.num_clauses

        # create vars
        for i in range(1, h + 1):
            for j in range(1, w + 1):
                p = self.toIndex(i, j)
                for k in range(1, K + 1):
                    Xs[p, k] = f"{self.toVarNumber(self.toIndex(i,j),k)}"  # x(p, k)
                    num_vars += 1

        for i in range(1, h + 1):
            for j in range(1, w + 1):
                p = self.toIndex(i, j)
                nbs = self.getNeighbors(i, j)
                for nb in nbs:
                    noVar = num_vars + 1
                    q = self.toIndex(nb[0], nb[1])
                    # if p < q:
                    if p < q:
                        Ys[p, q] = f"{noVar}"  # y(p, q)
                        num_vars += 1

        # Each cell p exactly one value k - EO(x(p, k))
        amo = ""  # cnf for at most one
        alo = ""  # cnf for at least one
        for i in range(1, h + 1):
            for j in range(1, w + 1):
                p = self.toIndex(i, j)
                for k in range(1, K + 1):
                    alo += Xs[p, k] + " "
                    for l in range(k + 1, K + 1):
                        amo += "-" + Xs[p, k] + " -" + Xs[p, l] + " 0\n"
                        num_clauses += 1
                alo += "0\n"
                num_clauses += 1
        cnf += amo
        cnf += alo

        for i in range(1, h + 1):
            for j in range(1, w + 1):
                p = self.toIndex(i, j)
                nbs = self.getNeighbors(i, j)
                for k in range(1, K + 1):
                    for nb in nbs:
                        q = self.toIndex(nb[0], nb[1])
                        # if p < q:
                        # y(p, q) && x(p, k) => x(q, k)
                        if p < q:
                            cnf += (
                                "-"
                                # + (Ys[p, q] if p < q else Ys[q, p])
                                + Ys[p, q]
                                + " -"
                                + Xs[p, k]
                                + " "
                                + Xs[q, k]
                                + " 0\n"
                            )
                            num_clauses += 1
                            # x(p, k) && x(p, k) => y(p, q)
                            cnf += (
                                "-"
                                + Xs[p, k]
                                + " -"
                                + Xs[q, k]
                                + " "
                                # + (Ys[p, q] if p < q else Ys[q, p])
                                + Ys[p, q]
                                + " 0\n"
                            )
                            num_clauses += 1
                        # # y(p, q) = y(q, p):
                        # cnf += Ys[p, q] + " -" + Ys[q, p] + " 0\n"
                        # num_clauses += 1
                        # cnf += "-" + Ys[p, q] + " " + Ys[q, p] + " 0\n"
                        # num_clauses += 1

        # if x(p, k) = True
        # => if p is end_point:
        #       => exactly one Neightbors(p): y(p, q) = True
        #    else:
        #       => exactly two Neightbors(p): y(p, q) = True
        for i in range(1, h + 1):
            for j in range(1, w + 1):
                p = self.toIndex(i, j)
                nbs = self.getNeighbors(i, j)
                is_end_point = grid[i - 1][j - 1] != "-"
                if is_end_point:
                    k = k_values.index(int(grid[i - 1][j - 1])) + 1
                    # cnf:  ExactlyOne(q in Neighbors(p): x(q, k))
                    alo = ""
                    amo = ""
                    for x in range(0, len(nbs)):
                        q1 = self.toIndex(nbs[x][0], nbs[x][1])
                        alo += (Ys[p, q1] if p < q1 else Ys[q1, p]) + " "
                        for y in range(x + 1, len(nbs)):
                            q2 = self.toIndex(nbs[y][0], nbs[y][1])
                            amo += (
                                "-"
                                + (Ys[p, q1] if p < q1 else Ys[q1, p])
                                + " -"
                                + (Ys[p, q2] if p < q2 else Ys[q2, p])
                                + " 0\n"
                            )
                            num_clauses += 1
                    alo += "0\n"
                    num_clauses += 1
                    cnf += alo
                    cnf += amo

                else:
                    # cnf:  ExactlyTwo(q in Neighbors(p): y(p, q))
                    alo = ""
                    amo = ""
                    # AMT(y(p, q))
                    for x in range(0, len(nbs)):
                        q1 = self.toIndex(nbs[x][0], nbs[x][1])
                        # alo += Ys[p, q1] + " "
                        for y in range(x + 1, len(nbs)):
                            q2 = self.toIndex(nbs[y][0], nbs[y][1])
                            for z in range(y + 1, len(nbs)):
                                q3 = self.toIndex(nbs[z][0], nbs[z][1])
                                amo += (
                                    "-"
                                    + (Ys[p, q1] if p < q1 else Ys[q1, p])
                                    + " -"
                                    + (Ys[p, q2] if p < q2 else Ys[q2, p])
                                    + " -"
                                    + (Ys[p, q3] if p < q3 else Ys[q3, p])
                                    + " 0\n"
                                )
                                num_clauses += 1
                    # ALT(y(p, q))
                    for x in range(0, len(nbs)):
                        # q1 = self.toIndex(nbs[x][0], nbs[x][1])
                        for y in range(0, len(nbs)):
                            q2 = self.toIndex(nbs[y][0], nbs[y][1])
                            if x != y:
                                alo += (Ys[p, q2] if p < q2 else Ys[q2, p]) + " "
                        alo += "0\n"
                        num_clauses += 1
                    cnf += alo
                    cnf += amo

        self.cnf = cnf
        self.num_vars = num_vars
        self.num_clauses = num_clauses
        self.vars = Xs
        self.second_vars = Ys
        return

    def input(self):
        Xs = self.vars
        endPoints = self.endPoints
        k_values = self.k_values
        cnf = self.cnf
        # x(p, k) = true if p is end point
        for ep in endPoints:
            x = ep[0]
            y = ep[1]
            k = ep[2]
            p = self.toIndex(x, y)
            cnf += Xs[p, k_values.index(k) + 1] + " 0\n"

        self.cnf = cnf

        return

    def solve(self):
        w = self.width
        h = self.height
        N = self.k
        k_values = self.k_values
        num_vars = self.num_vars
        num_clauses = self.num_clauses
        grid = self.board.grid
        cnf_clauses = (
            "p cnf " + str(num_vars) + " " + str(num_clauses) + "\n" + self.cnf
        )
        solver = self.solver
        cnf = CNF()

        cnf.from_string(cnf_clauses)
        solver = Solver(
            name="m22", bootstrap_with=cnf, use_timer=True, warm_start=False
        )

        solve_status = solver.solve()
        t1 = time.time()
        self.solver = solver
        t2 = time.time()
        solvingTime = solver.time() * 1000
        # solvingTime = (t2 - t1) * 1000
        print("Solving time: ", round(solvingTime, 6), " ms.")
        if solve_status:
            # print("Solve: true")
            result_vars = solver.get_model()
            self.solvingTime = str(solvingTime)
            for var in result_vars:
                if var > 0 and var <= w * h * N:
                    x_i_j_k = self.toI_J_K(var)
                    i = x_i_j_k[0]
                    j = x_i_j_k[1]
                    k = x_i_j_k[2]
                    # print("Cell (", i,", ",j,"): ",k_values[k-1])
                    grid[i - 1][j - 1] = str(k_values[k - 1])
            self.board.grid = grid
            self.board.writeOutputFile()
            # self.board.show()
        else:
            print("Solve: False.")
        solver.delete()
        return

    def writeCNFFile(self):
        cnf_file_name = "cnf.txt"
        cnf = self.cnf
        num_vars = self.num_vars
        num_clauses = self.num_clauses
        file = open(cnf_file_name, "w")
        s = "p cnf " + str(num_vars) + " " + str(num_clauses) + "\n" + cnf
        file.write(s)
        file.close()
        return

    def toIndex(self, x, y):
        w = self.width
        h = self.height
        if x <= h and y <= w:
            return w * (x - 1) + y
        else:
            print("Index is invalid!")
            return -1

    def toBase(self, p):
        w = self.width
        h = self.height
        if p % w == 0:
            j = w
            i = p // w
        else:
            j = p % w
            i = (p - (p % w)) // w + 1
        return [i, j]

    def toVarNumber(self, p, k):
        n = self.k
        if k <= n:
            noVar = (p - 1) * n + k
            return noVar
        else:
            print("K value unvaliable!")
            return -1

    def toI_J_K(self, noVar):
        w = self.width
        h = self.height
        n = self.k
        p = 0
        k = 0
        if noVar % n == 0:
            k = n
            p = noVar // n
        else:
            k = noVar % n
            p = (noVar - (noVar % n)) // n + 1
        pos = self.toBase(p)
        i = pos[0]
        j = pos[1]
        return (i, j, k)

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
    satSolver = SATSolver("110")
    satSolver.constraints()
    satSolver.input()
    satSolver.writeCNFFile()
    satSolver.solve()
