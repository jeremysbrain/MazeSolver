from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("Maze Solver")
        self.root_widget.wm_protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root_widget, width=width, height=height, bg="white")
        self.canvas.pack()
        self.running_state = False

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()
    
    def wait_for_close(self):
        self.running_state = True
        while self.running_state == True:
            self.redraw()
        print("Done.")
    
    def close(self):
        self.running_state = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.x1 = p1.x
        self.x2 = p2.x
        self.y1 = p1.y
        self.y2 = p2.y
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)

class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False
    
    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win != None:
            bg_color = "white"

            if self.has_left_wall:
                wall_color = "black"
            else:
                wall_color = bg_color
            self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), wall_color)

            if self.has_right_wall:
                wall_color = "black"
            else:
                wall_color = bg_color
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), wall_color)

            if self.has_top_wall:
                wall_color = "black"
            else:
                wall_color = bg_color
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), wall_color)

            if self.has_bottom_wall:
                wall_color = "black"
            else:
                wall_color = bg_color
            self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), wall_color)
    
    def draw_move(self, to_cell, undo=False):
        fill_color = "red"
        if undo == True:
            fill_color = "gray"
        self_center_x = abs((self.__x1 + self.__x2) // 2)
        self_center_y = abs((self.__y1 + self.__y2) // 2)
        dest_center_x = abs((to_cell.__x1 + to_cell.__x2) // 2)
        dest_center_y = abs((to_cell.__y1 + to_cell.__y2) // 2)

        self_line = Line(Point(self_center_x, self_center_y), Point(self_center_x, dest_center_y))
        dest_line = Line(Point(dest_center_x, dest_center_y), Point(self_center_x, dest_center_y))
        
        if self.__win != None:
            self.__win.draw_line(self_line, fill_color)
            self.__win.draw_line(dest_line, fill_color)