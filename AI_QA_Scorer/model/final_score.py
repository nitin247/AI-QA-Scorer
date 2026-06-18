from model import cosine_similarity
from model import keywords_match
import json
import pathlib


class Score:

    def __init__(self):
        return
    
    # Load Rubric
    def get_rubric_details(self, rubric_id=None):
        parent_dir = pathlib.Path(__file__).parent.parent
        file_path = parent_dir / 'client' / 'teacher' / 'questions.json'
        with open(file_path, 'r') as f:
            # Load the JSON data from the file object
            data = json.load(f)
            filtered_by_id = [question for question in data if question["qid"] == rubric_id]

        return filtered_by_id
    
    def calc_score(self, answer, rubric_id):
        rubric = self.get_rubric_details(rubric_id)
        rubric_details = rubric[0]
        
        cs = cosine_similarity.Similarity()
        km = keywords_match.Match()
        sim_score = float(cs.get_score(answer, rubric_details['rubric_must_include']))
        sim_score_rounded = round(sim_score , 2)
        keyword_hit = float(km.fuzzy_best_match(answer, [rubric_details['rubric_must_include'], rubric_details['rubric_synonyms'], rubric_details['rubric_exemplars']]))
        keyword_hit_rounded = round(keyword_hit , 2)
        question = rubric_details['question_text']
        
        # Whether to call SLM model or not        
        if sim_score_rounded >= 0.85 and keyword_hit_rounded >= 0.70:
            verdict = 'correct'
            score = int(sim_score_rounded * 5)
            return {'score':score, 'verdict': verdict, 'feedback': 'Score calculated based on similarity and keywords', 'missing_points': ''}
        else: 
            from model import slm
            lm = slm.Grade()
            llm_score = lm.grade(question, answer, keyword_hit, sim_score, rubric_details['rubric_must_include'], rubric_details['rubric_synonyms'], rubric_details['rubric_misconceptions'], rubric_details['rubric_numeric_rules'])
            score = 3;
            verdict = 'Incorrect'
            final = 0.4 * keyword_hit + 0.3 * sim_score + 0.3 * (score/5)
            final = round((final* 5), 2)
            feedback = json.loads(llm_score)
            return {'score':final, 'verdict': verdict, 'feedback': feedback['result'], 'missing_points': ''}

    def get_final_score(self, qid, answer=None):
        score_details = self.calc_score(answer, qid)
        return score_details
