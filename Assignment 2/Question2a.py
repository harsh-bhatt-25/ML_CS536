from random import choices
from collections import Counter

data_array = []
m, k = 1, 20


class GenerateDataset():

    def generate_y_values(self, x_values):
        if x_values[0] == 0:
            y = Counter(x_values[1:8]).most_common()[0][0]
        else:
            y = Counter(x_values[8:15]).most_common()[0][0]
        return y

    def generate_data_points(self, k):
        x_values = [choices([0, 1], [0.5, 0.5])[0]]

        for i in range(1, 15):
            x_values.append(choices([x_values[i - 1], (1 - x_values[i - 1])], [0.75, 0.25])[0])
        for i in range(15, k + 1):
            x_values.append(choices([1, 0], [0.5, 0.5])[0])
        y_value = self.generate_y_values(x_values)
        return [x_values, y_value]

    def generate(self, m):
        for i in range(m):
            data_array.append(self.generate_data_points(k))


obj = GenerateDataset()
obj.generate(m)
print(data_array)
