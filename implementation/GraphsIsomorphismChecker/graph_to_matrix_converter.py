import numpy as np
def get_union_of_two_lists(list1, list2):
    list1_set = set(list1)
    list2_set = set(list2)
    diff_list1_list2 = list1_set - list2_set
    union = list2 + list(diff_list1_list2)
    return union


def convert_graph_to_matrix(graph_entity_pairs, graph_relations, relations):
    source =  [entity_pair[0] for entity_pair in graph_entity_pairs]
    target =  [entity_pair[1] for entity_pair in graph_entity_pairs]
    entities = get_union_of_two_lists(source, target)
    adjacency_matrix = np.zeros((len(entities), len(entities)))
    for row, source in enumerate(entities):
        for column, target in enumerate(entities):
            try:
                index = graph_entity_pairs.index((source, target))
                adjacency_matrix[row][column] = relations.index(graph_relations[index]) + 1
            except:
                continue
