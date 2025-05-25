import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("cs_students.csv")

# Skill strength mapping
skill_strength = {"Weak": 1, "Average": 2, "Strong": 3}

# Define career requirements
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

# --- UI ---

st.title("AI Mentor: Skill Gap Analyzer")
st.markdown("Personalized career readiness assessment for CS students.")
st.markdown("---")

# Select student
name = st.selectbox("Select Your Name", df["Name"].unique())

# Initialize session state for analysis
if 'analyze' not in st.session_state:
    st.session_state.analyze = False
    st.session_state.selected_name = None

if st.button("Analyze My Skills"):
    st.session_state.analyze = True
    st.session_state.selected_name = name

# Show results only after clicking analyze
if st.session_state.analyze and st.session_state.selected_name:
    student = df[df["Name"] == st.session_state.selected_name].iloc[0]
    role = student["Future Career"]
    st.header(f"Career Goal: {role}")

    required = career_skills.get(role, {})
    total_skills = len(required)

    # Calculate skill readiness score
    skill_score = 0
    for skill, req_level in required.items():
        student_level = skill_strength.get(student[skill], 0)
        if student_level >= req_level:
            skill_score += 1
    readiness = round((skill_score / total_skills) * 100)

    # GPA score
    gpa_score = (student["GPA"] / 4.0) * 100

    # Combined final score
    combined_score = round((readiness * 0.7) + (gpa_score * 0.3), 2)

    # Show summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Skill Readiness", f"{readiness}%")
    col2.metric("GPA Score", f"{round(gpa_score, 2)}%")
    col3.metric("Final Score", f"{combined_score}%")

    st.markdown("---")
    st.progress(combined_score / 100)

    # Skill gap details in expander
    with st.expander("View Skill Gap Details"):
        for skill, req_level in required.items():
            student_level = skill_strength.get(student[skill], 0)
            level_display = f"{student[skill]} ({student_level}/3)"
            req_display = f"{req_level}/3"

            if student_level >= req_level:
                st.markdown(f"<span style='color:green;'>{skill}: Meets requirement ({level_display})</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:orange;'>{skill}: Needs improvement. Required: {req_display}, Yours: {level_display}</span>", unsafe_allow_html=True)

    st.markdown("---")

    # Final message based on combined score
    if combined_score >= 85:
        st.success("Outstanding performance! You're ready.")
    elif combined_score >= 70:
        st.info("Good progress! A few improvements needed.")
    else:
        st.warning("Focus on improving both GPA and skills.")
