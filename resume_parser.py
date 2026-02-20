import PyPDF2
import docx
import os
import re

# Extensive Skill Database for Multi-domain Support
SKILL_DATA = {
    "Technical": [
        "Python", "Java", "C++", "JavaScript", "TypeScript", "Go", "Rust", "SQL", "NoSQL", 
        "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD",
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Pandas", "NumPy"
    ],
    "Tools": ["Git", "GitHub", "Jira", "Postman", "Tableau", "PowerBI", "Matplotlib", "Seaborn"],
    "Soft Skills": ["Project Management", "Agile", "Scrum", "Communication", "Leadership", "Critical Thinking"]
}

def extract_text(file_path):
    """Extract text from PDF, DOCX, or TXT."""
    if not os.path.exists(file_path):
        return ""
    
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + " "
        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = " ".join([p.text for p in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return text

def extract_skills(text):
    """Extract skills from text using pattern matching."""
    found_skills = set()
    text_lower = text.lower()
    
    for category, skills in SKILL_DATA.items():
        for skill in skills:
            # Use regex for better matching (word boundaries)
            pattern = rf"\b{re.escape(skill.lower())}\b"
            if re.search(pattern, text_lower):
                found_skills.add(skill)
                
    return list(found_skills)
