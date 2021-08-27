from logging import getLogger

from automaticAssessor import generateFeedack, extract_information_from_sample_solution
from json_processor.deserializer import load_data_from_json
from json_processor.serializer import load_result_to_json


class ProcessingResource:
    __logger = getLogger(__name__)

    # Starts processing of a queried task
    def processTask(self, data):

        submission, solution = load_data_from_json(data)
        submission_id = submission["id"]
        submission_text = submission["text"]

        resulting_feedback = []

        solution_graph = extract_information_from_sample_solution(sample_solution=solution)
        feedback_result = generateFeedack(txt_submission=submission_text, solution_graph=solution_graph)
        output = load_result_to_json(submission_id, feedback_result[0], feedback_result[1])
        resulting_feedback.append(output)
        return resulting_feedback


