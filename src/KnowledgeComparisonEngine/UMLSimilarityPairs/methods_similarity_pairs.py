from KnowledgeComparisonEngine.UMLElement.Method import Method
from KnowledgeComparisonEngine.UMLSimilarityPairs.similarity_pairs import SimilarityPairs


class MethodsPairs(SimilarityPairs):
    def __init__(self, methods_matrix, methods_sources):
        self.methods_matrix = methods_matrix
        self.methods_sources = methods_sources
        self.methods_set = [Method(method_name, method_vector) for (method_name, method_vector) in
                            zip(self.methods_sources, self.methods_matrix)]

    def get_similarity_pairs(self, reference_methods_set: 'MethodsPairs', parent_classes_similarity_set):
        """ Generate the methods similarity pairs
                :param reference_methods_set: set of reference methods to compare with
                :param parent_classes_similarity_set: List of Containing classes of the methods
                :return: List containing the pairs of similar methods : (meth1, meth2), (meth1, None), (None, meth2)
                """
        similarity_list = []
        counter = 0
        methods2_set = reference_methods_set.methods_set
        matched_elements = set()
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
                matched_elements.add(similar_method)
        return similarity_list
