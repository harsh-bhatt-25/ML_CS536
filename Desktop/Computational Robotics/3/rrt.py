from tree import Tree
import numpy as np
from file_parse import parse_problem
import random
from visualizer import visualize_path
import math


def sample():
    return [round(random.uniform(0, 10), 1), round(random.uniform(0, 10), 1), math.radians(round(random.uniform(0, 360), 0))]


def is_near_target(tree, point):
    cloud_radius = 0.4
    dist = tree.get_distance(point, tree.goal)
    if dist < cloud_radius:
        tree.add(point, tree.goal)
        tree.success = True
        return True


def get_path(tree, iterations):
    if tree.success:
        final = [tree.goal]
        while final[0] != tree.start:
            final.insert(0, tree.parent(final[0]))
        print(f"Path is {final}")
        return final
    else:
        print(f"Path Not Found with {iterations} iterations")


def rrt_star(robot, obstacles, start, goal, n_iter):
    start = tuple(start)
    goal = tuple(goal)
    tree = Tree(robot, obstacles, start, goal)
    r = 0.5
    n1, n2 = 50, 150
    dt = 0.05
    for _ in range(n_iter):
        near_point = tree.nearest(sample())
        valid_connection = tree.extend(near_point, n1, n2, dt)

        if is_near_target(tree, valid_connection):
            break

    path = get_path(tree, n_iter)

    branches = []
    for key, value in tree.vertex_and_edges.items():
        for i in value:
            branches.append([key, i])

    robot.set_pose((start[0], start[1], 0))
    initial = robot.transform()
    robot.set_pose((goal[0], goal[1], 1.8))
    final = robot.transform()

    # animate(robot, path, obstacles, start, goal)
    visualize_path(path, [initial, final], obstacles, start, goal)
    return path


if __name__ == "__main__":
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot1, obstacles1, problems1 = parse_problem(world, problem)
    n_iters = 2000
    samples = []
    # for i in range(n_iters):
    #     samples.append(sample())

    # rrt.rrt(robot1, obstacles1, problems1[0][0], problems1[0][1], 2000, samples=samples)
    rrt_star(robot1, obstacles1, problems1[0][0], problems1[0][1], 2000)
