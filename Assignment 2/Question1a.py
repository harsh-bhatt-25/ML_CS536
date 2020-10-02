import numpy as np
from random import choices

data_array = []
m, k = 1, 10


def generate_data_points(k):
    array = []
    array.append(choices([0, 1], [0.5, 0.5])[0])
    print(array)
    for i in range(1,k):
        array.append(choices([array[i-1], (1-array[i-1])], [0.75, 0.25])[0])
    print(array)


for i in range(m):
    data_array.append(generate_data_points(k))
