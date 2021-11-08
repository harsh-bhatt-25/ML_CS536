import numpy as np

class Robot:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.translation = (0., 0.)
        self.rotation = 0.
        self.translated_robot = None

    def set_pose(self, pose):
        self.translation = (pose[0], pose[1])
        self.rotation = pose[2]

    def transform(self):
        w, l = self.width, self.height
        x_t, y_t = self.translation
        points = []
        for x, y in [(-w/2, -l/2), (-w/2, l/2), (w/2, l/2), (w/2, -l/2)]:
            new_x = x * np.cos(self.rotation) - y * np.sin(self.rotation) + x_t
            new_y = x * np.sin(self.rotation) + y * np.cos(self.rotation) + y_t
            points.append((new_x, new_y))
        self.translated_robot = points
        return points
