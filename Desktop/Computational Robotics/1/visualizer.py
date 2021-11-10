from file_parse import parse_problem, get_robot_global_coordinates
from sampler import sample
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import cv2

video_writer = cv2.VideoWriter("animation.mp4", cv2.VideoWriter_fourcc(*"avc1"), 25, (640, 480))


def animate(c_robot, path, c_obstacles, start, goal):
    length = len(path)
    numpy_obstacles = []
    fig, ax = plt.subplots()

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))

    i = 0

    for path_index in range(length-1):
        start_x1, start_y1 = path[path_index]
        final_x2, final_y2 = path[path_index+1]
        frames = 20
        dx, dy = (final_x2 - start_x1)/frames, (final_y2 - start_y1)/frames

        x1, y1 = start_x1, start_y1

        index=0
        while index < frames:
            index+=1
            x2, y2 = x1 + dx, y1 + dy


            ax.autoscale_view()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)


            for current_robot in c_robot:
                rob = get_robot_global_coordinates(current_robot, x2, y2)

            robot_view = PolyCollection(np.array([rob]), cmap=matplotlib.cm.jet, edgecolors="none")
            robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
            robot_view.set_color([0.1, 0, 0.5])
            ax.add_collection(robot_view)

            polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
            polygonal_obstacles.set_color([0.68, 0.85, 0.9])
            ax.add_collection(polygonal_obstacles)

            plt.plot(start[0], start[1], 'g.')
            plt.plot(goal[0], goal[1], 'r.')

            # plt.plot((x1, x2), (y1, y2), 'g')
            x1 = x2
            y1 = y2
            plt.savefig(f"image.png")
            image = cv2.imread(f"image.png")
            video_writer.write(image)
    plt.show()


def visualize(c_robot, c_obstacles, start, goal, points=None, lines=None, branches=None):
    numpy_obstacles = []
    numpy_robot = []

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))
    fig, ax = plt.subplots()

    for current_robot in c_robot:
        print(current_robot)
        numpy_robot.append(np.array(current_robot))

    # Adding the robot in the collection with random colors
    robot_view = PolyCollection(numpy_robot, cmap=matplotlib.cm.jet, edgecolors="none")
    robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
    robot_view.set_color([0.5, 0, 0.5])
    ax.add_collection(robot_view)

    # Creating a collection of obstacles and adding them to the collection
    polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
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
        length = len(lines)
        for i in range(length-1):
            xs = (lines[i][0], lines[i+1][0])
            ys = (lines[i][1], lines[i+1][1])
            plt.plot(xs, ys)

    if branches:
        length = len(branches)
        for i in range(length-1):
            xs = (branches[i][0][0], branches[i][1][0])
            ys = (branches[i][0][1], branches[i][1][1])
            plt.plot(xs, ys)

    plt.savefig("image.png")
    plt.show()
    # image = cv2.imread("image.jpg")
    # video_writer.write(image)


def visualize_problem(c_robot, c_obstacles, start, goal):
    numpy_obstacles = []
    numpy_robot = []

    fig, ax = plt.subplots()

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))

    for current_robot in c_robot:
        numpy_robot.append(np.array(current_robot))

    robot_view = PolyCollection(numpy_robot, cmap=matplotlib.cm.jet, edgecolors="none")
    robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
    robot_view.set_color([0.5, 0, 0.5])
    ax.add_collection(robot_view)

    # Creating a collection of obstacles and adding them to the final collection
    polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
    polygonal_obstacles.set_color([0.68, 0.85, 0.9])
    ax.add_collection(polygonal_obstacles)

    ax.autoscale_view()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Plotting start and end points
    plt.plot(start[0], start[1], 'g.')
    plt.plot(goal[0], goal[1], 'r.')

    plt.show()


def visualize_points(points, c_robot, c_obstacles, start, goal):
    numpy_obstacles = []
    numpy_robot = []

    fig, ax = plt.subplots()

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))

    for current_robot in c_robot:
        numpy_robot.append(np.array(current_robot))

    # Adding the robot in the collection with random colors
    robot_view = PolyCollection(numpy_robot, cmap=matplotlib.cm.jet, edgecolors="none")
    robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
    robot_view.set_color([0.5, 0, 0.5])
    ax.add_collection(robot_view)

    # Creating a collection of obstacles and adding them to the collection
    polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
    polygonal_obstacles.set_color([0.68, 0.85, 0.9])
    ax.add_collection(polygonal_obstacles)

    ax.autoscale_view()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Plotting start and end points
    plt.plot(start[0], start[1], 'g.')
    plt.plot(goal[0], goal[1], 'r.')

    for point in points:
        plt.plot(point[0], point[1], 'k.')

    plt.show()


def visualize_lines(lines, c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal, lines=lines)


def visualize_branches(lines, c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal, branches=lines)


if __name__ == '__main__':
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot, obstacles, problems = parse_problem(world, problem)

    # Translate robot to global configuration
    r1 = get_robot_global_coordinates(robot, problems[0][0][0], problems[0][0][1])
    r2 = get_robot_global_coordinates(robot, problems[0][1][0], problems[0][1][1])
    robot_config = [r1, r2]

    # Visualize the problem
    # visualize_problem(robot_config, obstacles, problems[0][0], problems[0][1])

    # Visualize the points + problem
    points = []
    iters = 10
    for i in range(10):
        points.append(sample())
    visualize_points(points, robot_config, obstacles, problems[0][0], problems[0][1])
