import numpy as np
from Question1f import DecisionTree
from Question1a import GenerateDataset
from graph import graph

x, y = [], []


def error(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return 1 - accuracy


i = 50
while i < 1000:
    data_obj = GenerateDataset(10)
    x_test, x_train, y_test, y_train = None, None, None, None
    x_train, y_train = data_obj.generate(i, 10)

    new_obj = GenerateDataset(10)
    x_test, y_test = new_obj.generate(20000, 10)

    clf = DecisionTree()
    clf.train(x_train, y_train)

    clf.print_tree(clf.root)

    y_pred = clf.predict(x_test)
    acc = error(y_test, y_pred)
    print("Testing Accuracy", 1 - acc)
    print("Testing Error:", acc)

    y_train_pred = clf.predict(x_train)
    acc1 = error(y_train, y_train_pred)
    print("Training Error:", acc1)

    y.append(acc)
    x.append(i)
    if i < 100:
        i += 10
    else:
        i += 100

graph(x, y)
print(x, y)
