import streamlit as st
import json
import pathlib
import inline_grader


def get_rubrics():
    parent_dir = pathlib.Path(__file__).parent.parent
    file_path = parent_dir / '..' / 'teacher' / 'questions.json'
    if not file_path.exists():
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def page_style():
    st.markdown(
        """
        <style>
            .title-style {font-size: 2.6rem; font-weight: 700; margin-bottom: 0.3rem;}
            .subtitle-style {font-size: 1.05rem; color: #6c757d; margin-bottom: 1.4rem;}
            .result-card {border-radius: 1rem; background: #f8f9fa; padding: 1rem;}
            .stButton>button {background-color: #1f77b4; color: white; border: none;}
            .stTextArea>div>div>textarea {min-height: 160px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="AI Questionnaire Scorer | Student", page_icon="📝", layout="wide")
page_style()

st.markdown('<div class="title-style">AI Questionnaire Scorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Student portal – choose a question and get instant grading feedback.</div>', unsafe_allow_html=True)

all_questions = get_rubrics()

if not all_questions:
    st.warning("No questions are available yet. Please ask your teacher to add questions in the Teacher app.")
else:
    question_labels = [f"Q{idx + 1}: {q['question_text']}" for idx, q in enumerate(all_questions)]
    selected_index = st.selectbox("Select a question", options=list(range(len(question_labels))), format_func=lambda x: question_labels[x])
    selected_question = all_questions[selected_index]

    st.markdown(f"### {question_labels[selected_index]}")
    st.info(selected_question['question_text'])

    with st.form("student_answer_form"):
        answer = st.text_area("Your answer", placeholder="Type your answer here...")
        submitted = st.form_submit_button("Grade answer")

        if submitted:
            if not answer.strip():
                st.error("Please enter your answer before submitting.")
            else:
                with st.spinner("Grading your answer..."):
                    result = inline_grader.get_result_inline(selected_question['qid'], answer)

                st.success("Answer graded successfully")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("Verdict", result['verdict'].capitalize())
                col2.metric("Score", f"{result['score']} / 5")
                col3.metric("Missing points", result['missing_points'] or "None")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("#### Feedback")
                st.write(result['feedback'])
                if result['missing_points']:
                    st.warning(result['missing_points'])
                st.markdown("---")
                st.caption("Change the selected question to grade another answer.")

