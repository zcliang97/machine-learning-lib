from node import Node

class UninformedSearch:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end

    def isValid(self, point):
        return point[0] >= 0 and point[0] < 25 \
            and point[1] >= 0 and point[1] < 25 \
            and self.maze[point[1]][point[0]] == 0
    
    def getCost(self, x, y):
        # since all unit moves have the same cost, total cost is just the difference between the next coordinate and the start
        # if the maze had different costs for making different moves, it would be calculated
        return (y - self.start[1]) + (x - self.start[0])

    def bfs(self):
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
                open_q.append(Node((x, y-1), newPath, curr.cost + 1))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.append(Node((x, y+1), newPath, curr.cost + 1))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.append(Node((x-1, y), newPath, curr.cost + 1))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)): 
                open_q.append(Node((x+1, y), newPath, curr.cost + 1))
                self.maze[y][x+1] = 2
            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored
    
    def dfs(self):
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
                open_q.insert(0, Node((x, y-1), newPath, curr.cost + 1))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.insert(0, Node((x, y+1), newPath, curr.cost + 1))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.insert(0, Node((x-1, y), newPath, curr.cost + 1))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)):
                open_q.insert(0, Node((x+1, y), newPath, curr.cost + 1))
                self.maze[y][x+1] = 2
            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored

    # todo
    def ucs(self):
        open_q = [Node(self.start, [], 1)]
        closed_q = []
        explored = 0

        while open_q:
            # sort the nodes based on the lowest cost
            open_q = sorted(open_q, key=lambda node: node[0])
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
                open_q.append((self.getCost(x, y-1), Node((x, y-1), newPath, curr.cost + 1)))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)): 
                open_q.append((self.getCost(x, y+1), Node((x, y+1), newPath, curr.cost + 1)))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)): 
                open_q.append((self.getCost(x-1, y), Node((x-1, y), newPath, curr.cost + 1)))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)): 
                open_q.append((self.getCost(x+1, y), Node((x+1, y), newPath, curr.cost + 1)))
                self.maze[y][x+1] = 2
            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored
    
    def dls(self, limit=10):
        open_q = [Node(self.start, [], 1)]
        closed_q = []
        explored = 0
        isFound = False

        while open_q:
            curr = open_q.pop(0)
            newPath = curr.path[:]
            newPath.append(curr.point)
            x, y = curr.point
            if curr.point == self.end: 
                curr.path.append(curr.point)
                self.maze[y][x] = 3
                explored += 1
                isFound = True
                break
            
            # will only accept moves where the descent is within the depth limit
            # up
            if self.isValid((x, y-1)) and self.getCost(x, y-1) <= limit:
                open_q.insert(0, Node((x, y-1), newPath, curr.cost + 1))
                self.maze[y-1][x] = 2
            # down
            if self.isValid((x, y+1)) and self.getCost(x, y+1) <= limit: 
                open_q.insert(0, Node((x, y+1), newPath, curr.cost + 1))
                self.maze[y+1][x] = 2
            # left
            if self.isValid((x-1, y)) and self.getCost(x-1, y) <= limit: 
                open_q.insert(0, Node((x-1, y), newPath, curr.cost + 1))
                self.maze[y][x-1] = 2
            # right
            if self.isValid((x+1, y)) and self.getCost(x+1, y) <= limit:
                open_q.insert(0, Node((x+1, y), newPath, curr.cost + 1))
                self.maze[y][x+1] = 2
            closed_q.append(curr)
            self.maze[y][x] = 3
            explored += 1

        return curr.cost, curr.path, explored, isFound

    def ids(self):
        # ids does depth limited search for each limit and will increment the limit and rerun if the goal is not found
        limit = 1
        isFound = False
        while not isFound:
            cost, path, explored, isFound = self.dls(limit)
            limit += 1

        return cost, path, explored