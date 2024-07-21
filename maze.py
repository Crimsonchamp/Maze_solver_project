from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    #Defines window settings
    def __init__(self,w,h):
        self.__root = Tk()
        self.__root.title("Maze Solver")

        self.c = Canvas(self.__root, height=h, width=w)
        self.c.pack()

        self.running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    #Forces window to continue redrawing
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    #Checks for window close
    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
    
    #Closes window
    def close(self):
        self.running = False

    def draw_line(Line,fill_color):
        Line.draw()


class Point:
    #Point class represents singular points
    def __init__(self,x,y):
        # x is horizon, 0 is left
        # y is vert, 0 is top
        self.x = x
        self.y = y


class Line:
    #Determines points to draw a line between
    def __init__(self,p1,p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y

    #The logic of drawing between
    def draw(self,canvas,fill_color):
        canvas.create_line(
           self.x1,self.y1,self.x2,self.y2,fill=fill_color,width=2
        )
    
class Cell:
    #Wall stats
    def __init__(self,p1,p2,canvas=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = p1.x
        self._y1 = p1.y
        self._x2 = p2.x
        self._y2 = p2.y
        self._win = canvas
        self.visited = False

    #Drawing the lines at Cell's wall coodrinates
    def draw(self,canvas):
        if self.has_left_wall == True:
            l = Line(Point(self._x1,self._y1),Point(self._x1,self._y2))
            l.draw(canvas,"black")
        else:
            l = Line(Point(self._x1,self._y1),Point(self._x1,self._y2))
            l.draw(canvas,"#d9d9d9")
            
        if self.has_right_wall == True:
            l = Line(Point(self._x2,self._y1),Point(self._x2,self._y2))
            l.draw(canvas,"black")
        else:
            l = Line(Point(self._x2,self._y1),Point(self._x2,self._y2))
            l.draw(canvas,"#d9d9d9")

        if self.has_top_wall == True:
             l = Line(Point(self._x1,self._y1),Point(self._x2,self._y1))
             l.draw(canvas,"black")
        else:
            l = Line(Point(self._x1,self._y1),Point(self._x2,self._y1))
            l.draw(canvas,"#d9d9d9")

        if self.has_bottom_wall == True:
             l = Line(Point(self._x1,self._y2),Point(self._x2,self._y2))
             l.draw(canvas,"black")
        else:
            l = Line(Point(self._x1,self._y2),Point(self._x2,self._y2))
            l.draw(canvas,"#d9d9d9")

    #Draws from center of self to next cell.
    def draw_move(self, to_cell, undo=False):
        if undo == False:
            fill_color = "red"
        else:
            fill_color = "gray"
        
        cx = ((self._x2 - self._x1)/2)+self._x1
        cy = ((self._y2 - self._y1)/2)+self._y1

        tcx = ((to_cell._x2 - to_cell._x1)/2)+to_cell._x1
        tcy = ((to_cell._y2 - to_cell._y1)/2)+to_cell._y1

        l = Line(Point(cx,cy),Point(tcx,tcy))
        l.draw(self._win.c,fill_color)


class Maze:
        #x1,y1 are starting positions. 
    def __init__(self, x1,y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None:
            self.seed = random.seed(seed)
        else:
            self.seed = random.seed()
        self._create_cells()


    #Creates the grid of cells in data format
    def _create_cells(self):
        self._cells = []
        current_x = self.x1
        current_y = self.y1
        for col in range(self.num_cols):
            self._cells.append([])
            for point in range(self.num_rows):
                self._cells[col].append(
                    Cell(
                        Point(current_x,current_y),
                        Point(current_x+self.cell_size_x,current_y+self.cell_size_y),
                        self.win
                        )
                )
                current_x = current_x+self.cell_size_x
            current_x = self.x1
            current_y = current_y+self.cell_size_y
        self._break_entrance_and_exit()
        
        
        
        

    #Call for each cell in a maze to be drawn from data grid
    def _draw_cell(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell = self._cells[row][col]
                cell.draw(self.win.c)
                self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False
    
    #Reminder that i is row and j is column. So i is x and j is y.
    def _break_walls_r(self,i,j):
        #Marks current cell as visited
        self._cells[i][j].visited = True
        #On until done 
        while True:
            #Inner list of directions that can be travelled
            to_visit = []
            
            #Checks if any paths are still viable
            dead_end = 0

            #Checks up, right, down, left for directions to visit.
            if i > 0:
                if self._cells[i-1][j].visited == False:
                    to_visit.append("up")
                    dead_end += 1
            if j < self.num_cols - 1:
                if self._cells[i][j+1].visited == False:
                    to_visit.append("right")
                    dead_end += 1
            if i < self.num_rows - 1:
                if self._cells[i+1][j].visited == False:
                    to_visit.append("down")
                    dead_end += 1
            if j > 0:
                if self._cells[i][j-1].visited == False:
                    to_visit.append("left")
                    dead_end += 1

            # If there are no viable paths left, draw cell and return a step.
            if dead_end == 0:
                self._cells[i][j].draw(self.win.c)
                print("Drawing:", i,j)
                return
            
            # Choose direction at random
            direction = random.choice(to_visit)
            print("Directions",to_visit)
            print("Chosen",direction)

            #If direction, delete wall between direction cell and current cell
            
            if direction == "up":
                print(i,j, "to", i-1,j)
                self._cells[i][j].has_top_wall = False
                self._cells[i-1][j].has_bottom_wall = False
                self._break_walls_r(i-1,j)

            if direction == "right":
                print(i,j, "to", i,j+1)
                self._cells[i][j].has_right_wall = False
                self._cells[i][j+1].has_left_wall = False
                self._break_walls_r(i,j+1)

            if direction == "down":
                print(i,j, "to", i+1,j)
                self._cells[i][j].has_bottom_wall = False
                self._cells[i+1][j].has_top_wall = False
                self._break_walls_r(i+1,j)

            if direction == "left":
                print(i,j, "to", i,j-1)
                self._cells[i][j].has_left_wall = False
                self._cells[i][j-1].has_right_wall = False
                self._break_walls_r(i,j-1)

    def _reset_cells_visited(self):
        for rows in self._cells:
            for column in rows:
                column.visited = False
    
    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self,i,j):
        self._animate()
        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        self._cells[i][j].visited = True

        if i > 0:
            if not self._cells[i-1][j].visited and self._cells[i][j].has_top_wall == False:
                self._cells[i][j].draw_move(self._cells[i-1][j])
                if self._solve_r(i-1,j) == True:
                    return True
                self._cells[i-1][j].draw_move(self._cells[i][j],True)

        if j < self.num_cols - 1:
            if not self._cells[i][j+1].visited and self._cells[i][j].has_right_wall == False:
                self._cells[i][j].draw_move(self._cells[i][j+1])
                if self._cells[i][j+1] == self._cells[-1][-1]:
                    if self._cells[i][j].has_right_wall == False:
                        return True
                if self._solve_r(i,j+1) == True:
                    return True
                self._cells[i][j+1].draw_move(self._cells[i][j],True)

        if i < self.num_rows - 1:
            if not self._cells[i+1][j].visited and self._cells[i][j].has_bottom_wall == False:
                self._cells[i][j].draw_move(self._cells[i+1][j])
                if self._cells[i+1][j] == self._cells[-1][-1]:
                    if self._cells[i][j].has_bottom_wall == False:
                        return True
                if self._solve_r(i+1,j) == True:
                    return True
                self._cells[i+1][j].draw_move(self._cells[i][j],True)

        if j > 0:
            if not self._cells[i][j-1].visited and self._cells[i][j].has_left_wall == False:
                self._cells[i][j].draw_move(self._cells[i][j-1])
                if self._solve_r(i,j-1) == True:
                    return True
                self._cells[i][j-1].draw_move(self._cells[i][j],True)
        





    #Call on win's redraw, add time between each drawn line.
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)


def main():
    #Call for window
    win = Window(800,600)

    #Draw a maze, posx,posy, columns,rows, size x, size,y, window
    maze1 = Maze(30,30, 10, 10, 50, 50, win)
    maze1._draw_cell()
    maze1._break_walls_r(0,0)
    maze1._reset_cells_visited()
    maze1.solve()
    #print (maze1._cells[0][0].visited)


    #To draw cells
    #cell1 = Cell(Point(50,50),Point(100,100),win)
    #cell1.draw(win.c)
    #cell2 = Cell(Point(200,200),Point(300,300),win)
    #cell2.has_bottom_wall = False
    #cell2.draw(win.c)

    #cell1.draw_move(cell2)

    #Is the line to be drawn, followed by the call to draw
    #l = Line(Point(0,0),Point(30,30))
    #l.draw(win.c,"black")

    win.wait_for_close()
    

main()