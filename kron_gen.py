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


def generate_stochastic_kron_graph(initiator_matrix, k, delete_self_loops_for_stats=False, directed=False, custom_edges=False,
                                   edges=0):
    initN = initiator_matrix.get_init_node_count()
    nNodes = math.pow(initN, k)  # get final size and make empty 'kroned' matrix
    mtxDim = initiator_matrix.get_init_node_count()
    mtxSum = initiator_matrix.get_matrix_sum()
    if custom_edges:
        nEdges = edges
        if nEdges > (nNodes * nNodes):
            raise ValueError("More edges than possible with number of Nodes")
    else:
        nEdges = math.pow(mtxSum, k)  # get number of predicted edges
    collisions = 0

    print("mtxSum")
    print(mtxSum)
    print("Edges: ")
    print(nEdges)
    print("Nodes: ")
    print(nNodes)
    print("iniMtx")
    print(initiator_matrix)

    # create vector for recursive matrix probability
    probToRCPosV = []
    cumProb = 0.0
    for i in range(mtxDim):
        for j in range(mtxDim):
            prob = initiator_matrix.get_value(i, j)
            if prob > 0.0:
                cumProb += prob
                probToRCPosV.append((cumProb / mtxSum, i, j))
                # print "Prob Vector Value:" #testing
                # print cumProb/mtxSum #testing

    # add Nodes
    finalGraph = np.zeros((int(nNodes), int(nNodes)))
    # add Edges
    e = 0
    # print nEdges #testing
    while e < nEdges:
        rng = nNodes
        row = 0
        col = 0
        for t in range(k):
            prob = random.uniform(0, 1)
            # print "prob:" #testing
            # print prob #testing
            n = 0
            while prob > probToRCPosV[n][0]:
                n += 1
            mrow = probToRCPosV[n][1]
            mcol = probToRCPosV[n][2]
            rng /= mtxDim
            row += mrow * rng
            col += mcol * rng
        if finalGraph[int(row)][int(col)] == 0:  # if there is no edge
            finalGraph[int(row)][int(col)] = 1
            e += 1
            if not directed:  # symmetry if not directed
                if row != col:
                    finalGraph[int(row)][int(col)] = 1
                    e += 1
        else:
            collisions += 1
    print("Collisions: ")
    print(collisions)  # testing
    # delete self loops if needed for stats
    if delete_self_loops_for_stats:
        finalGraph = delete_self_loops(finalGraph, nNodes)
    finalGraph = convert(finalGraph)
    return finalGraph


def generate_deterministic_kron_graph(initiator_matrix, k):
    final_graph = np.copy(initiator_matrix.W)
    curr = 1
    while curr < k:
        curr = curr + 1
        final_graph = np.kron(final_graph, initiator_matrix.W)
    final_graph = convert(final_graph)
    return final_graph

# def generate_stochastic_kron_graph(initiator_matrix, depth, delete_self_loops_for_stats=False, directed=False,
#                                    custom_edges=False, edges=0):
#     init_node_count = initiator_matrix.get_init_node_count()
#     # get final size and make empty matrix
#     node_count = math.pow(init_node_count, depth)
#     matrix_dimensions = initiator_matrix.get_init_node_count()
#     matrix_sum = initiator_matrix.get_matrix_sum()
#
#     if custom_edges:
#         edge_count = edges
#         if edge_count > (node_count * node_count):
#             raise ValueError("More edges than possible with number of Nodes")
#     else:
#         edge_count = math.pow(matrix_sum, depth)  # number of predicted edges
#
#     collisions = 0
#
#     print("Matrix sum:", matrix_sum)
#     print("Edge count: ", edge_count)
#     print("Node count: ", node_count)
#     print("Initiator Matrix:", initiator_matrix)
#
#     # create vector for recursive matrix probability
#     recursive_matrix_probability = list()
#     for i in range(matrix_dimensions):
#         recursive_matrix_probability.append(list())
#     cumulative_probability = 0.0
#     for i in range(matrix_dimensions):
#         for j in range(matrix_dimensions):
#             prob = initiator_matrix.get_value(i, j)
#             if prob > 0.0:
#                 cumulative_probability += prob
#                 recursive_matrix_probability[i].append(cumulative_probability / matrix_sum)
#
#     # add Nodes
#     final_graph = np.zeros((int(node_count), int(node_count)))
#
#     # add Edges
#     e = 0
#     # print edge_count #testing
#     while e < edge_count:
#         rng = node_count
#         row = 0
#         col = 0
#         for t in range(depth):
#             prob = random.uniform(0, 1)
#             mrow = 0
#             mcol = 0
#             for row in range(matrix_dimensions):
#                 for col in range(matrix_dimensions):
#                     if prob < recursive_matrix_probability[row][col]:
#                         break
#             rng /= matrix_dimensions
#             row += mrow * rng
#             col += mcol * rng
#         if final_graph[int(row)][int(col)] == 0:  # if there is no edge
#             final_graph[int(row)][int(col)] = 1
#             e += 1
#             if not directed:  # symmetry if not directed
#                 if row != col:
#                     final_graph[int(col)][int(row)] = 1
#                     e += 1
#         else:
#             collisions += 1
#     print("Collisions: ", collisions)
#
#     # delete self loops if needed for stats
#     if delete_self_loops_for_stats:
#         final_graph = delete_self_loops(final_graph, node_count)
#     final_graph = convert(final_graph)
#     return final_graph
