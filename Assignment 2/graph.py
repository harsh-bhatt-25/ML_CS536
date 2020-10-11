import matplotlib.pyplot as plt


def graph(x, y):
    plt.scatter(x, y, label="Hello", color="red")
    plt.xlabel("m values")
    plt.ylabel(" $|err_{test} - err_{train}|$")
    plt.title("ID3")
    plt.legend()
    plt.show()
