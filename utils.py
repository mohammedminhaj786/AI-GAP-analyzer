from job_roles_data import job_roles

def get_skills_for_role(role):
    return job_roles.get(role, [])

SKILL_DATABASE = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Statistics",
    "Pandas",
    "NumPy",
    "SQL",
    "NLP",
    "Computer Vision",
    "TensorFlow",
    "PyTorch",
    "Git",
    "GitHub",
    "Data Visualization",
    "Matplotlib",
    "Seaborn"
]

