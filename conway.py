from grid import CellGrid
from tkinter import *
import time

class Conway(CellGrid):
    def __init__(self, master, columnNumber, rowNumber, cellSize, *args, **kwargs):
        super().__init__(master, columnNumber, rowNumber, cellSize, *args, **kwargs)
        self.columnNumber = columnNumber
        self.rowNumber = rowNumber
        self.master = master
        self.blocked = []
        self.paused = False
        self.nextIter = [[0]*self.columnNumber for i in range(self.rowNumber)]#keeps track of the next iteration
        #of the game. 
        master.bind("r", self.run)
        master.bind("c", lambda event: self.gridClear())#clear screen
        master.bind("<space>", self.pause)

    def explore(self, r, c):
        dr = [-1, 1, 0, 0, -1, -1, 1, 1]
        dc = [0, 0, 1, -1, -1, 1, 1, -1]
        state = self.grid[r][c].fill
        aliveNeighbors = []#how we keep track of which cell is alive and which is dead.
        #RULES:
        #Cell with fewer than 2 live neighbors die.
        #Cells with 2 or 3 neighbors live.
        #Cells with more than 3 neighbors die
        #Dead cells with 3 live neighbors becomes alive.

        for i in range(8):
            rr = r + dr[i]
            cc = c + dc[i]

            if rr < 0 or cc < 0: continue#points where index is out of bounds.
            if rr >= self.rowNumber or cc >= self.columnNumber: continue

            curCell = self.grid[rr][cc]
            if curCell.fill:
                aliveNeighbors.append((rr,cc))
        
        fate = len(aliveNeighbors)
        #game logic
        if state == False and fate == 3:
            self.nextIter[r][c] = 1
        elif fate < 2 and state == True:
            self.nextIter[r][c] = 0
        elif (fate == 2 or fate == 3) and state == True:
            self.nextIter[r][c] = 1
        elif fate > 3 and state == True:
            self.nextIter[r][c] = 0

    def updateIter(self, nextIter):
        self.gridClear()
        for i in range(self.columnNumber):
            for j in range(self.rowNumber):
                curCell = self.grid[j][i]
                if(self.nextIter[j][i] == 1):
                    if(curCell.fill == False):
                        curCell._switch()
                        curCell.draw()
                elif(self.nextIter[j][i] == 0):
                    if(curCell.fill == True):
                        curCell._switch()
                        curCell.draw()
        self.nextIter = [[0]*self.columnNumber for i in range(self.rowNumber)]#is there a better way to clear a 2d array?
    
    def pause(self, event):
        self.paused = not self.paused
    
    def run(self,event):
        while(self.paused == False):
            for i in range(self.columnNumber):#is it really the best option to go through every cell?
                for j in range(self.rowNumber):
                    #print(self.grid[i][j].abs, self.grid[i][j].ord)
                    self.explore(self.grid[j][i].abs, self.grid[j][i].ord)
            #print(self.nextIter)
            self.updateIter(self.nextIter)
            time.sleep(0.1)