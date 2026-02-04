from utils import SKILL_DATABASE

def extract_skills_from_resume(resume_text):
    found_skills = []

    resume_text = resume_text.lower()

    for skill in SKILL_DATABASE:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills
