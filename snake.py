from grid import CellGrid
from tkinter import *
from random import *
import time

class Snake(CellGrid):
    def __init__(self, master, columnNumber, rowNumber, cellSize, *args, **kwargs):
        super().__init__(master, columnNumber, rowNumber, cellSize, *args, **kwargs)
        self.columnNumber = columnNumber
        self.rowNumber = rowNumber
        self.snake = [(10,10)]#values of the snake, starts with the starting value
        self.fruit = ()
        self.dir = (0,0) #direction for snake movement. up, down, left right. 
        #starts as zero.
        master.bind("<Left>", self.handleArrows)
        master.bind("<Up>", self.handleArrows)
        master.bind("<Down>", self.handleArrows)
        master.bind("<Right>", self.handleArrows)
        master.bind("s", lambda function : self.go())

    def makeFruit(self):#make a fruit.
        self.fruit = (randint(0,self.rowNumber-1), randint(0,self.columnNumber-1))#where the fruit is to grow snake. 
        fruitCell = self.grid[self.fruit[0]][self.fruit[1]]
        fruitCell._switch()
        fruitCell.draw(path=True)
        self.update()
    
    def updateSnake(self):
        if(not self.fruit):
            self.makeFruit()
            print(self.fruit)
        startCell = self.grid[self.snake[0][0]][self.snake[0][1]]
        if(startCell.fill == False):
            startCell._switch()
            startCell.draw()#draw starting point
        nextSnake = []#for updating snake. stupid immutable tuples
        if(self.dir != (0,0)):
            for i in self.snake:#Draw each segment of snake, update each value of the snake in that order.
                print(i)
                tupx = i[0] + self.dir[0]
                tupy = i[1] + self.dir[1]
                nextSnake.append((tupx, tupy))
                
                curCell = self.grid[i[0]][i[1]]#uglier? maybe. 
                curCell._switch()
                curCell.draw()
                nexCell = self.grid[tupx][tupy]#uglier? maybe. 
                if((tupx,tupy) == self.fruit):
                    end = self.snake[len(self.snake)-1]
                    newx = end[0] + self.dir[0]
                    newy = end[1] + self.dir[1]
                    nextSnake.append((newx,newy))
                    self.makeFruit()
                    #self.snake.append((tupx,tupy))
                nexCell._switch()
                nexCell.draw()
                self.update()
            self.snake = nextSnake
            print(self.snake)

    def go(self):
        self.updateSnake()
        self.after(100, self.go)

    def handleArrows(self,event):
        key = event.keysym
        if(key == 'Left'):
            self.dir = (0,-1)
        elif(key == 'Right'):
            self.dir = (0,1)
        elif(key == 'Down'):
            self.dir = (1,0)
        elif(key == 'Up'):
            self.dir = (-1,0)
