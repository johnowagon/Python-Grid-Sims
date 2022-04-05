from tkinter import *
import time

class Cell():
    FILLED_COLOR_BG = "#EEC4ED"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "#EEC4ED"
    BLOCKED_COLOR_BG = "brown"
    BLOCKED_COLOR_BORDER = "brown"
    END_COLOR_BG = "blue"
    END_COLOR_BORDER = "blue"
    PATH_COLOR_BG = "magenta"
    PATH_COLOR_BORDER = "magenta"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill

    def draw(self, start=False, end=False, path=False, conway=False):#this is possibly the worst coded thing here. 
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            if(start):
                fill = Cell.FILLED_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
            elif(end):
                fill = Cell.END_COLOR_BG
                outline = Cell.END_COLOR_BORDER
            elif(path):
                fill = Cell.PATH_COLOR_BG
                outline = Cell.PATH_COLOR_BORDER
            elif(conway):
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BG
            else:
                fill = Cell.BLOCKED_COLOR_BG
                outline = Cell.BLOCKED_COLOR_BORDER
            

            if not self.fill and conway:
                fill = Cell.EMPTY_COLOR_BORDER
                outline = Cell.EMPTY_COLOR_BG
            elif not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

    def highlightCell(self):
        if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size
        self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = "#93E9BE", outline = "black")



class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.blocked = []
        
        self.columnNumber = columnNumber
        self.rowNumber = rowNumber

        self.cellSize = cellSize

        self.start = ()#coords for start location
        self.end = ()#coords for end location (for search algos)

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #array for keeping track of conways alive cells.
        self.alive = []

        #keep list of visited nodes for search algos.
        self.visited = [[0]*self.columnNumber for i in range(self.rowNumber)]

        self.prev = []#hoping this works for scope problems. temporary solution
        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.

        self.bind("<Shift-Button-1>", self.handleStart)
        #gives start location
        self.bind("<Command-Button-1>", self.handleEnd)

        #master.bind("c", lambda event: self.gridClear)#clear screen

        #self.bind("b", self.BFS)#perform breadth first search
        #self.bind("d", self.DFS)#perform depth first search

        master.bind("<Shift-Tab>", self.visitedClear)#clear visited but leave blocked,start,end.

        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)
        self.blocked.append((row,column))

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)
            self.blocked.append((row,column))

    def handleStart(self,event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        
        if(self.start):
            prevCell = self.grid[self.start[0]][self.start[1]]#delete previous starting node
            prevCell._switch()
            prevCell.draw()
        
        self.start = (row,column)
        cell._switch()
        cell.draw(start=True)
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

    #def chinkDestroyer(self, event):


    def handleEnd(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        
        if(self.end):
            prevCell = self.grid[self.end[0]][self.end[1]]#delete previous starting node
            prevCell._switch()
            prevCell.draw()
        
        self.end = (row,column)
        cell._switch()
        cell.draw(end=True)
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)
        #print(self.blocked.count((0,0)))
    
    def gridClear(self):
        for i in range(self.rowNumber):#literally dont know how to do this more efficicently. 
            #maybe keep track of (r,c) for visited to improve compute for this function.
            for j in range(self.columnNumber):
                if self.visited[i][j] == True:
                    curCell = self.grid[i][j]
                    curCell._switch()
                    curCell.draw()

        for cell in self.blocked:
            curCell = self.grid[cell[0]][cell[1]]
            curCell._switch()
            curCell.draw()
        self.update()
        self.blocked.clear()
        self.start = ()
        self.end = ()
        self.visited = [[0]*self.columnNumber for i in range(self.rowNumber)] #not ideal??

    def visitedClear(self,event):
        for i in range(self.rowNumber):#literally dont know how to do this more efficicently. 
            #maybe keep track of (r,c) for visited to improve compute for this function.
            for j in range(self.columnNumber):
                if self.visited[i][j] == True:
                    curCell = self.grid[i][j]
                    curCell._switch()
                    curCell.draw()
        start = self.grid[self.start[0]][self.start[1]]
        end = self.grid[self.end[0]][self.end[1]]
        if(not start.fill and not end.fill):
            start._switch()
            start.draw(start=True)
            end._switch()
            end.draw(end=True)

        self.update()
        self.visited = [[0]*self.columnNumber for i in range(self.rowNumber)] #not ideal??