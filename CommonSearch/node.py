class Node:
    def __init__(self, point, path, cost, heuristic=100):
        self.point = point
        self.path = path
        self.cost = cost
        self.heuristic = heuristic