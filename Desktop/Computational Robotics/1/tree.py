from collision import isCollisionFree
import numpy as np
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
            distance = np.linalg.norm(np.array([vertex[0], vertex[1]]) - np.array([point[0], point[1]]))
            if distance < minimum:
                nearest_point = vertex
                minimum = distance
        return nearest_point

    def extend(self, point1, point2):
        prev = point1
        x, y = point1
        step = 0.1
        while True:
            distance = np.linalg.norm(np.array([x, y]) - np.array([point2[0], point2[1]]))
            x = round((1 - step / distance) * prev[0] + step / distance * point2[0], 2)
            y = round((1 - step / distance) * prev[1] + step / distance * point2[1], 2)
            if not isCollisionFree(self.robot, (x, y), self.obstacles):
                if not self.rewire_flag:
                    break
                else:
                    return False

            if np.linalg.norm(np.array([point1[0], point1[1]]) - np.array([x, y])) < np.linalg.norm(
                    np.array([point1[0], point1[1]]) - np.array([point2[0], point2[1]])):
                prev = x, y
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
            try:
                cost += self.cost[(parent, pt)]
            except:
                return 100
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
