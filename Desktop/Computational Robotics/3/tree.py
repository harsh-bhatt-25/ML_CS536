from collision import isCollisionFree
import numpy as np
import math
np.seterr(divide='ignore', invalid='ignore')


class Tree:
    def __init__(self, robot, obstacles, start, goal):
        self.robot = robot
        self.obstacles = obstacles
        self.start = start
        self.goal = goal
        self.vertex_and_edges = {self.start: set()}
        self.success = False
        self.cost = {}
        self.rewire_flag = False
        self.near_point = None

    def get_distance(self, p1, p2):
        try:
            theta1, theta2 = p1[2], p2[2]
            theta = theta1 - theta2

            theta = math.radians((math.degrees(theta) + 180) % 360 - 180)
            return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]) + np.square(theta))
        except:
            print("------------------------------")
            print(p1, p2)

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
        minimum, nearest_point = float("inf"), None
        for vertex in self.vertex_and_edges.keys():
            distance = self.get_distance(vertex, point)
            if distance < minimum:
                nearest_point = vertex
                minimum = distance
        return nearest_point

    def extend(self, point, n1, n2, dt):
        u = [(np.random.uniform(2., 6.), np.random.uniform(0.01, 0.09)) for i in range(0, 50)]
        n = [np.random.uniform(low=n1, high=n2) for _ in range(0, 50)]
        states = self.robot.propagate(point, u, n, dt)

        cur = point
        for state_new in states[1:]:
            if not isCollisionFree(self.robot, state_new, self.obstacles) or self.exists(state_new):
                break
            cur = state_new
        if cur != point:
            self.add(point, cur)
            return cur
        else:
            return None
