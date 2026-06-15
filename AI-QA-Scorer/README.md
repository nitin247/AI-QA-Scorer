AI Questionnaire Scorer
======================

Project to automatically score short-answer questionnaires using a combination of keyword matching, cosine similarity, and a small fine-tuned model for educational scoring.

**Features**
- Automatic scoring of student responses
- Teacher tools to create and manage questions
- Streamlit-based client UI for running the app locally
- Modular scoring components: keyword match, cosine similarity, and final scoring

**Quick Start**

Prerequisites
- Python 3.9+ (recommended)
- Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit UI (development):

```bash
streamlit run client/streamlit_main.py
```

Repository layout

- client/: Frontend and example runners
  - client/streamlit_main.py — Streamlit app entrypoint
  - client/student/inline_grader.py — student-side grading helpers
  - client/student/questionnarie.py — student questionnaire flow
  - client/teacher/create_question.py — teacher question creation script
  - client/teacher/questions.json — example question bank
- model/: scoring modules
  - model/cosine_similarity.py
  - model/keywords_match.py
  - model/final_score.py
  - model/slm.py
- fine_tuned_model/: (large model file; not tracked in package manager)
  - Qwen3-0.6B-SAG-Edu-F16.gguf

How it works
- The system combines simple keyword matching and vector similarity to produce candidate scores, then applies a final scoring model or heuristic in `model/final_score.py`.
- Teachers author questions with expected keywords and optionally sample answers using `client/teacher/create_question.py` and `client/teacher/questions.json`.

Usage examples

- Score a single response programmatically (example):

```python
from model.keywords_match import score_keywords
from model.cosine_similarity import cosine_score
from model.final_score import combine_scores

text = "Student answer text here"
kw = score_keywords(text, question_keywords=[...])
cos = cosine_score(text, sample_answers=[...])
final = combine_scores(kw, cos)
print(final)
```

Notes about models and data
- Large model file(s) live in `fine_tuned_model/`. The repo includes a `.gguf` model file for local use; loading and inference depend on your chosen runtime.
- The app is intentionally modular — you can swap or improve scoring components in `model/`.

Contributing
- Tidy up `client/teacher/questions.json` when adding new questions.
- Add unit tests for new scoring logic under a `tests/` folder (not present yet).

Contacts
- For questions, edit or open an issue in the repo.

License
- No license specified. Add a `LICENSE` file if you want to make the project open-source.
