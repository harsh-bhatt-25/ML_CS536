import numpy as np
from Question1b import DecisionTree
from Question1a import GenerateDataset


def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return 1 - accuracy


data_obj = GenerateDataset(4)
x_tr, y_tr = data_obj.generate(30, 4)
x_train = np.array(x_tr)
y_train = np.array(y_tr)
x_te, y_te = data_obj.generate(100, 4)
x_test, y_test = np.array(x_te), np.array(y_te)


clf = DecisionTree()
clf.train(x_train, y_train)

clf.print_tree(clf.root)

y_pred = clf.predict(x_test)
acc = accuracy(y_test, y_pred)
print("Testing Accuracy", 1-acc)
print("Testing Error:", acc)

y_train_pred = clf.predict(x_train)
acc1 = accuracy(y_train, y_train_pred)
print("Training Error:", acc1)
