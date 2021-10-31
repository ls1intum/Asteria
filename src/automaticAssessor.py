import os
from pathlib import Path

from FeedbackInferenceEngine.feedback_generator import FeedbackGenerator
from KnowledgeComparisonEngine.similarity_evaluator import compare_graphs
from KnowledgeExtractionEngine.TextExtractor.text_extractor import TextExtractor
from KnowledgeExtractionEngine.UMLModelExtractor.uml_extractor import UML_extractor
from Visualization.graph_drawer import draw_graph


def extract_information_from_sample_solution(sample_solution):
    # extract KG from UML class diagram
    uml_extractor = UML_extractor(sample_solution)
    solution_graph_nodes, solution_graph_edges = uml_extractor.get_graph_from_uml_diagram()
    solution_graph = solution_graph_nodes, solution_graph_edges
    draw_graph(solution_graph_nodes, solution_graph_edges)

    return solution_graph


def generate_feedback_for_all_submissions(submissions_folder, sample_solution_path, feedback_directory):
    feedback_folder_name = os.path.join(feedback_directory, "AsteriaFeedback")
    if not os.path.exists(feedback_folder_name):
        os.makedirs(feedback_folder_name)

    solution_graph = extract_information_from_sample_solution(sample_solution_path)
    pathslist = Path(submissions_folder).glob('**/*.txt')
    for path in pathslist:
        submission_path = str(path)
        generate_feedback_for_submission(submission_path, solution_graph, feedback_folder_name)


def generate_feedback_for_submission(submission_path: str, solution_graph, feedback_folder_path) -> ([str], [str]):
    with open(submission_path, 'r') as file:
        txt_submission = file.read().replace('\n', '')
    # extract KG from Text
    text_extractor = TextExtractor()
    submission_graph_nodes, submission_graph_edges = text_extractor.get_graph_from_text(txt_submission)
    submission_graph = submission_graph_nodes, submission_graph_edges
    draw_graph(submission_graph_nodes, submission_graph_edges)

    # evaluate similarity between two KGs

    classes_similarity_sets, enums_similarity_sets, methods_similarity_sets, attributes_similarity_sets = compare_graphs(
        submission_graph, solution_graph)

    # generate Feedback
    feedback_generator = FeedbackGenerator()
    positive_feedback, negative_feedback = feedback_generator.get_feedback(classes_similarity_sets)

    automated_feedback = "########### FEEDBACK ###########\n" + "+++++++++++ POSITIVE FEEDBACK +++++++++++\n"
    for feedback_txt in positive_feedback:
        automated_feedback += f"{feedback_txt}\n"

    automated_feedback += "+++++++++++++++++++++++++++++++++++++++++\n" + "----------- NEGATIVE FEEDBACK -----------\n"
    for feedback_txt in negative_feedback:
        automated_feedback += f"{feedback_txt}\n"

    if not negative_feedback:
        automated_feedback += "*****************************************\n" + "Good Job! Everything seems to be " \
                                                                              "correct." + \
                              "*****************************************\n "
    file_name = os.path.split(submission_path)
    feedback_file_name = "asteria_feedback_ " + file_name[1]

    with open(os.path.join(feedback_folder_path, feedback_file_name), "a") as f:
        f.write(automated_feedback)

    print(automated_feedback)

    return positive_feedback, negative_feedback
