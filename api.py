from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import shutil
import os
import aiofiles

# Use the robust modules we built
from resume_parser import extract_text, extract_skills
from github_analyzer import analyze_github, calculate_github_score
from analyzer import get_match_results, get_recommendations, generate_detailed_roadmap
from job_roles_data import get_job_roles, get_skills_for_role

app = FastAPI(
    title="AI Opportunity Gap Analyzer",
    description="A powerful career analysis engine with AI semantic matching.",
    version="2.0",
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure 'uploads' directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

@app.get("/roles")
def get_roles():
    """Return available job roles for the dropdown."""
    return get_job_roles()

@app.post("/analyze")
async def analyze_career(
    job_role: str = Form(...),
    github_username: str = Form(None),
    resume: UploadFile = File(...)
):
    try:
        # 1. Save and Process Resume
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await resume.read()
            await out_file.write(content)

        resume_text = extract_text(file_path)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume.")

        # 2. Extract Skills
        user_skills = extract_skills(resume_text)
        job_skills = get_skills_for_role(job_role)
        
        if not job_skills:
            raise HTTPException(status_code=404, detail=f"Job role '{job_role}' not found.")

        # 3. Analyze Skill Gap (The robust AI engine)
        matched, missing, match_score = get_match_results(user_skills, job_skills)

        # 4. GitHub Analysis
        gh_data = None
        gh_score = 0
        if github_username:
            gh_data = analyze_github(github_username)
            gh_score = calculate_github_score(gh_data)

        # 5. Generate Recommendations
        recommendations = get_recommendations(missing, gh_score)
        
        # 6. Generate Detailed Roadmap
        roadmap = generate_detailed_roadmap(missing)
        
        # Calculate Readiness
        readiness_score = round((match_score * 0.7) + (gh_score * 0.3), 1)

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "role": job_role,
            "readiness_score": readiness_score,
            "resume_score": round(match_score, 1),
            "github_score": round(gh_score, 1),
            "matched_skills": matched,
            "missing_skills": missing,
            "github_data": gh_data,
            "recommendations": recommendations, 
            "roadmap": roadmap,
            "user_skills_detected": user_skills # Helpful for debugging/User display
        }

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
