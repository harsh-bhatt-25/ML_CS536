from collision import isCollisionFree
import numpy as np
from collections import defaultdict

np.seterr(divide='ignore', invalid='ignore')


def get_manhattan_distance(p1, p2):
    return np.abs(np.array([p1[0], p1[1]]) - np.array([p2[0], p2[1]])).sum()


class Tree:
    def __init__(self, robot, obstacles, start, goal):
        self.robot = robot
        self.obstacles = obstacles
        self.start = start
        self.goal = goal
        self.vertex_and_edges = {self.start: set()}
        self.success = False
        self.cost = {}

    def add(self, point1, point2):
        point1 = tuple(point1)
        point2 = tuple(point2)
        if point1 != point2:
            self.vertex_and_edges[point1].add(point2)
            self.vertex_and_edges[point2] = set()
            self.cost[(point1, point2)] = get_manhattan_distance(point1, point2) + self.get_cost(point1)

    def exists(self, point):
        return True if point in self.vertex_and_edges else False

    def parent(self, point):
        for vertex, connections in self.vertex_and_edges.items():
            if point in connections:
                return vertex

    def nearest(self, point):
        minimum, nearest_point = float("inf"), None
        for vertex in self.vertex_and_edges.keys():
            distance = np.linalg.norm(np.array([vertex[0], vertex[1]]) - np.array([point[0], point[1]]))
            if distance < minimum:
                nearest_point = vertex
                minimum = distance
        return nearest_point

    def extend(self, point1, point2):
        prev = point1
        x, y = point1

        while True:
            distance = np.linalg.norm(np.array([x, y]) - np.array([point2[0], point2[1]]))
            len_ratio = 0.1 / distance
            x = round((1 - len_ratio) * prev[0] + len_ratio * point2[0], 2)
            y = round((1 - len_ratio) * prev[1] + len_ratio * point2[1], 2)
            if not isCollisionFree(self.robot, (x, y), self.obstacles):
                break

            if np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([x, y])) < np.linalg.norm(
                    np.array([point1[0], point1[1]]) - np.array([point2[0], point2[1]])):
                prev = x, y
            else:
                break
        self.add(point1, prev)
        return prev

    def get_cost(self, point):
        cost = 0
        parent = point
        while parent != self.start:
            pt = parent
            parent = self.parent(pt)
            cost += self.cost[(parent, pt)]
        return cost

    def rewire(self):
        pass
