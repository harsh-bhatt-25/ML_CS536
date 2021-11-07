from file_parse import parse_problem, get_robot_global_coordinates
from sampler import sample
import numpy as np
import copy
import itertools


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_intersection_point(p1, p2, p3, p4):
    p3 = (p3.x, p3.y)
    p4 = (p4.x, p4.y)
    stacked = np.vstack([p1, p2, p3, p4])
    h_stacked = np.hstack((stacked, np.ones((4, 1))))
    line1 = np.cross(h_stacked[0], h_stacked[1])
    line2 = np.cross(h_stacked[2], h_stacked[3])
    x, y, z = np.cross(line1, line2)
    if z == 0:
        return float('inf'), float('inf')
    return x / z, y / z


def check_collinearity(point1, point2, point3):
    if ((point2.x <= max(point1.x, point3.x)) and (point2.x >= min(point1.x, point3.x)) and
            (point2.y <= max(point1.y, point3.y)) and (point2.y >= min(point1.y, point3.y))):
        return True
    return False


def check_orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        return 1
    elif val < 0:
        return 2
    else:
        return 0


def do_segments_intersect(p1, q1, p2, q2):
    orientation1 = check_orientation(p1, q1, p2)
    orientation2 = check_orientation(p1, q1, q2)
    orientation3 = check_orientation(p2, q2, p1)
    orientation4 = check_orientation(p2, q2, q1)

    if (orientation1 != orientation2) and (orientation3 != orientation4):
        return True

    if (orientation1 == 0) and check_collinearity(p1, p2, q1):
        return True

    if (orientation2 == 0) and check_collinearity(p1, q2, q1):
        return True

    if (orientation3 == 0) and check_collinearity(p2, p1, q2):
        return True

    if (orientation4 == 0) and check_collinearity(p2, q1, q2):
        return True

    return False


# def isCollisionFree(robot_config, point, obs):
#     x, y = point
#     # convert robot coordinates to world coordinates and translate to "point"
#     origin = robot_config[0]
#     rob_at_pt = []
#     for idx, pt in enumerate(robot_config):
#         if idx == 0:
#             rob_at_pt.append((x, y))
#         else:
#             rob_at_pt.append((round(pt[0] + x - origin[0], 1), round(pt[1] + y - origin[1], 1)))
#     for x, y in rob_at_pt:
#         if x > 10 or y > 10 or x < 0 or y < 0:
#             return False
#
#     rob = [(Point(a[0], a[1]), Point(b[0], b[1])) for idx, a in enumerate(rob_at_pt) for b in rob_at_pt[idx + 1:]]
#     for obstacle in obs:
#         obs = [(Point(a[0], a[1]), Point(b[0], b[1])) for idx, a in enumerate(obstacle) for b in obstacle[idx + 1:]]
#         for i in range(0, len(rob)):
#             for j in range(0, len(obs)):
#                 if do_segments_intersect(rob[i][0], rob[i][1], obs[j][0], obs[j][1]):
#                     return False
#     return True


def is_inside_polygon(points, p):
    n = len(points)

    # There must be at least 3 vertices
    # in polygon
    if n < 3:
        return False

    # Create a point for line segment
    # from p to infinite
    extreme = Point(11, p[1])
    count = i = 0
    p = Point(p[0], p[1])
    while True:
        next = (i + 1) % n

        # Check if the line segment from 'p' to
        # 'extreme' intersects with the line
        # segment from 'polygon[i]' to 'polygon[next]'
        p1 = Point(points[i][0], points[i][1])
        p2 = Point(points[next][0], points[next][1])
        if do_segments_intersect(p1, p2, p, extreme):

            # If the point 'p' is collinear with line
            # segment 'i-next', then check if it lies
            # on segment. If it lies, return true, otherwise false
            if check_orientation(p1, p, p2) == 0:
                return check_collinearity(p1, p, p2)

            count += 1

        i = next

        if (i == 0):
            break

    # Return true if count is odd, false otherwise
    return (count % 2 == 1)


def isCollisionFree(robot, point, obstacles):
    x, y = point
    # convert robot coordinates to world coordinates and translate to "point"
    origin = robot[0]
    rob_at_pt = []
    for idx, pt in enumerate(robot):
        if idx == 0:
            rob_at_pt.append((x, y))
        else:
            rob_at_pt.append((round(pt[0] + x - origin[0], 1), round(pt[1] + y - origin[1], 1)))

    # check for intersection
    # rob = [(Point(a[0],a[1]), Point(b[0],b[1])) for idx, a in enumerate(rob_at_pt) for b in rob_at_pt[idx + 1:]]
    # for obstacle in obstacles:
    # 	obs = [(Point(a[0],a[1]), Point(b[0],b[1])) for idx, a in enumerate(obstacle) for b in obstacle[idx + 1:]]
    # 	for i in range(0, len(rob)):
    # 		for j in range(0, len(obs)):
    # 			if doIntersect(rob[i][0], rob[i][1], obs[j][0], obs[j][1]):
    # 				return False
    rob = [((a[0], a[1]), (b[0], b[1])) for idx, a in enumerate(rob_at_pt) for b in rob_at_pt[idx + 1:]]
    for obstacle in obstacles:
        obs = [((a[0], a[1]), (b[0], b[1])) for idx, a in enumerate(obstacle) for b in obstacle[idx + 1:]]
        for i in range(0, len(rob)):
            for j in range(0, len(obs)):
                p1 = Point(rob[i][0][0], rob[i][0][1])
                p2 = Point(rob[i][1][0], rob[i][1][1])
                p3 = Point(obs[j][0][0], obs[j][0][1])
                p4 = Point(obs[j][1][0], obs[j][1][1])
                # if do_segments_intersect(rob[i][0], rob[i][1], obs[j][0], obs[j][1]):
                if do_segments_intersect(p1, p2, p3, p4):
                    return False

    # check if inside
    for obstacle in obstacles:
        for pt in rob_at_pt:
            if pt[0] > 10 or pt[1] > 10 or pt[0] < 0 or pt[1] < 0:
                return False
            if is_inside_polygon(points=obstacle, p=pt):
                return False
    return True


'''
Original function free
'''
# def isCollisionFree(robot_config, point, obstacle):
#     # x, y = point
#     # # convert robot coordinates to world coordinates and translate to "point"
#     # origin = robot_config[0]
#     # rob_at_pt = []
#     # for idx, pt in enumerate(robot_config):
#     #     if idx == 0:
#     #         rob_at_pt.append((x, y))
#     #     else:
#     #         rob_at_pt.append((round(pt[0] + x - origin[0], 1), round(pt[1] + y - origin[1], 1)))
#
#     robot_config = get_robot_global_coordinates(robot_config, point[0], point[1])
#     for x, y in robot_config:
#         if x > 10 or y > 10 or x < 0 or y < 0:
#             return False
#     # for current_node in robot_config:
#     #     # print(current_node)
#     #     if 0 < current_node[0] + point[0] < 10 and 0 < current_node[1] + point[1] < 10:
#     #         pass
#     #     else:
#     #         return False
#     # return check_collision_new(robot_config, point, obstacle)
#     return check_collision_new(robot_config, obstacle)


def check_single_obstacle(obstacle, robot_point):
    maximum = 11
    line = Point(maximum, robot_point[1])
    count = i = 0
    length = len(obstacle)
    robot_point = Point(robot_point[0], robot_point[1])
    while True:
        next = (i + 1) % length
        ob1 = Point(obstacle[i][0], obstacle[i][1])
        ob2 = Point(obstacle[next][0], obstacle[next][1])
        if do_segments_intersect(ob1, ob2, robot_point, line):
            if check_orientation(ob1, robot_point, ob2) == 0:
                return check_collinearity(ob1, robot_point, ob2)

            count += 1

        i = next

        if i == 0:
            break

        # Return true if count is odd, false otherwise
    return count % 2 == 1


def check_collision_new(robot_config, obstacle):
    for current_obstacle in obstacle:
        for rob in robot_config:
            c = check_single_obstacle(current_obstacle, rob)
            print(c)
            if not c:
                return False
    return True

# def check_collision_new(robot_config, obstacle):
#     # vertices = len(obstacle)
#     # maximum = 11
#     # if vertices < 3:
#     #     return True
#     # line = (maximum, robot_config[0][1])
#     # count = i = 0
#     # while True:
#     #     next = (i + 1) % vertices
#     #     if do_segments_intersect(obstacle[i], obstacle[next], robot_config, line):
#     #         if check_orientation(obstacle[i], robot_config, obstacle[next]) == 0:
#     #             return check_collinearity(obstacle[i], robot_config, obstacle[next])
#     #
#     #         count += 1
#     maximum = 11
#     # if vertices < 3:
#     #     return True
#     line = Point(maximum, robot_config[0][1])
#     count = i = 0
#     for current_obstacle in obstacle:
#         vertices = len(current_obstacle)
#         # while True:
#         next = (i + 1) % vertices
#         for rob in robot_config:
#             ob1 = Point(current_obstacle[i][0], current_obstacle[i][1])
#             ob2 = Point(current_obstacle[next][0], current_obstacle[next][1])
#             rb1 = Point(rob[0], rob[1])
#             print(ob1.x, ob1.y, ob2.x, ob2.y, rb1.x, rb1.y, line.x, line.y)
#             if do_segments_intersect(ob1, ob2, rb1, line):
#                 print("---------------------------------------")
#                 # if check_orientation(ob1, rb1, ob2) == 0:
#                 #     if not check_collinearity(ob1, rb1, ob2):
#                 #         return False
#
#                 count += 1
#
#             i = next
#
#             if i == 0:
#                 break
#         # if not count % 2 == 1:
#         #     print("True")
#         # else:
#         #     print("--------------------------------------------------------------------------------")
#     return not count % 2 == 1


def check_collision(robo, obs, return_points=False):
    robot_config = copy.deepcopy(robo)
    obstacle = copy.deepcopy(obs)
    len_robot = len(robot_config)
    # Adding one more point to loop properly
    robot_config.append(robot_config[0])
    world_points = [Point(0, 0), Point(0, 10), Point(10, 10), Point(10, 0), Point(0, 0)]

    # For every obstacle, check each segment with the robot segment
    for current_obstacle in obstacle:
        len_current_obstacle = len(current_obstacle)
        current_obstacle.append(current_obstacle[0])
        for i in range(len_current_obstacle):
            for j in range(len_robot):
                p1 = Point(current_obstacle[i][0], current_obstacle[i][1])
                p2 = Point(current_obstacle[i + 1][0], current_obstacle[i + 1][1])
                p3 = Point(robot_config[j][0], robot_config[j][1])
                p4 = Point(robot_config[j + 1][0], robot_config[j + 1][1])
                if do_segments_intersect(p1, p2, p3, p4):
                    print("-----------------------------------------------------------------")
                    print("False")
                    print(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y)
                    return False
                else:
                    print("True")
                    print(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y)

    # for i in range(len(world_points) - 1):
    #     for j in range(len_robot):
    #         p1 = world_points[i]
    #         p2 = world_points[i + 1]
    #         p3 = Point(robot_config[j][0], robot_config[j][1])
    #         p4 = Point(robot_config[j + 1][0], robot_config[j + 1][1])
    #         if do_segments_intersect(p1, p2, p3, p4):
    #             if not return_points:
    #                 return False
    #             else:
    #                 return p1, p2

    return True


if __name__ == "__main__":
    world = "world_definition_files/robot_env_01.txt"
    problem = "problem_definition_files/probs_01.txt"
    robot, obstacles, problems = parse_problem(world, problem)
    sample_point = sample()
    # sample_point = (0, 0)
    print(isCollisionFree(robot, sample_point, obstacles))
