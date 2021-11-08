import numpy as np
from collision import isCollisionFree
from file_parse import parse_problem, get_robot_global_coordinates
from sampler import sample
from visualizer import visualize_lines
from tree import Tree
import matplotlib.pyplot as plt


# def rrt(robot, obstacles, start, goal, iter_n):
#     t = Tree(robot, obstacles, tuple(start), tuple(goal))
#
#     # t.add(t.start, (0.3, 0.3))
#     # t.extend(t.start, (0.2, 0.2))
#
#     # samples = 10
#     for _ in range(iter_n):
#         sample_list = []
#         # for _ in range(samples):
#         #     # s = sample()
#         #     # posx = t.start[0] - (t.sx / 2.) + s[0] * t.sx * 2
#         #     # posy = t.start[1] - (t.sy / 2.) + s[1] * t.sy * 2
#         #     # sample_list.append((posx, posy))
#         #     sample_list.append(sample())
#
#         samples = sample()
#         if isCollisionFree(t.robot, samples, t.obstacles):
#             near_node = t.nearest(samples)
#             t.extend(near_node, samples)
#         else:
#             print("+++++++++++++++++++++++++++++++++")
# for current_sample in sample_list:
#     near_node = t.nearest(current_sample)
#     t.extend(near_node, current_sample)

# To have proper format fo r points to plot them
# print_paths = []
# for key, val in t.vertices.items():
#     for v in val:
#         print_paths.append([key, v])
# print(print_paths)

# visualize_lines(print_paths, robot, obstacles, start, goal)

def rrt(robot, obstacles, start, goal, iter_n):
    tree = Tree(robot, obstacles, tuple(start), goal)
    samples = []
    for i in range(0, iter_n):
        point2 = sample()
        nearest = tree.nearest(point2)
        if isCollisionFree(tree.robot, point2, tree.obstacles) and not tree.exists(point2):
            tree.extend(nearest, point2)

    # print(samples)
    print(tree.vertex_and_edges)
    # nearest = tree.nearest(goal)
    # last = tree.extend(nearest, goal)
    # path = []
    # init = tree.edges[None]
    # while init in tree.edges:
    #     path.append(init)
    #     init = tree.edges(init)
    # # if goal not in path:
    # #     path.append(goal)
    # # visualize_lines(path, robot, obstacles, start, goal)
    # return path


if __name__ == "__main__":
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot1, obstacles1, problems1 = parse_problem(world, problem)
    # robot_point = sample()
    # robot_point = (0, 0)
    # print(isCollisionFree(robot1, robot_point, obstacles1))
    rrt(robot1, obstacles1, problems1[0][0], problems1[0][1], 20)
