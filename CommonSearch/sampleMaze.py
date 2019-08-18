"""
A sample maze that have multiple points that can be configured to be starting/ending points.
Can run through command line and will color in the expanded/queued nodes along with the final path found.
"""

from InformedSearch import InformedSearch
from UninformedSearch import UninformedSearch
from Node import Node
from termcolor import colored
import argparse
import sys

# 0 = unvisited
# 1 = wall
# 2 = queued
# 3 = visited
# (x, y) = point
# x = x coordinate
# y = y coordinate

parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='algorithm', help="algorithm to find path [bfs, dfs, ucs, dls, ids, greedy, astar, hill, beam]")
parser.add_argument('-p', dest='endpoints', help="set of start and end points. [1 = (S, E1), 2 = (S, E2), 3 = (0,0;24,24)]")

maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
]


points = {
    "S": (2, 11),
    "E2": (2, 21),
    "E1": (23, 19),
    "0,0": (0, 0),
    "24,24": (24, 24)
}

def main():
    args = parser.parse_args()
    algo = args.algorithm
    endpoints = args.endpoints

    if endpoints == '1':
        starting_point = points["S"]
        ending_point = points["E1"]
    if endpoints == '2':
        starting_point = points["S"]
        ending_point = points["E2"]
    if endpoints == '3':
        starting_point = points["0,0"]
        ending_point = points["24,24"]

    informedSearch = InformedSearch(maze, starting_point, ending_point)
    uninformedSearch = UninformedSearch(maze, starting_point, ending_point)
    
    if algo == 'bfs':
        cost, path, explored = uninformedSearch.bfs()
    elif algo == 'dfs':
        cost, path, explored = uninformedSearch.dfs()
    elif algo == 'ucs':
        cost, path, explored = uninformedSearch.ucs()
    elif algo == 'ids':
        cost, path, explored = uninformedSearch.ids()
    elif algo == 'dls':
        cost, path, explored = uninformedSearch.dls()
    elif algo == 'astar':
        cost, path, explored = informedSearch.a_star()
    elif algo == 'greedy':
        cost, path, explored = informedSearch.greedy()
    elif algo == 'hill':
        cost, path, explored = informedSearch.hill()
    elif algo == 'beam':
        cost, path, explored = informedSearch.beam()
    
    printOutput(cost, path, explored)
    
def printOutput(cost, path, explored):
    maze.reverse()
    for i in range(25):
        for j in range(25):
            point = maze[i][j]
            if (j, 24-i) in path:
                print colored(point, "yellow"),
                continue
            if point == 0:
                print point,
            if point == 1:
                print colored(point, "red"),
            if point == 2:
                print colored(point, "blue"),
            if point == 3:
                print colored(point, "green"),
        print ""
    print "Path: {}".format(path)
    print "Cost: {}".format(cost)
    print "Explored: {}".format(explored)

if __name__ == "__main__":
    main()