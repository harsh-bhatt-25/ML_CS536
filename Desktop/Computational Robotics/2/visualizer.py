from file_parse import parse_problem
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from sample import sample


def visualize(c_robot, c_obstacles, start, goal, points=None, lines=None):
    numpy_obstacles = []
    numpy_robot_configs = []

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))

    for robot_config in c_robot:
        numpy_robot_configs.append(np.array(robot_config))

    fig, ax = plt.subplots()

    # Adding the robot in the collection with random colors
    robot_view = PolyCollection(numpy_robot_configs, cmap=matplotlib.cm.jet, edgecolors="none")
    robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
    robot_view.set_color([0.5, 0, 0.5])
    ax.add_collection(robot_view)

    # Creating a collection of obstacles and adding them to the collection
    polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
    # polygonal_obstacles.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
    polygonal_obstacles.set_color([0.68, 0.85, 0.9])
    ax.add_collection(polygonal_obstacles)

    ax.autoscale_view()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Plotting start and end points
    plt.plot(start[0], start[1], 'g.')
    plt.plot(goal[0], goal[1], 'r.')

    if points:
        for point in points:
            plt.plot(point[0], point[1], 'k.')

    if lines:
        for line in lines:
            xs = (line[0][0], line[1][0])
            ys = (line[0][1], line[1][1])
            plt.plot(xs, ys)

    plt.show()


def visualize_problem(c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal)


def visualize_points(points, c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal, points)


def visualize_lines(lines, c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal, lines=lines)


if __name__ == '__main__':
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot, obstacles, problems = parse_problem(world, problem)
    robot.set_pose((problems[0][0][0], problems[0][0][1], 0))
    initial = robot.transform()
    # initial = robot.translated_robot
    # print(initial)
    robot.set_pose((problems[0][1][0], problems[0][1][1], 1.8))
    final = robot.transform()
    # final = robot.translated_robot
    # print(final)

    n = 5
    points = []
    for _ in range(5):
        points.append(sample())
    # visualize_problem([initial, final], obstacles, problems[0][0], problems[0][1])
    visualize_points(points, [initial, final], obstacles, problems[0][0], problems[0][1])
