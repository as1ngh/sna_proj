import networkx as nx
import math
import kron_gen
import init_gen
import os


def compare(a):
    if a < 9000000:
        return a + 10000000
    return a


def get_graph(nxgraph):
    cc_conn = nx.connected_components(nxgraph)
    num_cc = nx.number_connected_components(nxgraph)
    return cc_conn, num_cc


def create_graph_stats(nxgraph):
    cc_conn, num_cc = get_graph(nxgraph)
    cc = nx.closeness_centrality(nxgraph)
    bc = nx.betweenness_centrality(nxgraph)
    deg = nx.degree_centrality(nxgraph)
    dens = nx.density(nxgraph)

    stats = {
        'closeness_centrality': cc,
        'betweenness_centrality': bc,
        'degree_centrality': deg,
        'number_connected_components': num_cc,
        'density': dens
    }

    return stats


def get_top_graph(g, node_order, depth):
    depth = int(depth)
    real_G = nx.Graph()
    for x in node_order[:depth]:
        for y in g.neighbors(x):
            if compare(x) > compare(y):
                real_G.add_edge(x, y)
    return real_G


if __name__ == "__main__":
    working_directory = os.getcwd()
    hepth_path = os.path.join(working_directory, "dataset/Cit-HepTh.txt")
    hepth_dates_path = os.path.join(working_directory, "dataset/Cit-HepTh-dates.txt")

    G = nx.read_edgelist(hepth_path, create_using=nx.DiGraph(), nodetype=int)

    nodes_dates = {}
    with open(hepth_dates_path, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            nodes_dates[int(p[0])] = p[1]

    all_node_order = list(G.nodes()).copy()
    all_node_order = sorted(all_node_order, key=lambda node: compare(node))

    # get init matrix from kron-fit algorithm
    nodes = 2
    init = init_gen.InitMatrix(nodes)
    init.make()
    init.set_value(0.957, 0, 0)
    init.set_value(0.564, 0, 1)
    init.set_value(0.657, 1, 0)
    init.set_value(0.037, 1, 1)

    det_init = init_gen.InitMatrix(nodes)
    det_init.make()
    det_init.set_value(1, 0, 0)
    det_init.set_value(1, 1, 0)
    det_init.set_value(1, 0, 1)
    det_init.set_value(0, 1, 1)

    for k in range(1, 14):
        real_graph = get_top_graph(G, all_node_order, math.pow(nodes, k))
        deterministic_graph = kron_gen.generate_deterministic_kron_graph(det_init, k)
        stochastic_graph = kron_gen.generate_stochastic_kron_graph(init, k)

        print(create_graph_stats(real_graph))
        print(create_graph_stats(deterministic_graph))
        print(create_graph_stats(stochastic_graph))
