import numpy as np
from Question2c2 import DecisionTree
from Question2a import GenerateDataset


def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return 1 - accuracy


data_obj = GenerateDataset()
x_tr, y_tr = data_obj.generate(1000, 10)
x_train = np.array(x_tr)
y_train = np.array(y_tr)
x_te, y_te = data_obj.generate(10000, 10)
x_test, y_test = np.array(x_te), np.array(y_te)

clf = DecisionTree(10)
clf.train(x_train, y_train)

# clf.print_tree(clf.root)

y_pred = clf.predict(x_test)
acc = accuracy(y_test, y_pred)
print("Testing Accuracy", 1 - acc)
print("Testing Error:", acc)

y_train_pred = clf.predict(x_train)
acc1 = accuracy(y_train, y_train_pred)
print("Training Error:", acc1)
