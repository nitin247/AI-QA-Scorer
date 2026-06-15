import streamlit as st
import uuid
import json
from pathlib import Path


def get_data_path():
    return Path(__file__).resolve().parent / "questions.json"


def load_questions():
    path = get_data_path()
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_question(record):
    path = get_data_path()
    questions = load_questions()
    questions.append(record)
    with path.open("w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)


def page_style():
    st.markdown(
        """
        <style>
            .title-style {font-size: 2.4rem; font-weight: 700; margin-bottom: 0.2rem;}
            .subtitle-style {font-size: 1.05rem; color: #6c757d; margin-bottom: 1.2rem;}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {border-radius: 0.75rem;}
            .stButton>button {background-color: #0f8b8d; color: white; border: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="AI Questionnaire Scorer | Teacher", page_icon="👩‍🏫", layout="wide")
page_style()

st.markdown('<div class="title-style">AI Questionnaire Scorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Teacher portal – create and manage short answer questions for student grading.</div>', unsafe_allow_html=True)

with st.form("question_form"):
    st.subheader("New question details")
    question_text = st.text_input("Question text", placeholder="What is the capital of France?")
    rubric_must_include = st.text_area("Required keywords / phrases", placeholder="Paris")
    rubric_synonyms = st.text_area("Valid synonyms or alternate phrasing", placeholder="City of Light")
    rubric_misconceptions = st.text_area("Common misconceptions", placeholder="Madrid is not correct")

    col1, col2 = st.columns(2)
    with col1:
        rubric_numeric_rules = st.text_input("Numeric rules / units", placeholder="Optional")
    with col2:
        rubric_scoring_bands = st.text_input("Scoring bands", value="0-5")

    rubric_exemplars = st.text_area("Reference examples", placeholder="Paris is the capital of France.")

    submitted = st.form_submit_button("Save question")
    if submitted:
        if not question_text.strip() or not rubric_must_include.strip():
            st.error("Please complete the question text and required keywords before saving.")
        else:
            new_record = {
                "qid": str(uuid.uuid4()),
                "question_text": question_text.strip(),
                "rubric_must_include": rubric_must_include.strip(),
                "rubric_synonyms": rubric_synonyms.strip(),
                "rubric_misconceptions": rubric_misconceptions.strip(),
                "rubric_numeric_rules": rubric_numeric_rules.strip(),
                "rubric_exemplars": rubric_exemplars.strip(),
                "rubric_scoring_bands": rubric_scoring_bands.strip(),
            }
            save_question(new_record)
            st.success("Question saved successfully.")
            with st.expander("View saved question"):
                st.json(new_record)

st.markdown("---")
existing_questions = load_questions()
if existing_questions:
    st.subheader(f"Existing questions ({len(existing_questions)})")
    for index, question in enumerate(existing_questions, start=1):
        with st.expander(f"Q{index}: {question['question_text']}"):
            st.markdown(f"**Must include:** {question['rubric_must_include']}")
            st.markdown(f"**Synonyms:** {question['rubric_synonyms'] or 'None'}")
            st.markdown(f"**Common misconceptions:** {question['rubric_misconceptions'] or 'None'}")
            st.markdown(f"**Reference examples:** {question['rubric_exemplars'] or 'None'}")
            st.markdown(f"**Scoring bands:** {question['rubric_scoring_bands'] or '0-5'}")
else:
    st.info("No questions have been created yet. Use the form above to add your first question.")
