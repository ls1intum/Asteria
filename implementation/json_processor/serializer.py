def load_result_to_json(submission_id, positive_feedback: [str], negative_feedback: [str]):
    """Function that converts the feedback generation results (positive and negative feedback) into json
    :param submission_id: submissionID
    :param positive_feedback: resulting positive feedback
    :param negative_feedback: resulting negative feedback
    :return: result in json
    """
    output = {
        "submissionID": submission_id,
        "positiveFeedback": positive_feedback,
        "negativeFeedback": negative_feedback
    }
    return output
