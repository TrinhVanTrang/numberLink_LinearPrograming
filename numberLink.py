
from ortools.linear_solver import pywraplp
from board import Board

class NumberLink:
    def __init__(self,inputFileName):
        file = open(inputFileName, "r")
        
        line = file.readline()
        line.replace('\n', '')
        arr = line.split(' ')
        self.width = int(arr[0])
        self.height = int(arr[1])
        
        line=file.readline()
        line.replace('\n', '')
        self.k=int(line)
        
        self.endPoints=[]
        for i in range(self.k):
            line=file.readline()
            line.replace('\n', '')
            arr = line.split(' ')
            x=int(arr[0])
            y=int(arr[1])
            k=int(arr[2])
            self.endPoints.append((x,y,k))
        file.close()
        
        self.board=Board(inputFileName)
        
    
