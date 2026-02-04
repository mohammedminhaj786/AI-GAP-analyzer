import requests

GITHUB_API_URL = "https://api.github.com/users/"

def analyze_github_profile(username):
    user_url = GITHUB_API_URL + username
    repos_url = user_url + "/repos"

    user_response = requests.get(user_url)
    repos_response = requests.get(repos_url)

    if user_response.status_code != 200:
        return None

    user_data = user_response.json()
    repos_data = repos_response.json()

    total_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)

    languages = {}
    total_stars = 0

    for repo in repos_data:
        lang = repo.get("language")
        stars = repo.get("stargazers_count", 0)

        total_stars += stars

        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    return {
        "total_repos": total_repos,
        "followers": followers,
        "languages": languages,
        "total_stars": total_stars
    }
