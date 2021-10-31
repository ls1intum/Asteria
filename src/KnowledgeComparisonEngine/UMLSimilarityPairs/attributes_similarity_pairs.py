from KnowledgeComparisonEngine.UMLElement.Attribute import Attribute
from KnowledgeComparisonEngine.UMLSimilarityPairs.similarity_pairs import SimilarityPairs


class AttributesPairs(SimilarityPairs):
    def __init__(self, attr_matrix, attr_sources):
        self.attr_matrix = attr_matrix
        self.attr_sources = attr_sources
        self.attr_set = [Attribute(attr_name, attr_vector) for (attr_name, attr_vector) in
                         zip(self.attr_sources, self.attr_matrix)]

    def get_similarity_pairs(self, reference_attributes_set: 'AttributesPairs', parent_classes_similarity_set):
        """ Generate the attributes similarity pairs
        :param reference_attributes_set: set of reference attributes
        :param parent_classes_similarity_set: List of Containing classes of the attributes
        :return: List containing the pairs of similar attributes : (attr1, attr2), (attr1, None), (None, attr2)
        """
        similarity_list = []
        counter = 0
        attr2_set = reference_attributes_set.attr_set
        for attr in self.attr_set:
            similar_attributes = [attr.calculate_similarity(attr2, parent_classes_similarity_set) for attr2 in
                                  attr2_set]
            if similar_attributes:
                counter += 1
                max_similarity_rate = max(similar_attributes)
                similar_attr_index = similar_attributes.index(max_similarity_rate)
                similar_attr = attr2_set[similar_attr_index]
                similarity_list.append((attr, similar_attr, max_similarity_rate))
                # attr2_set.remove(similar_attr_index)
            if not attr2_set:
                break
        if attr2_set:
            for attr in attr2_set:
                similarity_list.append((None, attr, 0))

        if counter < len(self.attr_set):
            for index in range(counter, len(self.attr_set)):
                similarity_list.append((self.attr_set[index], None, 0))

        return similarity_list
