from maze import Maze
from cell import Cell
from queue import PriorityQueue

# Determine if cell has is part of maze
def is_valid(maze, row, col):
    return (row >= 0) and (row < maze._num_rows) and (col >= 0) and (col < maze._num_cols)

# Determine if cell has wall
def is_unblocked(maze, from_cell, to_cell):
    # print(f"Checking if Cell {from_cell} has walls ----------------")
    # print(f"Does Cell {from_cell} have a bottom wall? {maze._cells[from_cell[0]][from_cell[1]].has_bottom_wall} ")
    # print(f"Does Cell {from_cell} have a top wall? {maze._cells[from_cell[0]][from_cell[1]].has_top_wall} ")
    # print(f"Does Cell {from_cell} have a left wall? {maze._cells[from_cell[0]][from_cell[1]].has_left_wall} ")
    # print(f"Does Cell {from_cell} have a right wall? {maze._cells[from_cell[0]][from_cell[1]].has_right_wall} ")
    
    # print(f"Checking if Cell {to_cell} has walls ----------------")
    # print(f"Does Cell {to_cell} have a bottom wall? {maze._cells[to_cell[0]][to_cell[1]].has_bottom_wall} ")
    # print(f"Does Cell {to_cell} have a top wall? {maze._cells[to_cell[0]][to_cell[1]].has_top_wall} ")
    # print(f"Does Cell {to_cell} have a left wall? {maze._cells[to_cell[0]][to_cell[1]].has_left_wall} ")
    # print(f"Does Cell {to_cell} have a right wall? {maze._cells[to_cell[0]][to_cell[1]].has_right_wall} ")
  
    if (
        to_cell[1] < maze._num_rows - 1
        and not maze._cells[to_cell[0]][to_cell[1]].has_top_wall
        and not maze._cells[from_cell[0]][from_cell[1]].has_bottom_wall
    ):
        return True
    if (
        to_cell[1] > 0
        and not maze._cells[to_cell[0]][to_cell[1]].has_bottom_wall
        and not maze._cells[from_cell[0]][from_cell[1]].has_top_wall
        and from_cell != (0, 0) #Check if start node
    ):
        return True
    if (
        to_cell[0] > 0
        and not maze._cells[to_cell[0]][to_cell[1]].has_right_wall
        and not maze._cells[from_cell[0]][from_cell[1]].has_left_wall 
    ):
        return True
    if (
        to_cell[0] < maze._num_cols -1
        and not maze._cells[to_cell[0]][to_cell[1]].has_left_wall
        and not maze._cells[from_cell[0]][from_cell[1]].has_right_wall 
    ):
        return True
    return False

def is_destination(maze, i, j):
    if (maze._num_rows-1 == i and maze._num_cols-1 == j):
        return True
    return False

def calculate_h(maze, row, col):
    return ((row - maze._num_rows) ** 2 + (col - maze._num_cols) ** 2) ** 0.5

def astar(maze):
    i = 0
    j = 0

    # Initialize closed list (visited cells)
    closed_list = [[False for _ in range(maze._num_cols)] for _ in range(maze._num_rows)]

    # Initialize start cell details
    cell_details = [[Cell() for _ in range(maze._num_cols)] for _ in range(maze._num_rows)]

    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = 0
    cell_details[i][j].parent_j = 0

    open_list = []
    found_dest = False # found flag
    open_list.append((i, j))

    # Main A* loop
    while len(open_list) > 0:
        p = open_list.pop()
        i = p[0]
        j = p[1]

        print(f"Cell {i}, {j}")
        closed_list[i][j] = True
        # print(f"Closed_List: {closed_list}")

        # Check each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # print(f"Current Cell: {new_i}, {new_j}")
            # If the successor is valid, unblocked and not visited
            if is_valid(maze, new_i, new_j) and is_unblocked(maze, (i, j), (new_i, new_j)) and not closed_list[new_i][new_j]:
                # print(f"Current Cell: {new_i}, {new_j}")
                maze._cells[new_i][new_j].draw_move(maze._cells[i][j])
                # if successor is destination
                if is_destination(maze, new_i, new_j):
                    # set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("Found Destination")
                    # trace and print the path from source to destination
                    found_dest = True
                    return found_dest
                else:
                    # calculate new f, g, h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h(maze, new_i, new_j)
                    f_new = g_new + h_new
                    # if cell is not in the open_list or the new f value is smaller
                    if (cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new):
                        # add the cell to the open list
                        open_list.append((new_i, new_j))
                        # update cell_details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
    
    if not found_dest:
        print(f"Failed to find the destination cell")
        return False

