from graphics import Window, Line, Point
from maze import Maze
from astar import astar
import sys


def main():
    num_rows = 10
    num_cols = 10
    margin = 50
    screen_x = 1000
    screen_y = 800
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    print("maze created")
    
    # Depth-First Search
    # is_solvable = maze.solve()

    # A* Search
    is_solvable = astar(maze)
    
    if not is_solvable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    win.wait_for_close()

main()