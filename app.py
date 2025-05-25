import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("cs_students.csv")
st.dataframe(df)

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
st.markdown("Select your name to find out if you're ready for your dream job!")

name = st.selectbox("Select Your Name", df["Name"].unique())

if st.button("Analyze Skills"):
    student = df[df["Name"] == name].iloc[0]
    role = student["Future Career"]
    st.subheader(f"🎯 Career Goal: {role}")
    
    required = career_skills.get(role, {})
    
    gap_report = []
    score = 0
    total = len(required)
    
    for skill, required_level in required.items():
        student_level = skill_strength.get(student[skill], 0)
        if student_level >= required_level:
            result = "✅ OK"
            score += 1
        else:
            result = f"❌ Improve to level {required_level}"
        gap_report.append((skill, student[skill], result))
    
    st.write(f"📊 **Placement Readiness Score: {round((score/total)*100)}%**")
    
    st.markdown("### 🔍 Skill Feedback")
    for skill, level, result in gap_report:
        st.write(f"**{skill}**: {level} → {result}")
    
    if score == total:
        st.success("You're ready! 🚀 Just polish your projects and resume.")
    elif score >= total * 0.6:
        st.warning("You're on the right track, just a bit more practice inshaAllah.")
    else:
        st.error("You need to strengthen key skills before applying.")
