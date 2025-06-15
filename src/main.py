
from cells import *
from maze import *
import sys

def main():
    sys.setrecursionlimit(10000)
    win = Window(800, 600)

    m = Maze(10,10,6,6,60,60, win, 140)
    solvable = m.solve()
    if solvable:
        print("Maze Solved!")
    else:
        print("I got stuck on this one")

    win.wait_for_close()

if __name__ == "__main__":
    main()