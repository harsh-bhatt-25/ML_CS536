from collision import isCollisionFree
import numpy as np
import math
np.seterr(divide='ignore', invalid='ignore')


def get_distance(p1, p2):
    theta1, theta2 = p1[2], p2[2]
    theta = theta1 - theta2

    theta = math.radians((math.degrees(theta) + 180) % 360 - 180)
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]) + np.square(theta))


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
            distance = get_distance(vertex, point)
            if distance < minimum:
                nearest_point = vertex
                minimum = distance
        return nearest_point

    def extend(self, point1, point2):
        prev = point1
        step = 0.1
        while True:
            distance = get_distance(prev, point2)
            x = round((1 - step / distance) * prev[0] + step / distance * point2[0], 2)
            y = round((1 - step / distance) * prev[1] + step / distance * point2[1], 2)
            theta = round((1 - step / distance) * prev[2] + step / distance * point2[2], 2)
            if not isCollisionFree(self.robot, (x, y, theta), self.obstacles):
                if not self.rewire_flag:
                    break
                else:
                    return False

            if get_distance(point1, [x, y, theta]) < get_distance(point1, point2):
            # if np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([x, y])) < np.linalg.norm(
            #         np.array([point1[0], point1[1]]) - np.array([point2[0], point2[1]])):
                prev = x, y, theta
            else:
                break
        if not self.rewire_flag:
            self.add(point1, prev)
            self.cost[(point1, prev)] = np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([prev[0], prev[1]]))
            return prev
        else:
            return True

    def get_cost(self, point):
        cost, pt = 0, point
        while pt != self.start:
            parent = self.parent(pt)
            cost += self.cost[(parent, pt)]
            pt = parent
        return cost

    def rewire(self, point, r):
        nearest_node, node_cost = self.near_point, None
        minimum_dist = float("inf")
        for current_node in self.vertex_and_edges:
            node_cost = self.get_cost(current_node)
            distance = np.linalg.norm(np.array([current_node[0], current_node[1]]) - np.array([point[0], point[1]]))
            final_cost = node_cost + distance
            if current_node == point:
                continue
            if distance < r:
                if final_cost < minimum_dist and self.extend(current_node, point):
                    nearest_node = current_node
                    minimum_dist = final_cost
        if nearest_node != self.near_point:
            if point in self.vertex_and_edges[self.near_point]:
                self.vertex_and_edges[self.near_point].remove(point)
                self.vertex_and_edges[nearest_node].add(point)
                self.cost[(nearest_node, point)] = node_cost
        return nearest_node
