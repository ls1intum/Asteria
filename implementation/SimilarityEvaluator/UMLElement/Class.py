from SimilarityEvaluator.UMLElement.NameSimilarity import levenshteinSimilarity
from SimilarityEvaluator.similarity_options import SimilarityOptions
from SimilarityEvaluator.UMLElement.UMLElement import UMLElement
from more_itertools import locate
from collections import Counter
import numpy as np


class Class(UMLElement):

    def __init__(self, class_name, class_vector):
        self.name = class_name
        self.vector = class_vector
        self.similarity_options = SimilarityOptions()

    def __get_intersection(self, lst1, lst2):
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3

    def __calculate_methods_similarity(self, reference_class: 'Class', targets1_list, targets2_list):
        has_method_index = self.similarity_options.RELATIONS.index("has method")

        class1_methods_locations = map(lambda x: x - 1,
                                       list(locate(self.vector, lambda x: x == has_method_index + 1)))
        print(f"class1_methods_locations = {list(class1_methods_locations)}\n")
        methods_class_1 = [targets1_list[index] for index in list(class1_methods_locations)]

        class2_methods_locations = map(lambda x: x - 1,
                                       list(locate(reference_class.vector, lambda x: x == has_method_index + 1)))
        print(f"class2_methods_locations = {list(class2_methods_locations)}\n")
        methods_class_2 = [targets2_list[index] for index in
                           list(class2_methods_locations)]
        # similarity based on the number of methods they have
        number_of_methods_similarity = min(len(methods_class_1),
                                           len(methods_class_2)) * self.similarity_options.METHODS_NUMBER_WEIGHT

        return number_of_methods_similarity

    def __calculate_attributes_similarity(self, reference_class: 'Class'):
        has_attribute_index = self.similarity_options.RELATIONS.index("has attribute")
        attributes_class_1 = list(locate(self.vector, lambda x: x == has_attribute_index + 1))
        attributes_class_2 = list(locate(reference_class.vector, lambda x: x == has_attribute_index + 1))
        number_of_attributes_similarity = min(len(attributes_class_1),
                                              len(attributes_class_2)) * self.similarity_options.ATTRIBUTES_NUMBER_WEIGHT
        return number_of_attributes_similarity



    @property
    def get_element_count(self):
        return len(list(filter(lambda x: x != 0, self.vector)))

    def calculate_similarity(self, reference_class: 'Class', targets1_list,
                             targets2_list):
        '''
        For calculating the weight of the similarity of every element, we consider the max. element count to reflect missing elements, i.e. it should not be possible to get a
        similarity of 1 if the amount of elements differs. E.g. if we compare two classes, classA with one attribute and classB with two attributes, the highest possible
        similarity between these classes should be 2/3 (name/type + one attribute can be similar), so the weight should be 1/3, no matter if we do
        classA.overallSimilarity(classB) or classB.overallSimilarity(classA). As we know that the reference class has at least as many elements as this class, we take the
        element count of the reference.
        '''
        weight = 1.0 / min(self.get_element_count, reference_class.get_element_count)

        name_similarity = levenshteinSimilarity(self.name,
                                                reference_class.name) * self.similarity_options.CLASS_NAME_WEIGHT
        abstract_index = self.similarity_options.RELATIONS.index("is abstract") + 1
        abstract_filter = lambda x: x == abstract_index
        reference_class_abstract = filter(abstract_filter, reference_class.vector)
        class_abstract = filter(abstract_filter, self.vector)
        type_similarity = (class_abstract == reference_class_abstract) * self.similarity_options.CLASS_TYPE_WEIGHT

        association_indices = [self.similarity_options.RELATIONS.index(association) + 1 for association in self.similarity_options.UML_ASSOCIATIONS]
        association_filter = lambda x: x in association_indices
        similar_associations = self.__get_intersection(
            list(filter(association_filter, self.vector)), list(
                filter(association_filter,
                       reference_class.vector)))
        associations_similarity = len(similar_associations) * self.similarity_options.RELATION_TYPE_WEIGHT
        print(f"associations similarity = {associations_similarity}\n")
        methods_similarity = self.__calculate_methods_similarity(reference_class, targets1_list, targets2_list)
        print(f"methods similarity = {methods_similarity}\n")
        attributes_similarity = self.__calculate_attributes_similarity(reference_class)
        similarity =   name_similarity + type_similarity + associations_similarity + methods_similarity + attributes_similarity
        print(f"similarity before weight= {similarity}")

        similarity = weight * similarity

        print(f"similarity after weigt = {similarity}")
        return similarity



