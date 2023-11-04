from pg import NumberlinkUI


class Board:
    def __init__(self, fileName):
        self.inputFile = fileName
        url = "input/" + fileName
        file = open(url, "r")

        line = file.readline()
        line.replace("\n", "")
        arr = line.split(" ")
        self.width = int(arr[0])
        self.height = int(arr[1])

        line = file.readline()
        line.replace("\n", "")
        self.k = int(line)

        self.endPoints = []
        grid = []
        for i in range(1, self.height + 1):
            s = []
            for j in range(1, self.width + 1):
                s.append("-")
            grid.append(s)
        for i in range(2 * self.k):
            line = file.readline()
            line.replace("\n", "")
            arr = line.split(" ")
            x = int(arr[0])
            y = int(arr[1])
            k = int(arr[2])

            self.endPoints.append((x, y, k))
            # replace number in cell
            grid[x - 1][y - 1] = str(k)
        self.grid = grid
        # self.endPoints.sort(key=lambda x: x[2])

        self.k_values = []
        for ep in self.endPoints:
            if ep[2] not in self.k_values:
                self.k_values.append(ep[2])
        self.k_values.sort()
        file.close()
        self.ui = None

        # self.ui = NumberlinkUI(
        #     self.width, self.height, self.k, self.endPoints, self.k_values, fileName
        # )

    def writeOutputFile(self):
        outputFileName = "output/" + self.inputFile
        file = open(outputFileName, "w")
        grid = self.grid
        # print(grid)
        w = self.width
        h = self.height
        for i in range(h):
            for j in range(w):
                file.write(grid[i][j] + " ")
            file.write("\n")
        file.close()

    def show(self):
        # arr = self.grid
        # for i in range(0, len(arr)):
        #     print(arr[i])
        self.ui = NumberlinkUI(
            self.width,
            self.height,
            self.k,
            self.endPoints,
            self.k_values,
            self.inputFile,
        )
        self.ui.render()


if __name__ == "__main__":
    board = Board("3")
    board.show()
