import matplotlib.pyplot as plt
import numpy as np

n, L = 100, 10

LcapMOM, LcapMLE, MSEmom, MSEmle, x_points = [], [], [], [], []

for j in range(1000):
    rand_points = np.random.uniform(0, L, n)
    mom = 2 * (np.sum(rand_points) / n)
    mle = np.max(rand_points)

    LcapMOM.append(mom)
    LcapMLE.append(mle)

    MSEmom.append(mom ** 2 / (3 * n))
    MSEmle.append((2 * (mle ** 2)) / ((n + 1) * (n + 2)))
    x_points.append(j)

figure, ((graph1, graph2), (graph3, graph4)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
graph1.scatter(x=np.asarray(x_points), y=LcapMOM, marker='o', c='r', edgecolor='r')
graph1.set_title("Method of Moments")
graph1.set_xlabel("$n$")
graph1.set_ylabel(r"$\^{L}_{MOM}$")

graph2.scatter(x=np.asarray(x_points), y=MSEmom, marker='o', c='r', edgecolor='r')
graph2.set_title("Method of Moments")
graph2.set_xlabel("$n$")
graph2.set_ylabel(r"$MSE(\^{L}_{MOM})$")

graph3.scatter(x=np.asarray(x_points), y=LcapMLE, marker='o', c='b', edgecolor='b')
graph3.set_title("Maximum Likelihood Estimation")
graph3.set_xlabel("$n$")
graph3.set_ylabel(r"$\^{L}_{MLE}$")

graph4.scatter(x=np.asarray(x_points), y=MSEmle, marker='o', c='b', edgecolor='b')
graph4.set_title("Maximum Likelihood Estimation")
graph4.set_xlabel("$n$")
graph4.set_ylabel(r"$MSE(\^{L}_{MLE})$")

# print(LcapMOM)
# print(LcapMLE)
# print(MSEmom)
# print(MSEmle)
# print(sum(MSEmom) / 1000)
# print(sum(MSEmle) / 1000)
# plt.savefig("graphs.png")
plt.show()
