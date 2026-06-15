from ShortAnswerGrader.model.final_score import Score


def get_result_inline(qid, answer):
    """Return grading results without requiring an HTTP API call."""
    fs = Score()
    return fs.get_final_score(qid, answer)
