import streamlit as st
import pandas as pd
from components import skill_card

# Load dataset
df = pd.read_csv("cs_students.csv")

# Skill strength mapping
skill_strength = {"Weak": 1, "Average": 2, "Strong": 3}

# Career skill requirements
career_skills = {
    "Machine Learning Researcher": {"Python": 3, "SQL": 2, "Java": 1},
    "Data Scientist": {"Python": 3, "SQL": 3, "Java": 1},
    "Software Engineer": {"Python": 2, "SQL": 2, "Java": 3},
    "Web Developer": {"Python": 2, "SQL": 3, "Java": 3},
    "Information Security Analyst": {"Python": 2, "SQL": 1, "Java": 3},
    "Machine Learning Engineer": {"Python": 3, "SQL": 2, "Java": 1},
    "Database Administrator": {"Python": 1, "SQL": 3, "Java": 2},
    "Cloud Solutions Architect": {"Python": 2, "SQL": 3, "Java": 2},
    "Mobile App Developer": {"Python": 2, "SQL": 1, "Java": 3},
}

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

# App Title
st.title("AI Mentor: Skill Gap Analyzer")

# Sidebar Help
st.sidebar.header("AI Mentor Help")
st.sidebar.markdown(
    """
- Select your name.
- Click **Analyze My Skills**.
- Review skill gaps and readiness score.
- Focus on suggested improvements.
"""
)

# User Selection
name = st.selectbox("Select Your Name", df["Name"].unique())

# Analyze Button
if "analyze" not in st.session_state:
    st.session_state.analyze = False

if st.button("Analyze My Skills"):
    st.session_state.analyze = True

# Analysis Output
if st.session_state.analyze:
    student = df[df["Name"] == name].iloc[0]
    role = student["Future Career"]
    st.markdown(f'<h2 class="career-goal">Career Goal: {role}</h2>', unsafe_allow_html=True)

    required = career_skills.get(role, {})
    st.markdown('<div class="skill-gap-report">', unsafe_allow_html=True)

    score = 0
    total = len(required)

    for skill, required_level in required.items():
        student_level = skill_strength.get(student[skill], 0)
        if student_level >= required_level:
            score += 1
        skill_card(skill, student_level, required_level)

    st.markdown('</div>', unsafe_allow_html=True)

    # Readiness score
    readiness = round((score / total) * 100)
    gpa_score = (student["GPA"] / 4.0) * 100
    combined_score = round((readiness * 0.7) + (gpa_score * 0.3), 2)

    if combined_score >= 85:
        status = "Outstanding! You're more than ready."
        card_class = "score-success"
    elif combined_score >= 70:
        status = "Good job! A few touch-ups and you’re ready."
        card_class = "score-warning"
    else:
        status = "Focus on improving both GPA and skills."
        card_class = "score-fail"

    score_html = f"""
    <div class="score-card {card_class}">
        <h3>Final Readiness Score: {combined_score}%</h3>
        <p>{status}</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width:{combined_score}%"></div>
        </div>
    </div>
    """
    st.markdown(score_html, unsafe_allow_html=True)
