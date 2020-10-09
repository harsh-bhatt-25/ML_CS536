import numpy as np
from sklearn.model_selection import train_test_split
from Question1b import DecisionTree
from Question1a import GenerateDataset


def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy


data_obj = GenerateDataset()
x_data, y_data = data_obj.generate(30)
X = np.array(x_data)
y = np.array(y_data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)
# print(X_train.shape)
print(y_train)
# print(X_test)
print(y_test)

clf = DecisionTree()
clf.train(X_train, y_train)

y_pred = clf.predict(X_test)
acc = accuracy(y_test, y_pred)
print(y_pred)
print("Accuracy:", acc)