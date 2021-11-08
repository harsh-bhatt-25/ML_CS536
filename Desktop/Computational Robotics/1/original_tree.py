# import numpy as np
# from collision import isCollisionFree, do_segments_intersect, Point, check_collision, get_intersection_point
# from file_parse import parse_problem, get_robot_global_coordinates
# from sampler import sample
# np.seterr(divide='ignore', invalid='ignore')
#
#
# class Node:
#     def __init__(self, node, parent=None):
#         self.node = node
#         self.children = []
#         self.parent = parent
#
#
# class Tree:
#     def __init__(self, robot, obstacles, start, goal, incremental_distance=0.1):
#         """
#         :param robot: robot configuration
#         :param obstacles: list of obstacles with their configurations
#         :param start: list, initial location
#         :param goal: list, goal location
#         """
#         self.robot = robot
#         self.obstacles = obstacles
#         self.start = tuple(start)
#         self.goal = tuple(goal)
#         self.incremental_distance = incremental_distance
#         self.index = 1
#         self.increment = 0.6
#         # head = Node(start)
#         # self.head = head
#         self.sx = self.goal[0] - self.start[0]
#         self.sy = self.goal[1] - self.start[1]
#
#         self.edges = {self.start: None}
#         self.vertices = {self.start: []}
#         # self.neighbors = {0: []}
#
#     def add(self, point1, point2):
#         if not self.exists(point2):
#             self.vertices[point2] = [point1]
#             self.vertices[point1].append(point2)
#             # self.neighbors[point2] = []
#             # E[child] = parent
#             self.edges[point2] = point1
#         else:
#             return
#
#     def exists(self, point):
#         return True if point in self.vertices else False
#
#     def parent(self, point):
#         return self.edges[point]
#
#     def nearest(self, point):
#         min_dist = float('inf')
#         for current_vertex in self.vertices:
#             distance = np.linalg.norm(np.array(current_vertex) - np.array(point))
#             if distance < min_dist:
#                 min_dist = distance
#                 min_point = current_vertex
#
#         return min_point
#
#     # def extend(self, point1, point2):
#     #     # If no collision between points, just add them
#     #     if isCollisionFree(self.robot, point2, self.obstacles):
#     #         self.add(point1, point2)
#     #     else:
#     #         print("HI")
#     #     #     isCollisionFree(self.robot, point2, self.obstacles)
#     #     #     # If collision, find the intersection point of the new line to the obstacle line
#     #     #     # Subtract 0.00001 so that the point is not on the obstacle
#     #     #     collision_segment = check_collision([point1, point2], self.obstacles, return_points=True)
#     #     #     if check_collision([point1, point2], self.obstacles):
#     #     #         intersection_point = get_intersection_point(point1, point2, collision_segment[0], collision_segment[1])
#     #     #         # intersection_point = (intersection_point[0] - delta, intersection_point[1] - delta)
#     #     #         self.add(point1, intersection_point)
#
#     def extend(self, point1, point2):
#         dirn = np.array(point2) - np.array(point1)
#         length = np.linalg.norm(dirn)
#         dirn = (dirn / length) * min(self.increment, length)
#         prev = point1
#
#         while prev != point2:
#             new_point = (round(prev[0] - dirn[0], 1), round(prev[1] - dirn[1], 1))
#             # print(new_point)
#             if isCollisionFree(self.robot, new_point, self.obstacles) and not self.exists(new_point):
#                 self.add(prev, new_point)
#                 prev = new_point
#             else:
#                 # self.add(point1, prev)
#                 break
#         return prev
#
#
# if __name__ == "__main__":
#     world = "world_definition_files/robot_env_01.txt"
#     problem = "problem_definition_files/probs_01.txt"
#     robot1, obstacles1, problems1 = parse_problem(world, problem)
#     # robot_point = sample()
#     robot_point = (0, 0)
#     print(isCollisionFree(robot1, robot_point, obstacles1))


import numpy as np
from original_collision import isCollisionFree, do_segments_intersect, Point, check_collision, get_intersection_point
from file_parse import parse_problem, get_robot_global_coordinates
from sampler import sample
from collections import defaultdict


class Tree:
    def __init__(self, robot, obstacles, start, goal):
        self.robot = robot
        self.obstacles = obstacles
        self.goal = goal
        self.vertices = set()
        # self.edges = defaultdict(list)
        self.vertices.add(start)
        self.edges = {}
        self.edges[None] = start
        self.stepSize = 0.6

    def add(self, point1, point2):
        self.vertices.add(point2)
        self.edges[point1] = point2

    def exists(self, point):
        if point in self.vertices:
            return True
        else:
            return False

    def parent(self, point):
        for k, v in self.edges.items():
            if v == point:
                return k
        return -1

    def nearest(self, point):
        nearest = None
        min_dist = None
        for vertex in self.vertices:
            dist = np.linalg.norm(np.array(point) - np.array(vertex))
            if min_dist is None or dist <= min_dist:
                min_dist = dist
                nearest = vertex
        return vertex

    def extend(self, point1, point2):
        dirn = np.array(point2) - np.array(point1)
        length = np.linalg.norm(dirn)
        dirn = (dirn / length) * min(self.stepSize, length)
        prev = point1

        while prev != point2:
            new_point = (round(prev[0] - dirn[0], 1), round(prev[1] - dirn[1], 1))
            # print(new_point)
            if isCollisionFree(self.robot, new_point, self.obstacles) and not self.exists(new_point):
                self.add(prev, new_point)
                prev = new_point
            else:
                # self.add(point1, prev)
                break
        return prev
