from FeedbackGenerator.feedback_generator import FeedbackGenerator
from GraphHelper.graph_drawer import draw_graph
from SimilarityEvaluator.similarity_evaluator import SimilarityEvaluator
from TextExtractor.text_extractor import TextExtractor
from UMLClassDiagramExtractor.uml_extractor import UML_extractor

#txt_submission = "The Context class uses the SortingStrategy interface. The SortingStrategy interface has the method sortList(). The ConcreteSortingStrategy classes implement the SortingStrategy interface and its sortList() method. The Context class uses the SortingStrategy class. The SortingPolicy interface calls the Context class. The Client class also calls the Context class."
txt_submission = "The Context class has the methods selectStrategy() and executeSorting(). The Context class uses the SortingStrategy interface. The SortingStrategy interface has the method sortList(). The ConcreteSortingStrategy classes implement the SortingStrategy interface and its sortList() method. The Context class uses the SortingStrategy interface. The SortingPolicy class calls the Context class. The Client class also calls the Context class."
sample_solution = "/home/maisa/Desktop/Asteria/implementation/UMLClassDiagramExtractor/SampleSolution.json"


def extract_information_from_sample_solution(sample_solution):
    # extract KG from UML class diagram
    uml_extractor = UML_extractor(sample_solution)
    solution_graph_nodes, solution_graph_edges = uml_extractor.get_graph_from_uml_diagram()
    solution_graph = solution_graph_nodes, solution_graph_edges
    draw_graph(solution_graph_nodes, solution_graph_edges)

    return solution_graph


def generateFeedack(txt_submission: str, solution_graph) -> ([str], [str]):
    # extract KG from Text

    text_extractor = TextExtractor()
    submission_graph_nodes, submission_graph_edges = text_extractor.get_graph_from_text(txt_submission)
    submission_graph = submission_graph_nodes, submission_graph_edges
    draw_graph(submission_graph_nodes, submission_graph_edges)

    # evaluate similarity between two KGs
    similarity_evaluator = SimilarityEvaluator()
    classes_similarity_sets, interfaces_similarity_sets, enums_similarity_sets, methods_similarity_sets, attributes_similarity_sets = similarity_evaluator.compare_graphs(
        submission_graph, solution_graph)

    print(
        f"classes_similarity_sets = {classes_similarity_sets}\ninterfaces_similarity_sets = {interfaces_similarity_sets}\nenums_similarity_sets = {enums_similarity_sets}\n")
    print(
        f"methods_similarity_sets = {methods_similarity_sets}\nattributes_similarity_sets = {attributes_similarity_sets}")

    # generate Feedback
    feedback_generator = FeedbackGenerator()
    classes_positive_feedback, classes_negative_feedback = feedback_generator.get_feedback(classes_similarity_sets)
    interfaces_positive_feedback, interfaces_negative_feedback = feedback_generator.get_feedback(
        interfaces_similarity_sets)
    positive_feedback = classes_positive_feedback + interfaces_positive_feedback
    negative_feedback = classes_negative_feedback + interfaces_negative_feedback

    print(f"########### FEEDBACK ###########\n")
    print(f"+++++++++++ POSITIVE FEEDBACK +++++++++++\n")
    [print(f"{feedback_txt}\n") for feedback_txt in positive_feedback]
    print(f"+++++++++++++++++++++++++++++++++++++++++\n")
    print(f"----------- NEGATIVE FEEDBACK -----------\n")
    [print(f"{feedback_txt}\n") for feedback_txt in negative_feedback]
    print(f"-----------------------------------------\n")

    return positive_feedback, negative_feedback


solution_graph = extract_information_from_sample_solution(sample_solution)
positive_feedback, negative_feedback = generateFeedack(txt_submission, solution_graph)

'''
text_extractor = TextExtractor()
submission_graph_nodes, submission_graph_edges = text_extractor.get_graph_from_text(txt_submission)
submission_graph = submission_graph_nodes, submission_graph_edges
draw_graph(submission_graph_nodes, submission_graph_edges)
'''
