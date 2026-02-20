import requests

def analyze_github(username):
    """
    Evaluates GitHub contributions and activity.
    Returns a dictionary of metrics or None if user not found.
    """
    if not username:
        return None
        
    base_url = f"https://api.github.com/users/{username}"
    
    try:
        user_res = requests.get(base_url)
        if user_res.status_code != 200:
            return None
            
        user_data = user_res.json()
        repos_res = requests.get(f"{base_url}/repos")
        repos_data = repos_res.json() if repos_res.status_code == 200 else []
        
        languages = {}
        stars = 0
        
        for repo in repos_data:
            stars += repo.get("stargazers_count", 0)
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        # Sort languages by frequency
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        top_langs = [l[0] for l in sorted_langs[:5]]
        
        return {
            "username": username,
            "name": user_data.get("name", username),
            "public_repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "total_stars": stars,
            "top_languages": top_langs,
            "bio": user_data.get("bio", ""),
            "profile_url": user_data.get("html_url", "")
        }
    except Exception as e:
        print(f"GitHub Analysis Error: {e}")
        return None

def calculate_github_score(data):
    """Calculate a score from 0-100 based on activity."""
    if not data:
        return 0
        
    score = 0
    # Higher weighted components
    score += min(data["public_repos"] * 5, 40)  # Up to 40 pts for repos
    score += min(data["total_stars"] * 10, 30)  # Up to 30 pts for stars
    score += min(len(data["top_languages"]) * 6, 30) # Up to 30 pts for variety
    
    return min(score, 100)
