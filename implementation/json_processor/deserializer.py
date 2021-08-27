
def load_data_from_json(input_json):
    """Converts submissions from json to python

    :param input_json: input with submissions and sample solution
    :return: (submissions_from_json: dict of submissions, solution_from_json: JSON_object)
    """
    submissions_from_json = input_json['submission']
    solution_from_json = input_json['sampleSolutionModel']
    return submissions_from_json, solution_from_json
