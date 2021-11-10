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
        for x, y in [(-w / 2, -l / 2), (-w / 2, l / 2), (w / 2, l / 2), (w / 2, -l / 2)]:
            new_x = x * np.cos(self.rotation) - y * np.sin(self.rotation) + x_t
            new_y = x * np.sin(self.rotation) + y * np.cos(self.rotation) + y_t
            points.append((new_x, new_y))
        self.translated_robot = points
        return points

    def kinematics(self, state, control):
        q, u = state, control
        return [u[0] * np.cos(q[2] + np.pi / 2.), u[0] * np.sin(q[2] + np.pi / 2.), u[1]]

    def propagate(self, state, controls, durations, dt):
        sequence = [state]
        current_state = state
        length = len(controls)
        for i in range(length):
            kinematics_value = self.kinematics(current_state, controls[i])
            new_state = (round(current_state[0] + kinematics_value[0] * durations[i] * dt, 1), round(current_state[1] \
                + kinematics_value[1] * durations[i] * dt, 1), round(current_state[2] + kinematics_value[2] * \
                                                                     durations[i] * dt, 2))
            sequence.append(new_state)
            current_state = new_state
        return sequence
