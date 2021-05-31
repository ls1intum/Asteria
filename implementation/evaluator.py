from TextExtractor.text_extractor import Text_extractor
from UMLClassDiagramExtractor.uml_extractor import UML_extractor
from GraphsIsomorphismChecker.graph_to_matrix_converter import convert_graph_to_matrix, get_union_of_two_lists

txt_submission = ""
text_extractor = Text_extractor()
submission_graph_nodes, submission_graph_edges = text_extractor.get_graph_from_submission(txt_submission)


uml_solution_path = "/home/maisa/KnowledgeGraphs/implementation/UMLClassDiagramExtractor/UMLClassDiagram.json"
uml_extractor = UML_extractor(uml_solution_path)
solution_graph_nodes, solution_graph_edges = uml_extractor.get_graph_from_solution()


relations = get_union_of_two_lists(submission_graph_edges, solution_graph_edges)
submission_matrix = convert_graph_to_matrix(submission_graph_nodes, submission_graph_edges, relations)
solution_matrix = convert_graph_to_matrix(solution_graph_nodes, solution_graph_edges, relations)

