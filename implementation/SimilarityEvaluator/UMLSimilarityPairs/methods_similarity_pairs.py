import numpy as np
from SimilarityEvaluator.UMLElement.Method import Method
from SimilarityEvaluator.UMLSimilarityPairs.similarity_pairs import SimilarityPairs


class MethodsPairs(SimilarityPairs):
    def __init__(self, methods_matrix, methods_sources):
        self.methods_matrix = methods_matrix
        self.methods_sources = methods_sources
        self.methods_set = [Method(method_name, method_vector) for (method_name, method_vector) in
                            zip(self.methods_sources, self.methods_matrix)]

    def get_similarity_pairs(self, reference_methods_set: 'MethodsPairs', parent_classes_similarity_set):
        similarity_list = []
        counter = 0
        methods2_set = reference_methods_set.methods_set

        for method in self.methods_set:
            similar_methods = [
                method.calculate_similarity(reference_method,
                                            parent_classes_similarity_set) for
                reference_method in methods2_set]
            if similar_methods:
                counter += 1
                max_similarity_rate = max(similar_methods)
                similar_method_index = similar_methods.index(max_similarity_rate)
                similar_method = methods2_set[similar_method_index]
                similarity_list.append((method, similar_method, max_similarity_rate))
                methods2_set.remove(similar_method)
            if not methods2_set:
                break
        if methods2_set:
            for method in methods2_set:
                similarity_list.append((None, method, 0))
        if counter < len(self.methods_set):
            for index in range(counter, len(self.methods_set)):
                similarity_list.append((self.methods_set[index], None, 0))
        return similarity_list
