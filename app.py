from resume_parser import extract_skills_from_resume
from utils import get_skills_for_role
from gap_engine import analyze_skill_gap

# ---- Sample Resume ----
resume_text = """
I have experience in Python, Pandas and GitHub.
"""

# ---- User Job Role ----
role = input("Enter target job role: ")

# ---- Extract User Skills ----
user_skills = extract_skills_from_resume(resume_text)

# ---- Get Job Skills ----
job_skills = get_skills_for_role(role)

# ---- Analyze Gap ----
matched, missing, score = analyze_skill_gap(user_skills, job_skills)

print("\nMatched Skills:")
for skill in matched:
    print("-", skill)

print("\nMissing Skills:")
for skill in missing:
    print("-", skill)

print("\nMatch Score:", round(score, 2), "%")

