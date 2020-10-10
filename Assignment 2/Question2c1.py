import numpy as np


class Node:
    def __init__(self, feature=None, value=None, *, left=None, right=None, label_name=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.label_name = label_name


class DecisionTree:
    flag = "a"

    def __init__(self, max_depth):
        self.root = None
        self.max_depth = max_depth

    def train(self, x_array, y):
        _, features = x_array.shape
        indices = [i for i in range(features)]
        self.root = self.tree(x_array, y, indices)

    def tree(self, x_array, y, feature_indices, depth=0):
        left_indices, right_indices = [], []
        len_labels = len(set(y))
        if len_labels == 1 or depth >= self.max_depth:
            label_name = self.max_counter(y)
            return Node(label_name=label_name)

        if len_labels != 1 and len(feature_indices) == 0:
            value = self.max_counter(y)
            return Node(label_name=value)

        indexes = feature_indices
        feature_index, entropy, feature_value = self.get_split_index(x_array, y, indexes, np.unique(y))
        if entropy == 0:
            value = self.max_counter(y)
            return Node(label_name=value)
        # indexes.remove(feature_index)

        x_column = x_array[:, feature_index]
        len_x_column = len(x_column)
        for i in range(len_x_column):
            if x_column[i] == feature_value:
                left_indices.append(i)
            else:
                right_indices.append(i)

        # left_split, right_split = np.array(left_indices), np.array(right_indices)
        left_node = self.tree(x_array[np.array(left_indices), :], y[np.array(left_indices)], indexes, depth+1)
        right_node = self.tree(x_array[np.array(right_indices), :], y[np.array(right_indices)], indexes, depth+1)
        return Node(feature_index, feature_value, left=left_node, right=right_node)

    def max_counter(self, y):
        counts = np.bincount(y)
        length = len(counts)
        max_count, max_value = -1, -1
        for i in range(length):
            if counts[i] > max_count:
                max_value = i
        return max_value

    def get_split_index(self, x_array, y, indexes, unique_y):
        entropy, split_index, split_value = -1, None, None
        for column in indexes:
            X_column = x_array[:, column]
            for value in unique_y:
                gain = self.information_gain(X_column, y, value)
                if gain > entropy:
                    entropy = gain
                    split_index = column
                    split_value = value

        return split_index, entropy, split_value

    def information_gain(self, X_column, y, split_value):
        H_Y = self.H(y)

        left_indices, right_indices = [], []
        length = len(X_column)
        for i in range(length):
            if X_column[i] == split_value:
                left_indices.append(i)
            else:
                right_indices.append(i)

        if len(left_indices) == 0 or len(right_indices) == 0:
            return 0

        y_length = len(y)
        H_Y_X = 0
        x_values = {len(left_indices): y[left_indices], len(right_indices): y[right_indices]}
        for value in x_values:
            x_probability = value / y_length
            H_Y_X += x_probability * self.H(x_values[value])

        IG = H_Y - H_Y_X
        return IG

    def H(self, y):
        counts = np.bincount(y)
        length_y = len(y)
        probabilities = np.array([i / length_y for i in counts])
        return -np.sum([p * np.log2(p) for p in probabilities if p > 0])

    def predict(self, x_array):
        return np.array([self.tree_traverse(x, self.root) for x in x_array])

    def tree_traverse(self, x, node):
        if node.label_name is not None:
            return node.label_name

        if x[node.feature] == node.value:
            return self.tree_traverse(x, node.left)
        return self.tree_traverse(x, node.right)

