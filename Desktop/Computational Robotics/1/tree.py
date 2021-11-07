import collision


class Tree:
    def __init__(self, robot, obstacles, start, goal):
        self.tree = {start: set()}
        self.obstacles = obstacles
        self.robot = robot
        self.goal = goal

    def add(self, point1, point2):
        self.tree[point1].add(point2)
        self.tree[point2] = set()

    def exists(self, point):
        return True if point in self.tree else False

    def parent(self, point):
        for k, v in self.tree.items():
            if point in v:
                return k

    @staticmethod
    def euclidean_dist(p1, p2):
        return (((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5

    def nearest(self, point):
        min_dist = float("inf")
        min_pt = None
        for k in self.tree.keys():
            distance = self.euclidean_dist(k, point)
            if distance < min_dist:
                min_pt = k
                min_dist = distance
        return min_pt

    def extend(self, point1, point2):
        # Discretized version
        len_ab = self.euclidean_dist(point1, point2)
        len_ratio = 0.1 / len_ab
        i = point1
        while True:
            new_x = round((1 - len_ratio) * i[0] + len_ratio * point2[0], 2)
            new_y = round((1 - len_ratio) * i[1] + len_ratio * point2[1], 2)
            if not collision.isCollisionFree(self.robot, (new_x, new_y), self.obstacles):
                break
            i = new_x, new_y
        self.add(point1, i)
