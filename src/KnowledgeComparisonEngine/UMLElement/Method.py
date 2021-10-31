import numpy as np
from KnowledgeComparisonEngine.UMLElement.NameSimilarity import calculate_similarity
from KnowledgeComparisonEngine.UMLElement.UMLElement import UMLElement
from KnowledgeComparisonEngine.similarity_options import SimilarityOptions


class Method(UMLElement):
    def __init__(self, method_name, method_vector):
        self.name = method_name
        self.vector = method_vector
        self.similarity_options = SimilarityOptions()

    def calculate_similarity(self, reference_method: 'Method',
                             class_similarity_list):
        """Calculate the similarity between two methods
                :param reference_method: Method to compare with
                :param class_similarity_list: Containing class of the method
                :return: similarity rate between two methods
        """
        name_similarity = calculate_similarity(self.name,
                                               reference_method.name) * self.similarity_options.METHOD_NAME_WEIGHT
        has_parent_index = self.similarity_options.RELATIONS.index("has parent") + 1
        parents1 = np.where(np.array(self.vector) == has_parent_index)[0]
        parents2 = np.where(np.array(reference_method.vector) == has_parent_index)[0]
        similar_parents = [(parent1, parent2) for (parent1, parent2, similarity_rate) in class_similarity_list if
                           parent1 in parents1 and parent2 in parents2]

        parent_similarity = len(similar_parents) * self.similarity_options.METHOD_PARENT_WEIGHT
        similarity = name_similarity + parent_similarity
        return self.ensure_similarity_range(similarity)
