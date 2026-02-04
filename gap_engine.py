def analyze_skill_gap(user_skills, job_skills):
    matched = []
    missing = []

    if not job_skills:
        return matched, missing, 0

    for skill in job_skills:
        if skill in user_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    match_score = (len(matched) / len(job_skills)) * 100

    return matched, missing, match_score
