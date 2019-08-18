from node import Node

class InformedSearch:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
    
    def isValid(self, point):
        return point[0] >= 0 and point[0] < 25 \
            and point[1] >= 0 and point[1] < 25 \
            and self.maze[point[1]][point[0]] == 0

    # heuristic function
    def getManhattan(self, point, goal):
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])

    def a_star(self):
        open_q = [Node(self.start, [], 1)]
        closed_q = []
        explored = 0

        while open_q:
            curr = open_q.pop(0)
            newPath = curr.path[:]
            newPath.append(curr.point)
            x, y = curr.point
            if curr.point == self.end: 
                curr.path.append(curr.point)
                self.maze[y][x] = 3
                explored += 1
                break
            # up
            if self.isValid((x, y-1)): 
                open_q.insert(0, Node((x, y-1), newPath, curr.cost + 1, curr.cost + 1 + self.getManhattan((x, y-1), self.end)))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.insert(0, Node((x, y+1), newPath, curr.cost + 1, curr.cost + 1 + self.getManhattan((x, y+1), self.end)))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.insert(0, Node((x-1, y), newPath, curr.cost + 1, curr.cost + 1 + self.getManhattan((x-1, y), self.end)))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)):
                open_q.insert(0, Node((x+1, y), newPath, curr.cost + 1, curr.cost + 1 + self.getManhattan((x+1, y), self.end)))
                self.maze[y][x+1] = 2
            
            open_q = sorted(open_q, key=lambda x: x.heuristic)

            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored
    
    def greedy(self):
        open_q = [Node(self.start, [], 1)]
        closed_q = []
        explored = 0

        while open_q:
            curr = open_q.pop(0)
            newPath = curr.path[:]
            newPath.append(curr.point)
            x, y = curr.point
            if curr.point == self.end: 
                curr.path.append(curr.point)
                self.maze[y][x] = 3
                explored += 1
                break
            # up
            if self.isValid((x, y-1)): 
                open_q.insert(0, Node((x, y-1), newPath, curr.cost + 1, 1 + self.getManhattan((x, y-1), self.end)))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.insert(0, Node((x, y+1), newPath, curr.cost + 1, 1 + self.getManhattan((x, y+1), self.end)))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.insert(0, Node((x-1, y), newPath, curr.cost + 1, 1 + self.getManhattan((x-1, y), self.end)))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)):
                open_q.insert(0, Node((x+1, y), newPath, curr.cost + 1, 1 + self.getManhattan((x+1, y), self.end)))
                self.maze[y][x+1] = 2
            
            open_q = sorted(open_q, key=lambda x: x.heuristic)

            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored

    def beam(self, length=3):
        open_q = [Node(self.start, [], 1)]
        closed_q = []
        explored = 0

        while open_q:
            curr = open_q.pop(0)
            newPath = curr.path[:]
            newPath.append(curr.point)
            x, y = curr.point
            if curr.point == self.end: 
                curr.path.append(curr.point)
                self.maze[y][x] = 3
                explored += 1
                break
            # up
            if self.isValid((x, y-1)): 
                open_q.insert(0, Node((x, y-1), newPath, curr.cost + 1, 1 + self.getManhattan((x, y-1), self.end)))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.insert(0, Node((x, y+1), newPath, curr.cost + 1, 1 + self.getManhattan((x, y+1), self.end)))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.insert(0, Node((x-1, y), newPath, curr.cost + 1, 1 + self.getManhattan((x-1, y), self.end)))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)):
                open_q.insert(0, Node((x+1, y), newPath, curr.cost + 1, 1 + self.getManhattan((x+1, y), self.end)))
                self.maze[y][x+1] = 2
            
            # get the top length amount of best moves
            open_q = sorted(open_q, key=lambda x: x.heuristic)[:length+1]

            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored

    def hill(self):
        # acts like beam search but with a beam size of 1
        return self.beam(1)