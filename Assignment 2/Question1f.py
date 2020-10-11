import numpy as np


class Node:
    def __init__(self, feature=None, value=None, *, left=None, right=None, label_name=None, entropy=None, samples=None,
                 counts=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.label_name = label_name
        self.entropy = entropy
        self.samples = samples
        self.counts = counts


class DecisionTree:
    flag = "a"

    def __init__(self):
        self.root = None

    def train(self, x_array, y):
        _, features = x_array.shape
        indices = [i for i in range(features)]
        self.root = self.tree(x_array, y, indices)

    def tree(self, x_array, y, feature_indices):
        left_indices, right_indices = [], []
        len_labels = len(set(y))
        if len_labels == 1:
            label_name = y[0]
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
        left_node = self.tree(x_array[np.array(left_indices), :], y[np.array(left_indices)], indexes)
        right_node = self.tree(x_array[np.array(right_indices), :], y[np.array(right_indices)], indexes)
        return Node(feature_index, feature_value, left=left_node, right=right_node, entropy=entropy,
                    samples=len(y), counts=np.bincount(y))

    def max_counter(self, y):
        counts = np.bincount(y)
        length = len(counts)
        max_count, max_value = -1, -1
        for i in range(length):
            if counts[i] > max_count:
                max_value = i
        return max_value

    def get_split_index(self, x_array, y, indexes, unique_y):
        best_gain, split_index, split_value = 0, None, None
        for column in indexes:
            X_column = x_array[:, column]
            left, right = np.array([]), np.array([])
            for value in unique_y:
                for i in range(len(X_column)):
                    if X_column[i] == value:
                        np.append(left, i)
                    else:
                        np.append(right, i)

                if len(left) == 0 or len(right) == 0:
                    continue

                gain = self.information_gain(left, right)
                if gain < best_gain:
                    best_gain = gain
                    split_index = column
                    split_value = value

        return split_index, best_gain, split_value

    def information_gain(self, left, right):
        probability = len(left) / (len(left) + len(right))
        return (probability * self.gini(left)) - ((1-probability) * self.gini(right))

    def gini(self, rows):
        length = len(rows)
        counts = np.bincount(rows)
        impurity = 1
        for i in range(len(counts)):
            prob = counts[i] / length
            impurity -= prob**2
        return impurity

    def predict(self, x_array):
        return np.array([self.tree_traverse(x, self.root) for x in x_array])

    def tree_traverse(self, x, node):
        if node.label_name is not None:
            return node.label_name

        if x[node.feature] == node.value:
            return self.tree_traverse(x, node.left)
        return self.tree_traverse(x, node.right)

    def print_tree(self, root):
        if root.feature is None and root.label_name is None:
            return

        queue = [root, self.flag]

        while True:
            current = queue.pop(0)
            if current != "a":
                if current.label_name is not None:
                    print("Value = {}, Entropy = {}".format(current.label_name, current.entropy, end=" "))
                else:
                    print("Feature = {}, Samples = {}, Counts = {}, Entropy = {}".format(current.feature,
                                                                                         current.samples,
                                                                                         current.counts,
                                                                                         current.entropy, end=" "))
                if current.left is not None:
                    queue.append(current.left)
                if current.right is not None:
                    queue.append(current.right)
            else:
                print("")
                if len(queue) == 0:
                    break
                else:
                    queue.append(self.flag)
