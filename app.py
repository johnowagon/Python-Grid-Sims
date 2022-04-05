#from grid import CellGrid
from algos import Algos
from conway import Conway
from snake import Snake
from tkinter import *

if __name__ == "__main__" :
    app = Tk()
    

    grid = Conway(app, 25, 25, 40)#What to change for differnt modes!
    #Change Conway to Algos is you want pathfinding.

    grid.pack()


    app.mainloop()
    
