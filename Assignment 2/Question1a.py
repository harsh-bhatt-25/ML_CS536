import numpy as np
from random import choices

data_array = []
m, k = 1, 10

sum = 0
for i in range(2,k+1):
    sum += 0.9**i

weights = []
for i in range(2,k+1):
    wi = (0.9**i)/sum
    weights.append(wi)
print(weights)


def generate_data_points(k):

    x_values = []

    def generate_y_values():
        check_sum = 0
        y = -1
        for i in range(1,k):
            check_sum += weights[i-1] * x_values[i]
        if check_sum >= 0.5:
            y = x_values[0]
        else:
            y = 1 - x_values[0]
        return y

    x_values.append(choices([0, 1], [0.5, 0.5])[0])
    for i in range(1,k):
        x_values.append(choices([x_values[i-1], (1-x_values[i-1])], [0.75, 0.25])[0])
    y_value = generate_y_values()
    print(x_values, y_value)


for i in range(m):
    data_array.append(generate_data_points(k))
