import numpy as np
from itertools import compress
from more_itertools import locate

uml_elements_types = ["is class", "is interface", "is enum", "is method", "is attribute"]
class_properties = ["is abstract", "has method", "has attribute"]
associations = ["is subclass of",  "implement", "is composed of", "is part of",
                "has parent", "calls", "uses"]
relations = uml_elements_types + class_properties + associations


def convert_graph_to_matrix(graph_entity_pairs, graph_relations):
    sources = list(set([entity_pair[0] for entity_pair in graph_entity_pairs]))
    targets = list(set([entity_pair[1] for entity_pair in graph_entity_pairs]))
    adjacency_matrix = np.zeros((len(sources), len(targets)), dtype=int)
    for row, source in enumerate(sources):
        for column, target in enumerate(targets):
            try:
                index = graph_entity_pairs.index((source, target))
                adjacency_matrix[row][column] = relations.index(graph_relations[index]) + 1
            except:
                continue

    return adjacency_matrix


def classify_uml_elements_with_types(graph_matrix, sources):
    uml_elements_matrices = [[], [], [], [], []]
    uml_elements_sources = [[], [], [], [], []]
    for index in range(1, 6):
        indices = list(locate(graph_matrix, lambda x: x[0] == index))
        uml_elements_matrices[index - 1] = graph_matrix[indices]
        uml_elements_sources[index - 1] = [sources[i] for i in indices]

    return uml_elements_sources, uml_elements_matrices
