from cells import *
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__cells = []
        self.__win = win
        if seed != None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for c in range(self.__num_cols):
            col = []
            for r in range(self.__num_rows):
                #if self.__win != None:
                col.append(Cell(self.__win))
            self.__cells.append(col)
        if self.__win != None:
            for c in range(self.__num_cols):
                for r in range(self.__num_rows):
                    self.__draw_cell(c, r)
        
    def __draw_cell(self, c, r):
        x1 = self.__x1 + self.__cell_size_x * c
        y1 = self.__y1 + self.__cell_size_y * r
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        if self.__win != None:
            self.__cells[c][r].draw(x1, y1, x2, y2)
            self.__animate()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.1)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, c, r):
        self.__cells[c][r].visited = True
        while True:
            next_cells = []

            if (c > 0) and (self.__cells[c - 1][r].visited == False):
                next_cells.append((c - 1, r))
            if (c < self.__num_cols - 1) and (self.__cells[c + 1][r].visited == False):
                next_cells.append((c + 1, r))
            if (r > 0) and (self.__cells[c][r - 1].visited == False):
                next_cells.append((c, r - 1))
            if (r < self.__num_rows - 1) and (self.__cells[c][r + 1].visited == False):
                next_cells.append((c, r + 1))

            if len(next_cells) == 0:
                self.__draw_cell(c, r)
                return

            next_direction = random.randrange(len(next_cells))
            next_step = next_cells[next_direction]

            
            if next_step[0] == c + 1:
                #print("C, R:", c, r)
                self.__cells[c][r].has_right_wall = False
                self.__cells[c + 1][r].has_left_wall = False
            if next_step[0] == c - 1:
                #print("C, R:", c, r)
                self.__cells[c][r].has_left_wall = False
                self.__cells[c - 1][r].has_right_wall = False
            if next_step[1] == r + 1:
                #print("C, R:", c, r)
                self.__cells[c][r].has_bottom_wall = False
                self.__cells[c][r + 1].has_top_wall = False
            if next_step[1] == r - 1:
                #print("C, R:", c, r)
                self.__cells[c][r].has_top_wall = False
                self.__cells[c][r - 1].has_bottom_wall = False
            
            self.__break_walls_r(next_step[0], next_step[1])
    
    def __reset_cells_visited(self):
        for c in range(self.__num_cols):
            for r in range(self.__num_rows):
                self.__cells[c][r].visited = False
    
    def _solve_r(self, c, r):
        self.__animate()

        self.__cells[c][r].visited = True

        if c == self.__num_cols - 1 and r == self.__num_rows - 1:
            # Successfully solved the maze
            return True
        
        current_cell = self.__cells[c][r]
        
        if c > 0:
            cell_left = self.__cells[c - 1][r]
            if (current_cell.has_left_wall == False) and (cell_left.visited == False):
                current_cell.draw_move(cell_left)
                if self._solve_r(c - 1, r):
                    return True
                else:
                    current_cell.draw_move(cell_left, True)
        
        if c < self.__num_cols - 1:
            cell_right = self.__cells[c + 1][r]
            if (current_cell.has_right_wall == False) and (cell_right.visited == False):
                current_cell.draw_move(cell_right)
                if self._solve_r(c + 1, r):
                    return True
                else:
                    current_cell.draw_move(cell_right, True)

        if r > 0:
            cell_up = self.__cells[c][r - 1]
            if (current_cell.has_top_wall == False) and (cell_up.visited == False):
                current_cell.draw_move(cell_up)
                if self._solve_r(c, r - 1):
                    return True
                else:
                    current_cell.draw_move(cell_up, True)

        if r < self.__num_rows - 1:
            cell_down = self.__cells[c][r + 1]
            if (current_cell.has_bottom_wall == False) and (cell_down.visited == False):
                current_cell.draw_move(cell_down)
                if self._solve_r(c, r + 1):
                    return True
                else:
                    current_cell.draw_move(cell_down, True)
        
        return False
    
    def solve(self):
        return self._solve_r(0, 0)

        