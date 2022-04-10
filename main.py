import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import kron_gen
import init_gen


def compare(a):
    if a < 9000000:
        return a + 10000000
    return a

def get_graph(nxgraph):
    x = nxgraph
    cc_conn = nx.connected_components(x)
    num_cc = nx.number_connected_components(x)
    # largest_cc = len(cc_conn[0])

    return x, cc_conn, num_cc  # , largest_cc

def create_graph_stats(nxgraph):
    (x, cc_conn, num_cc) = get_graph(nxgraph)  # , largest_cc
    cc = nx.closeness_centrality(x)
    bc = nx.betweenness_centrality(x)
    deg = nx.degree_centrality(x)
    dens = nx.density(x)

    stats = {'cc': cc, 'bc': bc, 'deg': deg, \
             'num_cc': num_cc, 'dens': dens}  # , 'largest_cc':largest_cc}

    return stats  # conn,

def get_top_graph(G, all_node_order, k):
    k = int(k)
    real_G = nx.Graph()
    for x in all_node_order[:k]:
        for y in G.neighbors(x):
            if compare(x)>compare(y):
                real_G.add_edge(x, y)
    return real_G


G = nx.read_edgelist("./dataset/Cit-hepTh.txt", create_using=nx.DiGraph(), nodetype=int)

nodes_dates = {}
with open('./dataset/Cit-HepTh-dates.txt', 'r') as data:
    x = []
    y = []
    for line in data:
        p = line.split()
        nodes_dates[int(p[0])] = p[1]

all_node_order = list(G.nodes()).copy()
all_node_order = sorted(all_node_order, key=lambda x: compare(x))

# get init matrix from kron-fit algorithm
nodes = 2
init = init_gen.InitMatrix(nodes)
init.make()
init.setValue(0.957, 0, 0)
init.setValue(0.564, 0, 1)
init.setValue( 0.657, 1, 0)
init.setValue(0.037, 1, 1)

det_init = init_gen.InitMatrix(nodes)
det_init.make()
det_init.setValue(1, 0, 0)
det_init.setValue(1, 1, 0)
det_init.setValue(1, 0, 1)
det_init.setValue(0, 1, 1)



for k in range(1, 14):
    real_G = get_top_graph(G, all_node_order, math.pow(nodes, k))
    det_G = kron_gen.generateDeterministicKron(init, k)
    stoc_G = kron_gen.generateStochasticKron(init, k)

    print(create_graph_stats(real_G))
    print(create_graph_stats(det_G))
    print(create_graph_stats(stoc_G))









