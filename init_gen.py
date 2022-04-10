import numpy as np
import networkx as nx


class InitMatrix:

    def __init__(self, num_of_nodes, matrix=None):
        self.num_of_nodes = num_of_nodes
        self.W = matrix
        # initially we will take in the number of nodes when the object is created

    def get_init_node_count(self):
        return self.num_of_nodes

    def set_init_node_count(self, v):
        self.num_of_nodes = v

    def get_value(self, i, j):
        return self.W[(i, j)]

    def set_value(self, new_value, i, j):
        self.W[(i, j)] = new_value

    def get_matrix_sum(self):
        n = self.get_init_node_count()
        matrix_sum = 0.0
        for i in range(n):
            for j in range(n):
                matrix_sum += self.get_value(i, j)
        return matrix_sum

    # This makes a init matrix manual (user adds edges)
    def make(self):
        n = self.num_of_nodes
        self.W = np.zeros((n, n))
