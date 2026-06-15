import pathlib

parent_dir = pathlib.Path(__file__).parent.parent
        file_path = parent_dir / 'model'

from file_path import final_score

def get_result_inline(qid, answer):
    """Return grading results without requiring an HTTP API call."""
    fs = final_score.Score()
    return fs.get_final_score(qid, answer)
