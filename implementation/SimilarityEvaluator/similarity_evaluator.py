from GraphHelper.graph_to_matrix_converter import convert_graph_to_matrix, classify_uml_elements_with_types
from SimilarityEvaluator.UMLSimilarityPairs.classes_similarity_pairs import ClassesPairs
from SimilarityEvaluator.UMLSimilarityPairs.methods_similarity_pairs import MethodsPairs
from SimilarityEvaluator.UMLSimilarityPairs.attributes_similarity_pairs import AttributesPairs


class SimilarityEvaluator:

    def compare_graphs(self, submission_graph, solution_graph):
        submission_entities = submission_graph[0]
        submission_relations = submission_graph[1]

        solution_entities = solution_graph[0]
        solution_relations = solution_graph[1]

        submission_matrix = convert_graph_to_matrix(submission_entities, submission_relations)
        solution_matrix = convert_graph_to_matrix(solution_entities, solution_relations)

        print(f"submission_matrix = {submission_matrix}\nsolution_matrix={solution_matrix}")

        submission_sources = list(set([submission_entity[0] for submission_entity in submission_entities]))
        submission_targets = list(set([submission_entity[1] for submission_entity in submission_entities]))

        solution_sources = list(set([solution_entity[0] for solution_entity in solution_entities]))
        solution_targets = list(set([solution_entity[1] for solution_entity in solution_entities]))

        submission_elements_sources, submission_elements_matrices, = classify_uml_elements_with_types(submission_matrix,
                                                                                                      submission_sources)
        solution_elements_sources, solution_elements_matrices = classify_uml_elements_with_types(solution_matrix,
                                                                                                 solution_sources)

        submission_classes_sources, submission_interfaces_sources, submission_enums_sources, submission_methods_sources, submission_attributes_sources = submission_elements_sources

        submission_classes_matrix, submission_interfaces_matrix, submission_enums_matrix, submission_methods_matrix, submission_attributes_matrix = submission_elements_matrices

        solution_classes_sources, solution_interfaces_sources, solution_enums_sources, solution_methods_sources, solution_attributes_sources = solution_elements_sources

        solution_classes_matrix, solution_interfaces_matrix, solution_enums_matrix, solution_methods_matrix, solution_attributes_matrix = solution_elements_matrices

        print(
            f"submission_classes_matrix={submission_classes_matrix}\nsubmission_interfaces_matrix={submission_interfaces_matrix}\nsubmission_enums_matrix={submission_enums_matrix}\nsubmission_methods_matrix={submission_methods_matrix}\nsubmission_attributes_matrix ={submission_attributes_matrix}")

        print(
            f"solution_classes_matrix={solution_classes_matrix}\nsolution_interfaces_matrix={solution_interfaces_matrix}\nsolution_enums_matrix={solution_enums_matrix}\nsolution_methods_matrix={solution_methods_matrix}\nsolution_attributes_matrix ={solution_attributes_matrix}")

        submission_classes_sets = ClassesPairs(submission_classes_matrix, submission_classes_sources, submission_targets)
        solution_classes_sets = ClassesPairs(solution_classes_matrix, solution_classes_sources, solution_targets)
        classes_similarity_sets = submission_classes_sets.get_similarity_pairs(solution_classes_sets)

        for (class1,class2,sim) in classes_similarity_sets:
            if class1 is None:
                class1_name = ""
            else:
                class1_name = class1.name
            if class2 is None:
                class2_name = ""
            else:
                class2_name = class2.name

            print(f"similar classes:{class1_name} and {class2_name} and {sim}")
        submission_interfaces_sets = ClassesPairs(submission_interfaces_matrix, submission_interfaces_sources,
                                                  submission_targets)
        solution_interfaces_sets = ClassesPairs(solution_interfaces_matrix, solution_interfaces_sources, solution_targets)
        interfaces_similarity_sets = submission_interfaces_sets.get_similarity_pairs(solution_interfaces_sets)

        for (inter1,inter2,sim) in interfaces_similarity_sets:
            if inter1 is None:
                inter1_name = ""
            else:
                inter1_name = inter1.name
            if inter2 is None:
                inter2_name = ""
            else:
                inter2_name = inter2.name

            print(f"similar interfaces:{inter1_name} and {inter2_name} and {sim}")
        submission_enums_sets = ClassesPairs(submission_enums_matrix, submission_enums_sources,
                                             submission_targets)
        solution_enums_sets = ClassesPairs(solution_enums_matrix, solution_enums_sources, solution_targets)
        enums_similarity_sets = submission_enums_sets.get_similarity_pairs(solution_enums_sets)

        submission_methods_sets = MethodsPairs(submission_methods_matrix, submission_methods_sources)
        solution_methods_sets = MethodsPairs(solution_methods_matrix, solution_methods_sources)
        methods_similarity_sets = submission_methods_sets.get_similarity_pairs(solution_methods_sets,
                                                                               classes_similarity_sets)
        for (meth1,meth2,sim) in methods_similarity_sets:
            if meth1 is None:
                meth1_name = ""
            else:
                meth1_name = meth1.name
            if meth2 is None:
                meth2_name = ""
            else:
                meth2_name = meth2.name
            print(f"similar methods:{meth1_name} and {meth2_name} and {sim}")

        submission_attributes_sets = AttributesPairs(submission_attributes_matrix, submission_attributes_sources)
        solution_attributes_sets = AttributesPairs(solution_attributes_matrix, solution_attributes_sources)
        attributes_similarity_sets = submission_attributes_sets.get_similarity_pairs(solution_attributes_sets,
                                                                                     classes_similarity_sets)

        return classes_similarity_sets, interfaces_similarity_sets, enums_similarity_sets, methods_similarity_sets, attributes_similarity_sets


'''

comparator = SimilarityEvaluator()
submission_entities = [("strategy", ""), ("strategy", "class"), ("strategy", "stephOne"), ("strategy", "stepTwo"),
                       ("strategy", "context"), ("strategy1", "strategy"), ("strategy1", ""), ("strategy1", "stephOne"),
                       ("strategy1", "stepTwo")]
submission_relations = ["be class", "be abstract", "has method", "has method", "has attribute", "be subclass of",
                        "be class", "has method", "has method"]

solution_entities = [("sortAlgorithm", ""), ("sortAlgorithm", ""), ("sortAlgorithm", "step"),
                     ("quickSort", "sortAlgorithm"), ("quickSort", "")]
solution_relations = ["be class", "be abstract", "has method", "be subclass of",
                      "be class"]

submission_graph = (submission_entities, submission_relations)
solution_graph = (solution_entities, solution_relations)

classes_similarity_sets, interfaces_similarity_sets, enums_similarity_sets, methods_similarity_sets, attributes_similarity_sets = comparator.compare_graphs(
    submission_graph, solution_graph)
'''