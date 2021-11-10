from file_parse import parse_problem
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import cv2

video_writer = cv2.VideoWriter("animation.mp4", cv2.VideoWriter_fourcc(*"avc1"), 1, (600, 600))

def animate(c_robot, path, c_obstacles, start, goal):
    length = len(path)
    numpy_obstacles = []
    fig, ax = plt.subplots()

    for current_obstacle in c_obstacles:
        numpy_obstacles.append(np.array(current_obstacle))

    for path_index in range(length-1):
        start_x1, start_y1, start_theta1 = path[path_index]
        final_x2, final_y2, final_theta2 = path[path_index+1]
        frames = 20
        dx, dy, dz = (final_x2 - start_x1)/frames, (final_y2 - start_y1)/frames, (final_theta2 - start_theta1)/frames

        x1, y1 = start_x1, start_y1

        index=0
        while index < frames:
            index+=1
            x2, y2 = x1 + dx, y1 + dy


            ax.autoscale_view()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)

            rob = c_robot
            rob.set_pose(path[path_index+1])
            robot_coordinates = rob.transform()

            robot_view = PolyCollection(np.array([robot_coordinates]), cmap=matplotlib.cm.jet, edgecolors="none")
            robot_view.set_color([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)])
            robot_view.set_color([0.1, 0, 0.5])
            ax.add_collection(robot_view)

            polygonal_obstacles = PolyCollection(numpy_obstacles, cmap=matplotlib.cm.jet, edgecolors="none")
            polygonal_obstacles.set_color([0.68, 0.85, 0.9])
            ax.add_collection(polygonal_obstacles)

            plt.plot(start[0], start[1], 'g.')
            plt.plot(goal[0], goal[1], 'r.')

            plt.plot((x1, x2), (y1, y2), 'g')
            x1 = x2
            y1 = y2
            plt.savefig("image.png")
            image = cv2.imread("image.png")
            video_writer.write(image)
    plt.show()


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

    # if lines:
    #     for line in lines:
    #         xs = (line[0][0], line[1][0])
    #         ys = (line[0][1], line[1][1])
    #         plt.plot(xs, ys)

    if lines:
        length = len(lines)
        for i in range(length - 1):
            xs = (lines[i][0], lines[i + 1][0])
            ys = (lines[i][1], lines[i + 1][1])
            plt.plot(xs, ys)

    plt.show()
    # plt.savefig("image.jpg")
    # image = cv2.imread("image.jpg")
    # video_writer.write(image)


def visualize_problem(c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal)


def visualize_points(points, c_robot, c_obstacles, start, goal):
    visualize(c_robot, c_obstacles, start, goal, points)


def visualize_path(lines, c_robot, c_obstacles, start, goal):
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
    # for _ in range(5):
    #     points.append(sample())
    # # visualize_problem([initial, final], obstacles, problems[0][0], problems[0][1])
    # visualize_points(points, [initial, final], obstacles, problems[0][0], problems[0][1])
