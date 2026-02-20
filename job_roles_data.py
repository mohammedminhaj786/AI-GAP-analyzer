JOB_ROLES = {
    "Data Scientist": [
        "Python", "Machine Learning", "SQL", "Statistics", "Data Visualization", 
        "Pandas", "NumPy", "Scikit-Learn", "Feature Engineering"
    ],
    "AI Engineer": [
        "Python", "Deep Learning", "TensorFlow", "PyTorch", "NLP", 
        "LLMs", "Computer Vision", "MLOps", "Model Deployment"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", 
        "Redux", "Tailwind CSS", "Responsive Design", "UI/UX"
    ],
    "Backend Developer": [
        "Python", "Node.js", "Express", "PostgreSQL", "MongoDB", 
        "REST API", "Docker", "FastAPI", "Authentication"
    ],
    "Cloud Architect": [
        "AWS", "Terraform", "Kubernetes", "Docker", "Networking", 
        "IAM", "Serverless", "Security", "CloudFormation"
    ]
}

def get_job_roles():
    return list(JOB_ROLES.keys())

def get_skills_for_role(role):
    return JOB_ROLES.get(role, [])
