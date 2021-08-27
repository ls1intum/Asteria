import numpy as np

from SimilarityEvaluator.UMLElement.Class import Class
from SimilarityEvaluator.UMLSimilarityPairs.similarity_pairs import SimilarityPairs


class ClassesPairs(SimilarityPairs):
    def __init__(self, classes_matrix, classes_sources, classes_targets):
        self.classes_matrix = classes_matrix
        self.classes_sources = classes_sources
        self.classes_targets = classes_targets
        self.classes_set = [Class(class_name, class_vector) for (class_name, class_vector) in
                            zip(self.classes_sources, self.classes_matrix)]

    def get_similarity_pairs(self, reference_classes_set: 'ClassesPairs'):
        similarity_list = []
        counter = 0
        classes2_set = reference_classes_set.classes_set
        for class1 in self.classes_set:
            similar_classes = []
            print(f"Class considered = {class1.name}")
            for reference_class in classes2_set:
                print(f"reference_class = {reference_class.name}")
                similar_classes.append(
                class1.calculate_similarity(reference_class, self.classes_targets,
                                            reference_classes_set.classes_targets))
            if similar_classes:
                counter += 1
                max_similarity_rate = max(similar_classes)
                similar_class_index = similar_classes.index(max_similarity_rate)
                similar_class = classes2_set[similar_class_index]
                similarity_list.append((class1, similar_class, max_similarity_rate))
                classes2_set.remove(similar_class)
            if not classes2_set:
                break
        if classes2_set:
            for class2 in classes2_set:
                similarity_list.append((None, class2, 0))
        if counter < len(self.classes_set):
            for index in range(counter, len(self.classes_set)):
                similarity_list.append((self.classes_set[index], None, 0))
        return similarity_list
