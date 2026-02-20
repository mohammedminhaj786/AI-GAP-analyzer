import argparse
import os
import sys
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills_from_resume
from github_analyzer import analyze_github_profile
from gap_engine import analyze_skill_gap, calculate_career_readiness, generate_recommendations
from utils import get_skills_for_role, calculate_github_score
from job_roles_data import job_roles

def main():
    parser = argparse.ArgumentParser(description="AI Opportunity Gap Analyzer - CLI")
    parser.add_argument("--resume", type=str, required=True, help="Path to resume file (PDF or DOCX)")
    parser.add_argument("--role", type=str, required=True, help=f"Target job role. Options: {', '.join(job_roles.keys())}")
    parser.add_argument("--github", type=str, help="GitHub username")

    args = parser.parse_args()

    if not os.path.exists(args.resume):
        print(f"Error: File not found: {args.resume}")
        sys.exit(1)

    print(f"\n--- Analyzing Resume: {os.path.basename(args.resume)} ---")
    
    # 1. Extract Resume Text
    if args.resume.endswith('.pdf'):
        resume_text = extract_text_from_pdf(args.resume)
    elif args.resume.endswith('.docx'):
        resume_text = extract_text_from_docx(args.resume)
    elif args.resume.endswith('.txt'):
        from resume_parser import extract_text_from_txt
        resume_text = extract_text_from_txt(args.resume)
    else:
        print("Error: Unsupported file format. Use PDF, DOCX, or TXT.")
        sys.exit(1)

    # 2. Extract Skills
    user_skills = extract_skills_from_resume(resume_text)
    job_skills = get_skills_for_role(args.role)

    if not job_skills:
        print(f"Error: Job role '{args.role}' not found. Available roles: {', '.join(job_roles.keys())}")
        sys.exit(1)

    # 3. Analyze Skill Gap
    matched, missing, score = analyze_skill_gap(user_skills, job_skills)

    # 4. GitHub Analysis
    github_data = None
    github_score = 0
    if args.github:
        print(f"--- Analyzing GitHub Profile: {args.github} ---")
        github_data = analyze_github_profile(args.github)
        if github_data:
            github_score = calculate_github_score(github_data)
        else:
            print("Warning: Could not fetch GitHub data.")

    # 5. Career Readiness Score
    career_score = calculate_career_readiness(score, github_score)

    # 6. Generate Recommendations
    recommendations = generate_recommendations(missing, github_score)

    # --- Output Results ---
    print("\n" + "="*50)
    print("AI OPPORTUNITY GAP ANALYSIS RESULTS")
    print("="*50)
    print(f"Target Role:        {args.role}")
    print(f"Resume Score:       {round(score, 2)}%")
    print(f"GitHub Score:       {github_score}%")
    print(f"Overall Readiness:  {career_score}%")
    print("-" * 50)
    
    print("\n[MATCHED SKILLS]:")
    if matched:
        for s in matched: print(f"  * {s}")
    else:
        print("  None")

    print("\n[MISSING SKILLS]:")
    if missing:
        for s in missing: print(f"  * {s}")
    else:
        print("  None (Perfect match!)")

    if github_data:
        print("\n[GITHUB INSIGHTS]:")
        print(f"  Public Repos:  {github_data['total_repos']}")
        print(f"  Total Stars:   {github_data['total_stars']}")
        print(f"  Top Languages: {', '.join(github_data['languages'].keys())}")

    print("\n[RECOMMENDATIONS]:")
    for rec in recommendations:
        print(f"  > {rec}")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
