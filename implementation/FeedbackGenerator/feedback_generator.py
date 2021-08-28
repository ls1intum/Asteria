from collections import Counter
from FeedbackGenerator.feedback_text import FeedbackText
from SimilarityEvaluator.similarity_options import SimilarityOptions
from SimilarityEvaluator.UMLElement.Class import Class
import itertools


class FeedbackGenerator:
    def __init__(self):
        self.feedback_text = FeedbackText()
        similarity_options = SimilarityOptions()
        self.relations = similarity_options.RELATIONS

    def get_feedback(self, similarity_triples: [(Class, Class, float)]) -> ([str], [str]):
        flatten = itertools.chain.from_iterable
        correct_identified_classes = [class1.name for (class1, class2,_) in similarity_triples if class1 is not None and class2 is not None]
        correct_classes_feedback= self.feedback_text.get_correctly_identified__classes_feedback(correct_identified_classes)
        feedback = [self.get_feedback_for_similarity_pair(similarity_triple) for similarity_triple in
                    similarity_triples]
        positive_feedback = list(flatten([feedback_pair[0] for feedback_pair in feedback]))
        positive_feedback.append(correct_classes_feedback)
        negative_feedback = list(flatten([feedback_pair[1] for feedback_pair in feedback]))
        return positive_feedback, negative_feedback

    def get_feedback_for_similarity_pair(self, similarity_triple: (Class, Class, float)) -> ([str], [str]):
        submission_element, solution_element, similarity_rate = similarity_triple

        positive_feedback = []
        negative_feedback = []
        if submission_element is None:
            negative_feedback.append(self.feedback_text.get_missing_element_feedback(solution_element.name))
            return positive_feedback, negative_feedback

        if solution_element is None:
            negative_feedback.append(self.feedback_text.get_superfluous_element_feedback(submission_element.name))
            return positive_feedback, negative_feedback

        if similarity_rate == 1:
            positive_feedback.append(self.feedback_text.CORRECT_ELEMENT_TEXT + submission_element.name)
            return positive_feedback, negative_feedback

        associations_feedback = self.get_feedback_for_associations(submission_element, solution_element)
        positive_feedback.extend(associations_feedback[0])
        negative_feedback.extend(associations_feedback[1])
        methods_feedback = self.get_feedback_for_method(submission_element, solution_element)
        positive_feedback.extend(methods_feedback[0])
        negative_feedback.extend(methods_feedback[1])
        attributes_feedback = self.get_feedback_for_attribute(submission_element, solution_element)
        positive_feedback.extend(attributes_feedback[0])
        negative_feedback.extend(attributes_feedback[1])
        return positive_feedback, negative_feedback

    def get_feedback_for_associations(self, submission_element: Class, solution_element: Class) -> ([str], [str]):
        associations_relations = ["implements","implements", "is composed of", "uses", "calls"]
        associations_names = ["inheritance", "realization", "aggregation(i.e. composition)", "unidirectional association","dependency"]
        associations_indices = [self.relations.index(association) + 1 for association in associations_relations]

        submission_associations = sorted(list(filter(lambda x: x in associations_indices, submission_element.vector)))
        solution_associations = sorted(list(filter(lambda x: x in associations_indices, solution_element.vector)))

        if not submission_associations and not solution_associations:
            return [], []

        if submission_associations == solution_associations:
            return [self.feedback_text.get_associations_fully_correct_feedback(submission_element.name)], []

        positive_feedback = []
        negative_feedback = []
        similar_associations = list((Counter(submission_associations) & Counter(solution_associations)).elements())
        similar_associations_names = [associations_names[associations_relations.index(self.relations[association - 1])]
                                      for association in similar_associations]
        if len (similar_associations_names) > 0:
            positive_feedback.append(self.feedback_text.get_associations_partially_correct_feedback(submission_element.name,
                                                                                                similar_associations_names))

        print(f"solution associations = {solution_associations}")
        print(f"submission associatiosn = {submission_associations}")
        missing_associations = list((Counter(solution_associations) - Counter(submission_associations)).elements())
        print(f"missing associations = {missing_associations}")
        missing_associations_names = [
            associations_names[associations_relations.index(self.relations[association - 1])]
            for association in missing_associations]
        if len(missing_associations_names) > 0:
            negative_feedback.append(
            self.feedback_text.get_missing_associations_feedback(submission_element.name, missing_associations_names))

        superfluous_associations = list((Counter(submission_associations) - Counter(solution_associations)).elements())
        superfluous_associations_names = [
            associations_names[associations_relations.index(self.relations[association - 1])]
            for association in superfluous_associations]
        if len(superfluous_associations_names) > 0:
            negative_feedback.append(self.feedback_text.get_superfluous_associations_feedback(submission_element.name,
                                                                                          superfluous_associations_names))
        return positive_feedback, negative_feedback

    def get_feedback_for_method(self, submission_element: Class, solution_element: Class) -> [str]:
        has_method_index = self.relations.index("has method") + 1
        submission_methods = list(filter(lambda rel: rel == has_method_index, submission_element.vector))
        solution_methods = list(filter(lambda rel: rel == has_method_index, solution_element.vector))

        if not submission_methods and not solution_methods:
            return [], []

        if len(submission_methods) == len(solution_methods):
            return [self.feedback_text.get_correct_methods_feedback(submission_element.name)], []

        if len(submission_methods) < len(solution_methods):
            return [], [self.feedback_text.get_missing_method_feedback(submission_element.name,
                                                                       len(solution_methods) - len(submission_methods))]

        if len(submission_methods) > len(solution_methods):
            return [], [self.feedback_text.get_superfluous_method_feedback(submission_element.name,
                                                                           len(submission_methods) - len(
                                                                               solution_methods))]

    def get_feedback_for_attribute(self, submission_element: Class, solution_element: Class) -> [str]:
        has_attribute_index = self.relations.index("has attribute") + 1
        submission_attributes = list(filter(lambda rel: rel == has_attribute_index, submission_element.vector))
        solution_attributes = list(filter(lambda rel: rel == has_attribute_index, solution_element.vector))

        if not submission_attributes and not solution_attributes:
            return [], []

        if len(submission_attributes) == len(solution_attributes):
            return [self.feedback_text.get_correct_attributes_feedback(submission_element.name)], []

        if len(submission_attributes) < len(solution_attributes):
            return [], [self.feedback_text.get_missing_attribute_feedback(submission_element.name,
                                                                          len(solution_attributes) - len(
                                                                              submission_attributes))]

        if len(submission_attributes) > len(solution_attributes):
            return [], [self.feedback_text.get_superfluous_attribute_feedback(submission_element.name,
                                                                              len(submission_attributes) - len(
                                                                                  solution_attributes))]
