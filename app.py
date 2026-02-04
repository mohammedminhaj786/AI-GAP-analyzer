import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from utils import get_skills_for_role
from gap_engine import analyze_skill_gap
from job_roles_data import job_roles

st.title("AI Opportunity Gap Analyzer")

# Resume input
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if st.button("Analyze"):

    if uploaded_file is not None:

        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)

        else:
            st.error("Unsupported file format")
            st.stop()

        user_skills = extract_skills_from_resume(resume_text)
        job_skills = get_skills_for_role(role)

        matched, missing, score = analyze_skill_gap(user_skills, job_skills)

        st.success("Analysis Completed")

        st.subheader("Match Score")
        st.write(f"{round(score,2)}%")

        st.subheader("Matched Skills")
        st.write(matched)

        st.subheader("Missing Skills")
        st.write(missing)

    else:
        st.warning("Please upload resume")

# Job role dropdown
role = st.selectbox("Select Target Job Role", list(job_roles.keys()))

if st.button("Analyze"):
    user_skills = extract_skills_from_resume(resume_text)
    job_skills = get_skills_for_role(role)

    matched, missing, score = analyze_skill_gap(user_skills, job_skills)

    st.subheader("Match Score")
    st.write(f"{round(score,2)}%")

    st.subheader("Matched Skills")
    st.write(matched)

    st.subheader("Missing Skills")
    st.write(missing)
