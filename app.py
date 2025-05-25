import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("cs_students.csv")
# st.dataframe(df)

# Convert skill levels to numbers
skill_strength = {"Weak": 1, "Average": 2, "Strong": 3}

# Define what each career requires
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

# UI
st.title("🤖 AI Mentor: Skill Gap Analyzer")
st.markdown("Welcome to your personalized career readiness check! 🎓")

st.divider()
name = st.selectbox("👤 Select Your Name", df["Name"].unique())

if 'analyze' not in st.session_state:
    st.session_state.analyze = False

if st.button("🔍 Analyze My Skills"):
    st.session_state.analyze = True

if st.session_state.analyze:
    student = df[df["Name"] == name].iloc[0]
    role = student["Future Career"]
    st.subheader(f"🎯 Career Goal: `{role}`")

    required = career_skills.get(role, {})

    st.divider()
    st.markdown("### 📊 Skill Gap Report")
    score = 0
    total = len(required)

    for skill, required_level in required.items():
        student_level = skill_strength.get(student[skill], 0)
        level_display = f"{student[skill]} ({student_level}/3)"
        required_display = f"{required_level}/3"
        
        # Color code based on status
        if student_level >= required_level:
            st.success(f"✅ **{skill}**: You’re good! ({level_display})")
            score += 1
        else:
            st.warning(f"⚠️ **{skill}**: Needs improvement → required: {required_display}, yours: {level_display}")

    st.divider()
    readiness = round((score / total) * 100)
    st.markdown(f"### 🎯 Placement Readiness Score: **{readiness}%**")

    if score == total:
        st.success("🚀 You're ready to apply! Just polish your resume and go get that job!")
    elif score >= total * 0.6:
        st.info("✨ You’re almost there! A bit more practice and you’ll shine inshaAllah.")
    else:
        st.error("📚 Focus on improving core skills before applying.")

