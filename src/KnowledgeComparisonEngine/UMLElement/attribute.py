import numpy as np
from KnowledgeComparisonEngine.UMLElement.NameSimilarity import calculate_similarity
from KnowledgeComparisonEngine.UMLElement.UMLElement import UMLElement
from KnowledgeComparisonEngine.similarity_options import SimilarityOptions


class Attribute(UMLElement):
    def __init__(self, attr_name: str, attr_vector: list()):
        self.name = attr_name
        self.vector = attr_vector
        self.similarity_options = SimilarityOptions()

    def calculate_similarity(self, reference_attribute: 'Attribute', class_similarity_list) -> float:
        """Calculate the similarity between two attributes
        :param reference_attribute: Attribute to compare with
        :param class_similarity_list: Containing class of the attribute
        :return: similarity rate between two attributes
    """
        name_similarity = calculate_similarity(self.name,
                                               reference_attribute.name) * self.similarity_options.ATTRIBUTE_NAME_WEIGHT
        has_parent_index = self.similarity_options.RELATIONS.index("has parent") + 1
        # It could be the case that an attribute with the same name is contained in different classes
        parents1 = np.where(np.array(self.vector) == has_parent_index)[0]
        parents2 = np.where(np.array(reference_attribute.vector) == has_parent_index)[0]
        similar_parents = [(parent1, parent2) for (parent1, parent2, similarity_rate) in class_similarity_list if
                           parent1 in parents1 and parent2 in parents2]
        parent_similarity = len(similar_parents) * self.similarity_options.ATTRIBUTE_PARENT_WEIGHT
        similarity = name_similarity + parent_similarity
        return self.ensure_similarity_range(similarity)
