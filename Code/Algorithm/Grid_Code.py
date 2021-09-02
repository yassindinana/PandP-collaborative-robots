from tkinter import *
import numpy as np
from tkinter import Button
import matplotlib.pyplot as plt

class Cell():
    FILLED_COLOR_BG = "black"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"

    FILLED_COLOR_BG_obstacle = "red"
    FILLED_COLOR_BORDER_obstacle = "red"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def draw(self,color =""):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            if color =="":
                fill = Cell.FILLED_COLOR_BG
                outline = Cell.FILLED_COLOR_BORDER
            else:
                fill = color
                outline = color

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

    def draw_obstacle(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.FILLED_COLOR_BG_obstacle
            outline = Cell.FILLED_COLOR_BORDER_obstacle

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)


class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        self.width = columnNumber
        self.height = rowNumber
        # https://stackoverflow.com/questions/568962/how-do-i-create-an-empty-array-matrix-in-numpy
        self.array = np.zeros(shape=(self.height,self.width))
        self.count = 1
        self.start = (0,0)
        self.end   = (0,0)
        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        self.button = Button(master, text="Go", command=self.draw_path)
        self.button.pack(side='left')
        self.draw()



    def draw(self,color=""):
        for row in self.grid:
            for cell in row:
                cell.draw(color)

    def draw_obstacle(self):
        for row in self.grid:
            for cell in row:
                cell.draw_obstacle()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

        if self.count == 1:#starting point
            self.start = (row,column)
            cell.draw("yellow")
        if self.count == 2:#end point
            self.end = (row,column)
            cell.draw("green")
        if self.count > 2 :#normal point
            #https://stackoverflow.com/questions/44209368/how-to-change-a-single-value-in-a-numpy-array
            self.array[row,column] = 1
            cell.draw()
        self.count += 1

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        if self.count > 2 :#normal point
            self.array[row,column] = 1
        self.count += 1
        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)

    def draw_path(self, _event=None):
        x_coords , y_coords = A_code.a_star_compute(self.array ,self.start ,self.end)
        for i in range(1,len(x_coords)-1):
            x = x_coords[i]
            y = y_coords[i]
            cell = self.grid[x][y]
            cell._switch()
            cell.draw_obstacle()
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.start_np = np.array(self.start)
        self.end_np = np.array(self.end)
        self.path = np.array(list(zip(x_coords,y_coords)))
        fig, ax = plt.subplots(figsize=(20, 20))
        ax.imshow(self.array, cmap=plt.cm.Dark2)
        ax.scatter(self.start[1], self.start[0], marker="*", color="yellow", s=200)
        ax.scatter(self.end[1], self.end[0], marker="*", color="red", s=200)
        ax.plot(y_coords, x_coords, color="black")
        plt.show()


if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, 30, 30, 30)
    grid.pack()

    app.mainloop()


















    

