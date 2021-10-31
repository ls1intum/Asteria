from KnowledgeComparisonEngine.UMLSimilarityPairs.attributes_similarity_pairs import AttributesPairs
from KnowledgeComparisonEngine.UMLSimilarityPairs.classes_similarity_pairs import ClassesPairs
from KnowledgeComparisonEngine.UMLSimilarityPairs.methods_similarity_pairs import MethodsPairs
from Visualization.graph_to_matrix_converter import convert_graph_to_matrix, classify_uml_elements_with_types


def compare_graphs(submission_graph, solution_graph):
    submission_entities = submission_graph[0]
    submission_relations = submission_graph[1]

    solution_entities = solution_graph[0]
    solution_relations = solution_graph[1]

    submission_matrix = convert_graph_to_matrix(submission_entities, submission_relations)
    solution_matrix = convert_graph_to_matrix(solution_entities, solution_relations)

    submission_sources = list(set([submission_entity[0] for submission_entity in submission_entities]))
    submission_targets = list(set([submission_entity[1] for submission_entity in submission_entities]))

    solution_sources = list(set([solution_entity[0] for solution_entity in solution_entities]))
    solution_targets = list(set([solution_entity[1] for solution_entity in solution_entities]))

    submission_elements_sources, submission_elements_matrices, = classify_uml_elements_with_types(submission_matrix,
                                                                                                  submission_sources)
    solution_elements_sources, solution_elements_matrices = classify_uml_elements_with_types(solution_matrix,
                                                                                             solution_sources)

    submission_classes_sources, submission_enums_sources, submission_methods_sources, submission_attributes_sources = submission_elements_sources

    submission_classes_matrix, submission_enums_matrix, submission_methods_matrix, submission_attributes_matrix = submission_elements_matrices

    solution_classes_sources, solution_enums_sources, solution_methods_sources, solution_attributes_sources = solution_elements_sources

    solution_classes_matrix, solution_enums_matrix, solution_methods_matrix, solution_attributes_matrix = solution_elements_matrices

    submission_classes_sets = ClassesPairs(submission_classes_matrix, submission_classes_sources,
                                           submission_targets)
    solution_classes_sets = ClassesPairs(solution_classes_matrix, solution_classes_sources, solution_targets)
    classes_similarity_sets = submission_classes_sets.get_similarity_pairs(solution_classes_sets)

    submission_enums_sets = ClassesPairs(submission_enums_matrix, submission_enums_sources,
                                         submission_targets)
    solution_enums_sets = ClassesPairs(solution_enums_matrix, solution_enums_sources, solution_targets)
    enums_similarity_sets = submission_enums_sets.get_similarity_pairs(solution_enums_sets)

    submission_methods_sets = MethodsPairs(submission_methods_matrix, submission_methods_sources)
    solution_methods_sets = MethodsPairs(solution_methods_matrix, solution_methods_sources)
    methods_similarity_sets = submission_methods_sets.get_similarity_pairs(solution_methods_sets,
                                                                           classes_similarity_sets)

    submission_attributes_sets = AttributesPairs(submission_attributes_matrix, submission_attributes_sources)
    solution_attributes_sets = AttributesPairs(solution_attributes_matrix, solution_attributes_sources)
    attributes_similarity_sets = submission_attributes_sets.get_similarity_pairs(solution_attributes_sets,
                                                                                 classes_similarity_sets)

    return classes_similarity_sets, enums_similarity_sets, methods_similarity_sets, attributes_similarity_sets
