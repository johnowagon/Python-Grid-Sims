from grid import CellGrid
from tkinter import *
import time
class Algos(CellGrid):
    def __init__(self, master, columnNumber, rowNumber, cellSize, *args, **kwargs):
        super().__init__(master, columnNumber, rowNumber, cellSize, *args, **kwargs)
        self.columnNumber = columnNumber
        self.rowNumber = rowNumber
        self.master = master
 
        self.cellSize = cellSize
        self.blocked = []
        master.bind("b", self.BFS)#perform breadth first search
        master.bind("d", self.DFS)#perform depth first search
        
    
    def reconstruct(self,s,e,prev):
            path = []
            at = e
            path.append(e)
            while(at):
                path.append(prev[at])
                at = prev[at]

            path.reverse()

            if path[1] == self.start:
                for i in range(1, len(path)):
                    curCell = self.grid[path[i][0]][path[i][1]]
                    if(path[i] == self.end):
                        curCell._switch()
                    curCell.draw(path=True)
                    self.update()
            return path
            
    def explore_neighbors(self, r, c, DSrow, DScol, prev):#I want to reuse this for conways. For now, the functions are separate.
        #function that takes row, col, data structure (q for bfs, stack for dfs)
        #and explores neighbors.
        #these arrays represent each cardinal direction that the search can go. 
        #direction at i index is r + dr[i],c + dc[i]
        dr = [-1, 1, 0, 0, -1, -1, 1, 1]
        dc = [0, 0, 1, -1, -1, 1, 1, -1]
        fakeNodeInNextLayer = 0
        for i in range(8):
            rr = r + dr[i]
            cc = c + dc[i]

            if rr < 0 or cc < 0: continue#points where index is out of bounds OR a block is found.
            if rr >= self.rowNumber or cc >= self.columnNumber: continue
            if self.visited[rr][cc] == True: continue
            if self.blocked.count((rr,cc)) > 0: continue
            
            curCell = self.grid[rr][cc]
            curCell._switch()
            curCell.highlightCell()
            self.update()

            DSrow.append(rr)
            DScol.append(cc)
            self.visited[rr][cc] = True
            prev[(rr,cc)] = (r,c)
            fakeNodeInNextLayer += 1
        return fakeNodeInNextLayer

    def BFS(self, event):
        if(not self.start or not self.end):
            return print("Not a valid input.")
        startRow = self.start[0]
        startCol = self.start[1]

        queueRow = [] #BFS queue, where we take neighbors out of.
        queueCol = []
        prev = {self.start : None}#dictionary to reconstruct path.
        reached_end = False

        queueRow.append(self.start[0])
        queueCol.append(self.start[1])
        self.visited[self.start[0]][self.start[1]] = True

        nodenext = 0#variables for move counting. 
        nodeleft = 1
        mc = 0
        while len(queueRow) > 0:
            r = queueRow.pop(0)
            c = queueCol.pop(0)
            if (r,c) == self.end:
                reached_end = True
                break
            nodenext += self.explore_neighbors(r, c, queueRow, queueCol, prev)
            nodeleft -= 1
            if nodeleft == 0:
                nodeleft = nodenext
                nodenext = 0
                mc += 1
        if reached_end:
            print(f"Finished BFS in {mc} moves.")
            self.reconstruct(self.start, self.end, prev)
            return mc
        return -1

    def DFS(self, event):#DOES NOT NECESSARILY RETURN SHORTEST PATH!
        #strange behavior coming from DFS. Debugging soon
        if(not self.start or not self.end):
            return print("Not a valid input.")
        startRow = self.start[0]
        startCol = self.start[1]

        stackRow = [] #DFS stack, where we take neighbors out of.
        stackCol = []
        dprev = {self.start : None}#dictionary to reconstruct path.
        reached_end = False

        stackRow.append(self.start[0])
        stackCol.append(self.start[1])
        self.visited[self.start[0]][self.start[1]] = True
        nodenext = 0#variables for move counting. 
        nodeleft = 1
        mc = 0
        while len(stackRow) > 0:
            r = stackRow.pop()
            c = stackCol.pop()
            if (r,c) == self.end:
                reached_end = True
                break
            nodenext += self.explore_neighbors(r, c, stackRow, stackCol, dprev)
            nodeleft -= 1
            if nodeleft == 0:
                nodeleft = nodenext
                nodenext = 0
                mc += 1
        if reached_end:
            print(f"Finished DFS in {mc} moves.")
            #print(dprev)
            self.reconstruct(self.start, self.end, dprev)
            return mc
        return -1

        
       
