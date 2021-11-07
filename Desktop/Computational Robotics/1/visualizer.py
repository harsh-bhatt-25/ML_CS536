from file_parse import parse_problem, get_robot_global_coordinates
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
import pylab as pl
from PIL import Image
from PIL import ImageDraw
import random as rnd


# def visualize_problem(c_robot, c_obstacles, start, goal):
#
#     numpy_obstacles = []
#
#     for current_obstacle in c_obstacles:
#         numpy_obstacles.append(np.array(current_obstacle))
#     fig, ax = plt.subplots()
#
#     # Adding the robot in the collection with random colors
#     robot_view = PolyCollection([np.array(c_robot)], cmap=matplotlib.cm.jet, edgecolors="none")
#     robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
#     ax.add_collection(robot_view)
#
#     # Creating a collection of obstacles and adding them to the collection
#     polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
#     polygonal_obstacles.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
#     ax.add_collection(polygonal_obstacles)
#
#     ax.autoscale_view()
#     ax.set_xlim(0, 10)
#     ax.set_ylim(0, 10)
#
#     # Plotting start and end points
#     plt.plot(start[0], start[1], 'go')
#     plt.plot(goal[0], goal[1], 'ro')
#
#     plt.show()

def visualize(c_robot, c_obstacles, start, goal, points=None, lines=None):
    numpy_obstacles = []

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))
    fig, ax = plt.subplots()

    # Adding the robot in the collection with random colors
    robot_view = PolyCollection([np.array(c_robot)], cmap=matplotlib.cm.jet, edgecolors="none")
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

    # Translate robot to global configuration
    qx, qy = 1, 2
    robot = get_robot_global_coordinates(robot, qx, qy)

    visualize_problem(robot, obstacles, problems[0][0], problems[0][1])
    points = [[0.3, 1.4], [8.4, 1.3], [6.6, 4.4], [5.0, 6.7], [5.8, 1.4]]
    visualize_points(points, robot, obstacles, problems[0][0], problems[0][1])
