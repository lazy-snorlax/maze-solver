from cell import Cell
import random
import time


class Maze:
    def __init__(
            self, 
            x1, 
            y1, 
            num_rows, 
            num_cols, 
            cell_size_x, 
            cell_size_y, 
            win=None,
            seed=None
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)

        self.create_cells()
        self._break_entrance_and_exit()
        self.break_walls_r(0,0)
        self.reset_cells_visited()
    
    def create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self.draw_cell(i, j)
    
    def draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self.animate()

    def animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self.draw_cell(self._num_cols - 1, self._num_rows - 1)

    def break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # left
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j-1].visited:
                next_index_list.append((i, j-1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                next_index_list.append((i, j+1))

            # if no where to go from here
            # break out
            if len(next_index_list) == 0:
                self.draw_cell(i, j)
                return
            
            # randomly choose next direction
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            
            self.break_walls_r(next_index[0], next_index[1])
    
    def reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    # Depth-First Search
    def solve_r(self, i, j):
        self.animate()

        self._cells[i][j].visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        # move left if no wall and not visited
        if ( 
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self.solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        
        # move right if no wall and not visited
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self.solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if no wall and not visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self.solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if no wall and not visited
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self.solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # dead end, the previous cell know by returning False
        return False

    def solve(self):
        return self.solve_r(0, 0)