import numpy as np
import matplotlib.pyplot as plt

m, w, b, sigma_square = 200, 1, 5, 0.1
y_val, x_dash = [], []
w_est, b_est = [], []
w_est_dash, b_est_dash = [], []

x_val = np.random.uniform(100, 102, m)


def get_xdash(x):
    for i in x:
        x_dash.append(i - 101)
    return np.array(x_dash)


def get_y_values(x):
    for i in x:
        epsilon = np.random.normal(0, sigma_square)
        y_val.append((w * i) + b + epsilon)
    return np.array(y_val)


def get_w_est(x, y):
    for i in range(m):
        w_est.append((y[i] - b) / x[i])
    return np.array(w_est)


def get_w_est_dash(x, y):
    for i in range(m):
        w_est_dash.append((y[i] - b) / x[i])
    return np.array(w_est_dash)


def get_b_est(x, y):
    for i in range(m):
        b_est.append(y[i] - (w * x[i]))
    return np.array(b_est)


def get_b_est_dash(x, y):
    for i in range(m):
        b_est_dash.append(y[i] - (w * x[i]))
    return np.array(b_est_dash)


y = get_y_values(x_val)
x_dash = get_xdash(x_val)
w_est = get_w_est(x_val, y)
w_est_dash = get_w_est_dash(x_dash, y)
b_est = get_b_est(x_val, y)
b_est_dash = get_b_est_dash(x_dash, y)
print(w_est_dash)
x_plot = [i + 1 for i in range(m)]
plt.scatter(x_plot, b_est)
plt.show()
plt.scatter(x_plot, b_est_dash)
plt.show()
