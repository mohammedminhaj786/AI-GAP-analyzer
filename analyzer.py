from sentence_transformers import SentenceTransformer, util
import numpy as np

# Initialize the model once
print("Loading AI Gap Engine...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_match_results(user_skills, job_skills):
    """
    Identifies matched vs missing skills using semantic similarity.
    Works across multiple career domains.
    """
    if not job_skills:
        return [], [], 0
    
    if not user_skills:
        return [], job_skills, 0

    matched = []
    missing = []
    
    # Encode all skills
    user_embeddings = model.encode(user_skills, convert_to_tensor=True)
    job_embeddings = model.encode(job_skills, convert_to_tensor=True)
    
    # Compute cosine similarity matrix
    cosine_scores = util.cos_sim(job_embeddings, user_embeddings)
    
    for i, job_skill in enumerate(job_skills):
        # Best match for this job skill
        best_match_idx = np.argmax(cosine_scores[i].cpu().numpy())
        best_score = cosine_scores[i][best_match_idx].item()
        
        if best_score > 0.75: # Threshold for semantic match
            matched.append(job_skill)
        else:
            missing.append(job_skill)
            
    match_percentage = (len(matched) / len(job_skills)) * 100
    
    return matched, missing, match_percentage

# Knowledge Database for Learning Paths
SKILL_RESOURCES = {
    "Python": {
        "start": "Begin with official documentation or 'Automate the Boring Stuff with Python'.",
        "objective": "Build a CLI application or a simple data scraper.",
        "resources": ["https://www.python.org/about/gettingstarted/", "https://realpython.com/"]
    },
    "Machine Learning": {
        "start": "Take the 'Machine Learning Specialization' by Andrew Ng on Coursera.",
        "objective": "Understand supervised/unsupervised learning and build a linear regression model.",
        "resources": ["https://www.coursera.org/specializations/machine-learning-introduction", "https://scikit-learn.org/stable/tutorial/basic/tutorial.html"]
    },
    "SQL": {
        "start": "Practice queries on Mode Analytics or SQLZoo.",
        "objective": "Design a relational database schema and perform complex JOIN operations.",
        "resources": ["https://mode.com/sql-tutorial/", "https://sqlzoo.net/"]
    },
    "React": {
        "start": "Start with the 'React.dev' documentation and 'Beta' tutorials.",
        "objective": "Build a multi-page interactive web app using functional components and hooks.",
        "resources": ["https://react.dev/learn", "https://www.freecodecamp.org/learn/front-end-development-libraries/react/"]
    },
    "Docker": {
        "start": "Watch 'Docker Tutorial for Beginners' on YouTube (TechWorld with Nana).",
        "objective": "Containerize a full-stack application and orchestrate it using Docker Compose.",
        "resources": ["https://docs.docker.com/get-started/", "https://www.docker.com/101-tutorial/"]
    },
    "Deep Learning": {
        "start": "Study the 'Deep Learning Specialization' and practice with PyTorch/TensorFlow.",
        "objective": "Train a Neural Network for image classification or text generation.",
        "resources": ["https://www.deeplearning.ai/", "https://pytorch.org/tutorials/"]
    }
}

DEFAULT_RESOURCE = {
    "start": "Look for top-rated courses on Udemy or search for 'Beginner's guide to [Skill]' on Roadmap.sh.",
    "objective": "Complete a hands-on project that demonstrates real-world application of this skill.",
    "resources": ["https://roadmap.sh", "https://www.youtube.com/results?search_query=learning+[Skill]"]
}

def get_recommendations(missing_skills, github_score):
    """Provides personalized improvement recommendations."""
    recommendations = []
    
    if not missing_skills:
        recommendations.append("Profile Excellence: You already possess the core technical requirements for this role.")
    else:
        top_missing = missing_skills[:2]
        recommendations.append(f"Strategic Gap: Mastering [bold cyan]{', '.join(top_missing)}[/bold cyan] is your highest priority for this role.")
            
    if github_score < 40:
        recommendations.append("Portfolio Gap: Your GitHub activity is below industry standard for competitive roles. Start pushing daily code.")
    
    return recommendations

def generate_detailed_roadmap(missing_skills):
    """Generates a step-by-step roadmap for missing skills."""
    roadmap = []
    
    for skill in missing_skills:
        info = SKILL_RESOURCES.get(skill, DEFAULT_RESOURCE)
        roadmap.append({
            "skill": skill,
            "how_to_start": info["start"],
            "what_to_achieve": info["objective"],
            "useful_links": info["resources"]
        })
        
    return roadmap
