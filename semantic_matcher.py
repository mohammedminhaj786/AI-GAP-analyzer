from sentence_transformers import SentenceTransformer, util

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_skill_match(user_skills, job_skills):
    matched_skills = []

    for job_skill in job_skills:
        job_embedding = model.encode(job_skill, convert_to_tensor=True)

        for user_skill in user_skills:
            user_embedding = model.encode(user_skill, convert_to_tensor=True)

            similarity = util.cos_sim(job_embedding, user_embedding)

            if similarity.item() > 0.7:
                matched_skills.append(job_skill)

    return list(set(matched_skills))
