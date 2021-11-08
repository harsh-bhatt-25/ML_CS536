import random
import math


def sample():
    return [round(random.uniform(0, 10), 1), round(random.uniform(0, 10), 1), math.radians(round(random.uniform(0, 360), 0))]


if __name__ == '__main__':
    numbers = []
    n_points = 5
    for i in range(n_points):
        numbers.append(sample())

    print(numbers)
