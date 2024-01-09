import numpy as np
import pandas as pd

import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def find_structural_equivalent_groups(G):
    equivalent_groups = []
    nodes_checked = set()

    def are_structurally_equivalent(node1, node2):
        if G.is_directed():
            return set(G.predecessors(node1)) == set(G.predecessors(node2)) and set(G.successors(node1)) == set(G.successors(node2))
        else:
            return set(G.neighbors(node1)) == set(G.neighbors(node2))

    for node1 in G:
        if node1 not in nodes_checked:
            current_group = {node1}
            nodes_checked.add(node1)
            for node2 in set(G) - nodes_checked:
                if are_structurally_equivalent(node1, node2):
                    current_group.add(node2)
                    nodes_checked.add(node2)
            equivalent_groups.append(current_group)

    return equivalent_groups


def find_common_neighbor_equivalent_groups(graph):
    equivalent_groups = []
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
            equivalent_groups.append(equivalent)
    return equivalent_groups

def find_jaccard_equivalent_groups(graph, threshold=0.5):
    equivalent_groups = []
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for group in equivalent_groups:
            representative_node = group[0]
            group_neighbors = set(graph.neighbors(representative_node))
            similarity = len(neighbors.intersection(group_neighbors)) / (len(neighbors.union(group_neighbors)) + 1e-6)
            if similarity >= threshold:
                group.append(node)
                break
        else:
            equivalent_groups.append([node])

    return equivalent_groups

#-------------------Regular Equivalence-------------------#
def find_regular_equivalent_groups(graph):
    equivalent_groups = []  
    visited_nodes = set()

    def neighbors_with_degrees(node):
        neighbors = list(graph.neighbors(node))
        neighbors_degrees = [graph.degree(neighbor) for neighbor in neighbors]
        return zip(neighbors, neighbors_degrees)

    for node in graph.nodes():
        if node not in visited_nodes:
            current_neighbors = set(neighbors_with_degrees(node))

            equivalent_group = [node]

            for other_node in graph.nodes():
                if other_node not in visited_nodes and node != other_node:
                    other_neighbors = set(neighbors_with_degrees(other_node))

                    if current_neighbors == other_neighbors:
                        equivalent_group.append(other_node)
                        visited_nodes.add(other_node)

            if len(equivalent_group) > 1:
                equivalent_groups.append(equivalent_group)

    return equivalent_groups


def find_katz_equivalent_groups(graph):
    katz_centralities = nx.katz_centrality(graph)
    threshold=0.65
    
    equivalent_groups = []
    for node, katz_cent in katz_centralities.items():
        for group in equivalent_groups:
            representative_node = group[0]
            if abs(katz_cent - katz_centralities[representative_node]) <= threshold:
                group.append(node)
                break
        else:
            equivalent_groups.append([node])
    return equivalent_groups


#-------------------Automorphic Equivalence-------------------#
def find_automorphic_equivalent_groups(graph):
    equivalent_groups = []
    nodes = list(graph.nodes())
    
    def is_automorphic(subgraph1, subgraph2):
        return nx.is_isomorphic(subgraph1, subgraph2)
    
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
                subgraph1 = graph.subgraph(list(curr_neighbors) + [curr_node])
                subgraph2 = graph.subgraph(list(set(graph.neighbors(n))) + [n])
                
                if is_automorphic(subgraph1, subgraph2):
                    equivalent.append(n)
                    nodes.remove(n)
            i += 1
        
        if len(equivalent) > 1:
            equivalent_groups.append(equivalent)
    
    return equivalent_groups


def equivalence_pipeline(graph):
    equivalence_functions = [
        find_structural_equivalent_groups,
        find_common_neighbor_equivalent_groups,
        find_jaccard_equivalent_groups,
        find_regular_equivalent_groups,
        find_katz_equivalent_groups,
        find_automorphic_equivalent_groups
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

        plt.figure(figsize=(35, 35))
        node_colors = [color_map[node] for node in graph.nodes()]
        nx.draw(graph, pos, node_color=node_colors, with_labels=False, cmap=new_colormap)

        func_name = func.__name__.replace("find_", "").replace("_", " ").title()
        plt.title(func_name, fontsize=40)

        plt.show()
