import networkx as nx
from matplotlib import pyplot as plt


def plot_graph_with_weights(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)

    color_map = {
        'ArticleChannel': 'blue',
        'ArticleRessortName': 'green',
        'Article': 'red',
        'Posting': 'cyan',
        'Vote': 'magenta'
    }

    # Assign colors to nodes based on their type
    # node_colors = [color_map.get(G.nodes[node]['type'], 'grey') for node in G]
    node_colors = [color_map.get(G.nodes[node].get('type'), 'grey') for node in G]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors)
    #
    # # Draw edges
    nx.draw_networkx_edges(G, pos, width=1, arrows=True)
    #
    # # Draw node labels
    # node_labels = {node[0]: node[1]['type'][0] for node in
    #                G.nodes(data=True)}  # Just first letter of type for simplicity
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    # nx.draw(G, pos, with_labels=True, font_size=8)
    # Draw edge labels
    # edge_labels = nx.get_edge_attributes(G, 'label')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title('Graph of Articles, Postings, and Votes')
    plt.axis('off')
    plt.show()
