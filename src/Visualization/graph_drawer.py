import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(entity_pairs, relations):
    G = nx.DiGraph()
    edge_labels = dict()
    for index, entity in enumerate(entity_pairs):
        node1 = entity[0]
        node2 = entity[1]
        relation = relations[index]
        G.add_edge(node1, node2, label=relation, length=2 * len(relation))
        edge_labels[(node1, node2)] = relations[index]  # store the string version as a label

    pos = nx.spring_layout(G, k=0.5)  # set the positions of the nodes/edges/labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx(G, pos=pos, node_color='skyblue', node_size=7000, edge_cmap=plt.cm.Blues, edge_color='skyblue',
                     width=4, font_size=14)  # draw everything but the edge labels
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, node_color='skyblue', node_size=4000,
                                 edge_cmap=plt.cm.Blues)
    plt.show()
