from sampler import sample
from tree import Tree
from file_parse import parse_problem
from visualizer import visualize_lines
import numpy as np


def is_near_target(tree, point):
    cloud_radius = 0.2
    dist = np.linalg.norm(np.array([point[0], point[1]]) - np.array([tree.goal[0], tree.goal[1]]))
    if dist < 2 * cloud_radius:
        tree.add(point, tree.goal)
        tree.success = True
        return True


def rrt(robot, obstacles, start, goal, n_iter):
    start = tuple(start)
    goal = tuple(goal)
    tree = Tree(robot, obstacles, start, goal)
    for _ in range(n_iter):
        sample_point = sample()
        nearest_in_tree = tree.nearest(sample_point)
        valid_connection = tree.extend(nearest_in_tree, sample_point)
        if is_near_target(tree, valid_connection):
            break

    final = None
    if tree.success:
        final = [goal]
        while final[0] != start:
            final.insert(0, tree.parent(final[0]))
        print(final)
    else:
        print(f"Path Not Found with {n_iter} iterations")


    path = None
    if tree.success:
        path = [goal]
        while path[-1] != start:
            path.append(tree.parent(path[-1]))
        path = path[::-1]
        print(path)
    else:
        print(f"Path Not Found with {n_iter} iterations")

    print(tree.cost)
    print_paths = []
    for key, value in tree.vertex_and_edges.items():
        for i in value:
            print_paths.append([key, i])

    visualize_lines(print_paths, robot, obstacles, start, goal)
    return path


if __name__ == "__main__":
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot1, obstacles1, problems1 = parse_problem(world, problem)
    # robot_point = sample()
    # robot_point = (0, 0)
    # print(isCollisionFree(robot1, robot_point, obstacles1))
    rrt(robot1, obstacles1, problems1[0][0], problems1[0][1], 20000)