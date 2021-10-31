from KnowledgeComparisonEngine.UMLElement.Class import Class
from KnowledgeComparisonEngine.UMLSimilarityPairs.similarity_pairs import SimilarityPairs


class ClassesPairs(SimilarityPairs):
    def __init__(self, classes_matrix, classes_sources, classes_targets):
        self.classes_matrix = classes_matrix
        self.classes_sources = classes_sources
        self.classes_targets = classes_targets
        self.classes_set = [Class(class_name, class_vector) for (class_name, class_vector) in
                            zip(self.classes_sources, self.classes_matrix)]

    def get_similarity_pairs(self, reference_classes_set: 'ClassesPairs'):
        """ Generate the classes similarity pairs
            :param reference_classes_set: set of reference classes to compare with
            :return: List containing the pairs of similar classes : (class1, class2), (class1, None), (None, class2)
            """
        similarity_list = []
        counter = 0
        classes2_set = reference_classes_set.classes_set
        similarity_matrix = []
        matched_classes = []
        for class1 in self.classes_set:
            similar_classes = []
            for reference_class in classes2_set:
                similar_classes.append(
                    class1.calculate_similarity(reference_class, self.classes_targets,
                                                reference_classes_set.classes_targets))
            similarity_matrix.append(similar_classes)

        max_similarities = [(similarity_vecto.index(max(similarity_vecto)), max(similarity_vecto)) for similarity_vecto
                            in similarity_matrix]

        for index, pair in enumerate(max_similarities):
            same_matching = [y for (x, y) in max_similarities if x == pair[0]]
            if (len(same_matching) == 1 or max(same_matching) == pair[1]):
                similar_class = classes2_set[pair[0]]
                similarity_list.append((self.classes_set[index], similar_class, pair[1]))
                matched_classes.append(similar_class)
            else:
                similarity_list.append((self.classes_set[index], None, 0))

        for class2 in classes2_set:
            if class2 not in matched_classes:
                similarity_list.append((None, class2, 0))

        return similarity_list
