import pathlib
import sys

import streamlit as st

# Ensure the repository root is on sys.path so imports work
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Define Streamlit pages for student and teacher interfaces
student_page = st.Page(
    "student/questionnarie.py",
    title="Student",
    icon="📝",
    default=True,
)
teacher_page = st.Page(
    "teacher/create_question.py",
    title="Teacher",
    icon="👩‍🏫",
)

st.set_page_config(page_title="AI Questionnaire Scorer", page_icon="📊", layout="wide")

# Initialize navigation and run
pg = st.navigation([student_page, teacher_page])
pg.run()
