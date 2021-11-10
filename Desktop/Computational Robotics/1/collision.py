from file_parse import get_robot_global_coordinates


def check_collinearity(point1, point2, point3):
    if ((point2[0] <= max(point1[0], point3[0])) and (point2[0] >= min(point1[0], point3[0])) and
            (point2[1] <= max(point1[1], point3[1])) and (point2[1] >= min(point1[1], point3[1]))):
        return True
    return False


def check_orientation(p, q, r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
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


def is_inside_polygon(points: list, p: tuple) -> bool:
    n = len(points)

    ray_end = (11, p[1])
    count = i = 0

    while True:
        j = (i + 1) % n
        if do_segments_intersect(points[i], points[j], p, ray_end):
            if check_orientation(points[i], p, points[j]) == 0:
                return check_collinearity(points[i], p, points[j])
            count += 1
        i = j
        if i == 0:
            break

    return count % 2 == 1


def isCollisionFree(robot_coords, point, obstacles):
    robot = get_robot_global_coordinates(robot_coords, point[0], point[1])

    for x, y in robot:
        if x > 10 or y > 10 or x < 0 or y < 0:
            return False

    for robot_segment in robot:
        for current_obstacle in obstacles:
            if is_inside_polygon(current_obstacle, robot_segment):
                return False
    return True
