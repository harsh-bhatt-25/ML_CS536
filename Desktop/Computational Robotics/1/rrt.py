from sampler import sample
from tree import Tree
from file_parse import parse_problem
from visualizer import visualize_lines, visualize_branches
import numpy as np


def is_near_target(tree, point):
    cloud_radius = 0.4
    dist = np.linalg.norm(np.array([point[0], point[1]]) - np.array([tree.goal[0], tree.goal[1]]))
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


def rrt(robot, obstacles, start, goal, n_iter, samples=None):
    start = tuple(start)
    goal = tuple(goal)
    tree = Tree(robot, obstacles, start, goal)

    testing_iters = 1
    successes = 0
    for _ in range(testing_iters):
        if not samples:
            for _ in range(n_iter):
                sample_point = sample()
                near_point = tree.nearest(sample_point)
                valid_connection = tree.extend(near_point, sample_point)
                if is_near_target(tree, valid_connection):
                    break

            path = get_path(tree, n_iter)
            if path:
                successes += 1
        else:
            for sample_point in samples:
                near_point = tree.nearest(sample_point)
                valid_connection = tree.extend(near_point, sample_point)
                if is_near_target(tree, valid_connection):
                    break

            path = get_path(tree, n_iter)
            if path:
                successes += 1

    branches = []
    for key, value in tree.vertex_and_edges.items():
        for i in value:
            branches.append([key, i])

    if path:
        visualize_lines(path, [robot], obstacles, start, goal)
        # visualize_branches(branches, robot, obstacles, start, goal)
    return path


if __name__ == "__main__":
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot1, obstacles1, problems1 = parse_problem(world, problem)
    rrt(robot1, obstacles1, problems1[0][0], problems1[0][1], 1000)
