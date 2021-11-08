def get_robot_global_coordinates(robot_config, x, y):
    rob_at_pt = []
    for idx, pt in enumerate(robot_config):
        if idx == 0:
            rob_at_pt.append((x, y))
        else:
            rob_at_pt.append((round(pt[0] + x - robot_config[0][0], 1), round(pt[1] + y - robot_config[0][1], 1)))
    return rob_at_pt


def on_boundary(p: tuple, q: tuple, r: tuple) -> bool:
    """Check if q lies on the edge pr"""
    if ((q[0] <= max(p[0], r[0])) &
            (q[0] >= min(p[0], r[0])) &
            (q[1] <= max(p[1], r[1])) &
            (q[1] >= min(p[1], r[1]))):
        return True
    return False


def orientation(p: tuple, q: tuple, r: tuple) -> int:
    """Check the orientations. 0 = Collinear"""
    val = (((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1])))
    if val == 0:
        return 0
    if val > 0:
        return 1
    else:
        return 2


def do_intersect(p1, q1, p2, q2):
    """Checking intersection based on orientation of points.
    Reference: http://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf"""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True
    if (o1 == 0) and (on_boundary(p1, p2, q1)):
        return True
    if (o2 == 0) and (on_boundary(p1, q2, q1)):
        return True
    if (o3 == 0) and (on_boundary(p2, p1, q2)):
        return True
    if (o4 == 0) and (on_boundary(p2, q1, q2)):
        return True
    return False


def is_inside_polygon(points: list, p: tuple) -> bool:
    n = len(points)

    ray_end = (11, p[1])
    count = i = 0

    while True:
        j = (i + 1) % n
        if do_intersect(points[i], points[j], p, ray_end):
            if orientation(points[i], p, points[j]) == 0:
                return on_boundary(points[i], p, points[j])
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

    for rc in robot:
        for o in obstacles:
            if is_inside_polygon(o, rc):
                return False
    return True
