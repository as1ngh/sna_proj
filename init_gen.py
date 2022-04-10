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

    # # takes np array of probabilities for each position in init matrix
    # def make_stochastic_custom(self, probability_array):
    #     length = self.num_of_nodes * self.num_of_nodes
    #     if probability_array.shape[0] != length:
    #         raise IOError("Your array must be the length of positions in your initMatrix")
    #     for i in range(self.num_of_nodes):
    #         for j in range(self.num_of_nodes):
    #             for k in range(length):
    #                 self.set_value(probability_array[k], i, j)
    #
    # def make_stochastic_ab(self, alpha, beta, self_loops=True):
    #     # parm check
    #     if not (0.00 <= alpha <= 1.00):
    #         raise IOError("alpha (argument 1) must be a value equal to or between 0 and 1; it is a probability")
    #     if not (0.00 <= beta <= 1.00):
    #         raise IOError("beta (argument 2) must be a value equal to or between 0 and 1; it is a probability")
    #
    #     n = self.get_init_node_count()
    #
    #     # switch 1s and 0s for alpha and beta, keep self loops
    #     for i in range(n):
    #         for j in range(n):
    #             if i == j:
    #                 if not self_loops:
    #                     self.set_value(alpha, i, j)
    #             else:
    #                 if self.get_value(i, j) == 0:
    #                     self.set_value(beta, i, j)
    #                 else:
    #                     self.set_value(alpha, i, j)
    #
    # # takes a nxgraph, Returns initMatrix.
    # @staticmethod
    # def make_from_networkx_graph(nxgraph):
    #     adj_matrix = nx.to_numpy_matrix(nxgraph)
    #
    #     n = adj_matrix.shape[0]  # get num nodes
    #
    #     init = InitMatrix(n)
    #     init.make()
    #     for i in range(n):
    #         for j in range(n):
    #             init.set_value(adj_matrix[i, j], i, j)
    #
    #     return init
    #
    # # takes a nxgraph, alpha, and beta. Returns stochastic initMatrix.
    # def make_stochastic_ab_from_networkx_graph(self, nxgraph, alpha, beta):
    #     init = self.make_from_networkx_graph(nxgraph)
    #     init.make_stochastic_ab(alpha, beta)
    #     return init
    #
    # def add_edge(self, i, j, edge=1):
    #     if edge == 0 or edge == float('inf'):
    #         raise ValueError("Cannot add a zero or infinite edge")
    #
    #     self.W[int(i), int(j)] = edge
    #
    # def add_self_edges(self):
    #     n = self.get_init_node_count()
    #     for i in range(n):
    #         self.add_edge(i, i)
