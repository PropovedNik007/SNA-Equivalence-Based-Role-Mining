import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def find_structural_equivalent_nodes(graph):
    structural_equivalent = []
    nodes = list(graph.nodes())
    while nodes:
        node = nodes[0]
        equivalent = [node]
        neighbors = set(graph.neighbors(node))
        nodes.remove(node)
        i = 0
        while i < len(equivalent):
            curr_node = equivalent[i]
            for n in nodes[:]:
                if neighbors == set(graph.neighbors(n)):
                    equivalent.append(n)
                    nodes.remove(n)
            i += 1
        if len(equivalent) > 1:
            structural_equivalent.append(equivalent)
    return structural_equivalent


def find_common_neighbor_equivalent_nodes(graph):
    common_neighbor_equivalent = []
    nodes = list(graph.nodes())
    while nodes:
        node = nodes[0]
        equivalent = [node]
        neighbors = set(graph.neighbors(node))
        nodes.remove(node)
        i = 0
        while i < len(equivalent):
            curr_node = equivalent[i]
            curr_neighbors = set(graph.neighbors(curr_node))
            for n in nodes[:]:
                if len(curr_neighbors.intersection(set(graph.neighbors(n)))) == len(neighbors):
                    equivalent.append(n)
                    nodes.remove(n)
            i += 1
        if len(equivalent) > 1:
            common_neighbor_equivalent.append(equivalent)
    return common_neighbor_equivalent


def find_edge_equivalent_nodes(graph):
    edge_equivalent = []
    edges = list(graph.edges())
    while edges:
        edge = edges[0]
        equivalent = [edge]
        nodes = set(edge)
        edges.remove(edge)
        i = 0
        while i < len(equivalent):
            curr_edge = equivalent[i]
            for e in edges[:]:
                if set(e).intersection(nodes) == nodes:
                    equivalent.append(e)
                    nodes.update(e)
                    edges.remove(e)
            i += 1
        if len(equivalent) > 1:
            edge_equivalent.append(equivalent)
    return edge_equivalent


def find_jaccard_equivalent_nodes(graph, threshold=0.5):
    equivalent_nodes = []
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for group in equivalent_nodes:
            representative_node = group[0]
            group_neighbors = set(graph.neighbors(representative_node))
            similarity = len(neighbors.intersection(group_neighbors)) / len(neighbors.union(group_neighbors))
            if similarity >= threshold:
                group.append(node)
                break
        else:
            equivalent_nodes.append([node])

    return equivalent_nodes


def find_katz_equivalent_nodes(graph, threshold=0.5):
    katz_centralities = nx.katz_centrality(graph)

    equivalent_nodes = []
    for node, katz_cent in katz_centralities.items():
        for group in equivalent_nodes:
            representative_node = group[0]
            if abs(katz_cent - katz_centralities[representative_node]) <= threshold:
                group.append(node)
                break
        else:
            equivalent_nodes.append([node])


def equivalence_pipeline(graph):
    equivalence_functions = [
        find_structural_equivalent_nodes,
        find_common_neighbor_equivalent_nodes,
        find_edge_equivalent_nodes,
        find_jaccard_equivalent_nodes,
        find_katz_equivalent_nodes
    ]

    all_groups = []

    for func in equivalence_functions:
        equivalent_nodes = func(graph)
        all_groups.extend(equivalent_nodes)

    num_groups = len(all_groups)

    new_colors = plt.cm.tab10.colors + plt.cm.Set3.colors + plt.cm.Paired.colors
    new_colors = new_colors[:num_groups]
    new_colormap = mcolors.ListedColormap(new_colors)

    for func in equivalence_functions:
        equivalent_nodes = func(graph)

        color_map = {}
        for i, nodes in enumerate(equivalent_nodes):
            for node in nodes:
                color_map[node] = i

        default_color = len(equivalent_nodes)
        for node in graph.nodes():
            if node not in color_map:
                color_map[node] = default_color

        pos = nx.spring_layout(graph, seed=23768)

        plt.figure(figsize=(42, 42))
        node_colors = [color_map[node] for node in graph.nodes()]
        nx.draw(graph, pos, node_color=node_colors, with_labels=False, cmap=new_colormap)
        plt.show()
