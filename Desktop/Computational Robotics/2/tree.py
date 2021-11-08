from collision import isCollisionFree
import numpy as np
from collections import defaultdict
import math

np.seterr(divide='ignore', invalid='ignore')


def get_distance(p1, p2):
    theta1, theta2 = p1[2], p2[2]
    theta = theta1 - theta2
    theta = math.radians((math.degrees(theta) + 180) % 360 - 180)
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1], p2[1]) + np.square(theta))


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

    def exists(self, point):
        return True if point in self.vertex_and_edges else False

    def parent(self, point):
        for vertex, connections in self.vertex_and_edges.items():
            if point in connections:
                return vertex

    def nearest(self, point):
        min_dist = float("inf")
        min_pt = None
        for vertex in self.vertex_and_edges.keys():
            distance = get_distance(vertex, point)
            if distance < min_dist:
                min_pt = vertex
                min_dist = distance
        return min_pt

    def extend(self, point1, point2):
        i = point1
        x, y = point1
        while True:
            # len_ab = self.euclidean_dist((x, y), point2)
            len_ab = np.linalg.norm(np.array([x, y]) - np.array([point2[0], point2[1]]))
            len_ratio = 0.1 / len_ab
            x = round((1 - len_ratio) * i[0] + len_ratio * point2[0], 2)
            y = round((1 - len_ratio) * i[1] + len_ratio * point2[1], 2)
            if not isCollisionFree(self.robot, (x, y), self.obstacles):
                break
            if np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([x, y])) < np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([point2[0], point2[1]])):
                i = x, y
            else:
                break
        self.add(point1, i)
        return i
