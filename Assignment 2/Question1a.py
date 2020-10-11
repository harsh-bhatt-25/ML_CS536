from random import choices
import numpy as np


class GenerateDataset:

    def __init__(self, k):
        self.weights, self.y_array, self.x_array = [], [], []
        # Generate Weights
        weight_sum = 0
        for i in range(2, k + 1):
            weight_sum += 0.9 ** i

        for i in range(2, k + 1):
            wi = (0.9 ** i) / weight_sum
            self.weights.append(wi)

    def generate_y_values(self, x_values, k):
        check_sum = 0
        y = -1
        for i in range(1, k):
            check_sum += self.weights[i - 1] * x_values[i]
        if check_sum >= 0.5:
            y = x_values[0]
        else:
            y = 1 - x_values[0]
        return y

    def generate_data_points(self, k):
        x_values = [choices([0, 1], [0.5, 0.5])[0]]

        for i in range(1, k):
            x_values.append(choices([x_values[i - 1], (1 - x_values[i - 1])], [0.75, 0.25])[0])
        y_value = self.generate_y_values(x_values, k)
        self.y_array.append(y_value)
        self.x_array.append(x_values)
        # return [x_values, y_value]

    def generate(self, m, k):
        for i in range(m):
            self.generate_data_points(k)
        return np.array(self.x_array), np.array(self.y_array)

# obj = GenerateDataset()
# obj.generate(9)
# print(data_array)
