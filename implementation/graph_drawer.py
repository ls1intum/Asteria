import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(entity_pairs, relations):
    G = nx.DiGraph()
    edge_labels = dict()
    for index, entity in enumerate(entity_pairs):
        node1 = entity[0]
        node2 = entity[1]
        relation = relations[index]
        G.add_edge(node1, node2, label= relation, length = len(relation) * 2 )
        edge_labels[(node1, node2)] = relations[index]  # store the string version as a label

    plt.figure(figsize=(12,12))

    # Draw the graph


   # nx.draw_networkx_nodes(G, pos)
   # nx.draw_networkx_labels(G, pos)
   # nx.draw_networkx_edges(G, pos, edge_labels=edge_labels)
    pos = nx.spring_layout(G) # set the positions of the nodes/edges/labels
    nx.draw_networkx(G, pos=pos, node_color='skyblue', node_size=2000, edge_cmap=plt.cm.Blues) # draw everything but the edge labels
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, node_color='skyblue', node_size=2000, edge_cmap=plt.cm.Blues)
    plt.show()


    '''

    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})

    G=nx.from_pandas_edgelist(kg_df[kg_df['edge']=="composed by"], "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())

    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G, k = 0.5)
    plt.show()
    '''
    #nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)

