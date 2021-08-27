from FeedbackGenerator.feedback_text import FeedbackText
from SimilarityEvaluator.similarity_options import SimilarityOptions
from collections import Counter
import numpy as np


class feedback_generator:

    def __init__(self):
        self.feedback_text = FeedbackText()
        similarity_options = SimilarityOptions()
        associations = []
        self.relations = similarity_options.RELATIONS
        self.associations_indices = [self.relations.index(association) + 1 for association in associations]

    def generate_feedback_for_one_element(self, submission_element, solution_element, similarity_rate, similarity_pairs,
                                          submission_vector, solution_vector, submission_targets, solution_targets):
        if submission_element is None:
            return [self.feedback_text.MISSING_ELEMENT_TEXT + solution_element]

        if solution_element is None:
            return [submission_element + self.feedback_text.SUPERFLUOUS_ELEMENT_TEXT]

        if similarity_rate == 1:
            return [self.feedback_text.CORRECT_ELEMENT_TEXT + submission_element]

        submission_associations = list(filter(lambda x: x in self.associations_indices), submission_vector)
        solution_associations = list(filter(lambda x: x in self.associations_indices), solution_vector)
        similar_elements = list((Counter(submission_associations) & Counter(solution_associations)).elements())
        superfluous_elements = list((Counter(submission_associations) - Counter(solution_associations)).elements())
        missing_elements = list((Counter(solution_associations) - Counter(submission_associations)).elements())

        has_method_index = self.relations.index("has method") + 1
        has_attribute_index = self.relations.index("has attribute") + 1

        submission_methods = np.where(np.array(submission_vector) == has_method_index)[0]
        solution_methods = np.where(np.array(solution_vector) == has_attribute_index)[0]

        if len(submission_methods) < len(solution_methods):
            submission_methods = [(parent1, parent2) for (parent1, parent2) in similarity_pairs if
                                  parent1 in submission_methods and parent2 in solution_methods]

    def generate_feedback_for_associations(self, submission_element, solution_element, submission_vector,
                                           solution_vector, submission_targets, solution_targets, similarity):

        # submission_associations = [(relation, target) for (relation, target) in zip(submission_vector, submission_targets) if relation in self.associations_indices ]
        # solution_associations = [(relation, target) for (relation, target) in zip(solution_vector, solution_targets) if relation in self.associations_indices ]
        # sorted_submission_associations = submission_associations.sort(key= lambda pair: pair[0])
        # sorted_solution_associations = solution_associations.sort(key = lambda pair: pair[0])

        submission_associations = list(filter(lambda x: x in self.associations_indices), submission_vector)
        solution_associations = list(filter(lambda x: x in self.associations_indices), solution_vector)

        similar_elements = list((Counter(submission_associations) & Counter(solution_associations)).elements())
        superfluous_elements = list((Counter(submission_associations) - Counter(solution_associations)).elements())
        missing_elements = list((Counter(solution_associations) - Counter(submission_associations)).elements())

        if len(submission_associations) == len(solution_associations):
            return "You have covered all associations of the " + submission_element


        if len(submission_associations) < len(solution_associations):
            correct_associations = ",".join(similar_elements)
            return "You mentioned correctly the associations:" 
        similar_elements = list((Counter(submission_associations) & Counter(solution_associations)).elements())
        superfluous_elements = list((Counter(submission_associations) - Counter(solution_associations)).elements())
        missing_elements = list((Counter(solution_associations) - Counter(submission_associations)).elements())
