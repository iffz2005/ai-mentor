import streamlit as st

def skill_card(skill, student_level, required_level):
    level_names = {1: "Weak", 2: "Average", 3: "Strong"}
    card_class = "skill-good" if student_level >= required_level else "skill-improve"

    student_text = level_names.get(student_level, "N/A")
    required_text = level_names.get(required_level, "N/A")

    progress_pct = (student_level / 3) * 100

    card_html = f"""
    <div class="skill-card {card_class}">
        <div class="skill-name">{skill}</div>
        <div class="skill-level">
            Your Level: <strong>{student_text} ({student_level}/3)</strong><br/>
            Required: <strong>{required_text} ({required_level}/3)</strong>
        </div>
        <div class="progress-bar">
            <div class="progress-fill {'good' if student_level >= required_level else 'improve'}" style="width:{progress_pct}%"></div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
