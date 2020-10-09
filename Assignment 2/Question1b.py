import numpy as np


class Node:
    def __init__(self, feature=None, value=None, left=None, right=None, *, label_name=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.label_name = label_name
        

class DecisionTree:
    def __init__(self):
        self.root = None

    def train(self, x_array, y):
        self.root = self.tree(x_array, y)

    def tree(self, x_array, y):
        n_samples, n_features = x_array.shape
        left_indices, right_indices = [], []
        n_labels = len(set(y))
        if n_labels == 1:
            label_name = y[0]
            return Node(label_name = label_name)

        indexes = [i for i in range(n_features)]

        feature_index, feature_value = self.get_split_values(x_array, y, indexes)
        x_column = x_array[:, feature_index]
        len_x_column = len(x_column)
        for i in range(len_x_column):
            if x_column[i] <= feature_value:
                left_indices.append(i)
            else:
                right_indices.append(i)

        left_split, right_split = np.array(left_indices), np.array(right_indices)
        left_node = self.tree(x_array[left_split, :], y[left_split])
        right_node = self.tree(x_array[right_split, :], y[right_split])
        return Node(feature_index, feature_value, left_node, right_node)

    def get_split_values(self, x_array, y, indexes):
        best_gain, split_index, split_value = -1, None, None
        for column in indexes:
            X_column = x_array[:, column]
            values = np.array([0, 1])
            for value in values:
                gain = self.information_gain(X_column, y, value)
                if gain > best_gain:
                    best_gain = gain
                    split_index = column
                    split_value = value

        return split_index, split_value

    def information_gain(self, X_column, y, split_value):
        H_Y = self.H(y)

        left_indices, right_indices = [], []
        length = len(X_column)
        for i in range(length):
            if X_column[i] <= split_value:
                left_indices.append(i)
            else:
                right_indices.append(i)

        if len(left_indices) == 0 or len(right_indices) == 0:
            return 0

        n = len(y)
        n_l, n_r = len(left_indices), len(right_indices)
        e_l, e_r = self.H(y[left_indices]), self.H(y[right_indices])
        H_Y_X = (n_l / n) * e_l + (n_r / n) * e_r
        IG = H_Y - H_Y_X
        return IG

    def H(self, y):
        counts = np.bincount(y)
        length_y = len(y)
        ps = np.array([i / length_y for i in counts])
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def predict(self, x_array):
        return np.array([self.tree_traverse(x, self.root) for x in x_array])

    def tree_traverse(self, x, node):
        if node.label_name is not None:
            return node.label_name

        if x[node.feature] <= node.value:
            return self.tree_traverse(x, node.left)
        return self.tree_traverse(x, node.right)
