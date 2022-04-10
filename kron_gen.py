import numpy as np
import networkx as nx
import math
import random


# returns networkx graph created from np array
def convert(np_array):
    return nx.to_networkx_graph(np_array)


# used to take away self loops in final graph for stat purposes
def delete_self_loops(graph, node_count):
    node_count = int(node_count)
    for i in range(node_count):
        graph[i, i] = 0
    return graph


def generate_stochastic_kron_graph(initiator_matrix, k, delete_self_loops_for_stats=False, directed=False,
                                   custom_edges=False,
                                   edges=0):
    init_n = initiator_matrix.get_init_node_count()
    n_nodes = math.pow(init_n, k)
    matrix_dimension = initiator_matrix.get_init_node_count()
    matrix_sum = initiator_matrix.get_matrix_sum()
    if custom_edges:
        n_edges = edges
        if n_edges > (n_nodes * n_nodes):
            raise ValueError("More edges than possible with number of Nodes")
    else:
        n_edges = math.pow(matrix_sum, k)  # get number of predicted edges
    collisions = 0

    print("Matrix sum:", matrix_sum)
    print("Edges: ", n_edges)
    print("Nodes: ", n_nodes)

    # create vector for recursive matrix probability
    recursive_mtx_probability = []
    cumulative_probability = 0.0
    for i in range(matrix_dimension):
        for j in range(matrix_dimension):
            prob = initiator_matrix.get_value(i, j)
            if prob > 0.0:
                cumulative_probability += prob
                recursive_mtx_probability.append((cumulative_probability / matrix_sum, i, j))

    # add Nodes
    final_graph = np.zeros((int(n_nodes), int(n_nodes)))
    # add Edges
    e = 0
    # print n_edges #testing
    while e < n_edges:
        rng = n_nodes
        row = 0
        col = 0
        for t in range(k):
            prob = random.uniform(0, 1)
            # print "prob:" #testing
            # print prob #testing
            n = 0
            while prob > recursive_mtx_probability[n][0]:
                n += 1
            mrow = recursive_mtx_probability[n][1]
            mcol = recursive_mtx_probability[n][2]
            rng /= matrix_dimension
            row += mrow * rng
            col += mcol * rng
        if final_graph[int(row)][int(col)] == 0:  # if there is no edge
            final_graph[int(row)][int(col)] = 1
            e += 1
            if not directed:  # symmetry if not directed
                if row != col:
                    final_graph[int(col)][int(row)] = 1
                    e += 1
        else:
            collisions += 1
    print("Collisions: ", collisions)
    # delete self loops if needed for stats
    if delete_self_loops_for_stats:
        final_graph = delete_self_loops(final_graph, n_nodes)
    final_graph = convert(final_graph)
    return final_graph, collisions


def generate_deterministic_kron_graph(initiator_matrix, k):
    final_graph = np.copy(initiator_matrix.W)
    curr = 1
    while curr < k:
        curr = curr + 1
        final_graph = np.kron(final_graph, initiator_matrix.W)
    final_graph = convert(final_graph)
    return final_graph
