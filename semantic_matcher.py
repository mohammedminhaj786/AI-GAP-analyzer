from sentence_transformers import SentenceTransformer, util

# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_skill_match(user_skills, job_skills):
    matched_skills = []
    
    # Encode user skills once
    user_embeddings = {skill: model.encode(skill, convert_to_tensor=True) for skill in user_skills}
    
    for job_skill in job_skills:
        job_embedding = model.encode(job_skill, convert_to_tensor=True)
        
        # Check if job_skill matches any user_skill
        for user_skill, user_embedding in user_embeddings.items():
            similarity = util.cos_sim(job_embedding, user_embedding)
            
            if similarity.item() > 0.7:
                matched_skills.append(job_skill)
                break  # Only add once per job_skill

    return matched_skills