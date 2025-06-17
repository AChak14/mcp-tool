import requests
from datetime import datetime
from typing import List, Dict

API_URL = "https://api.github.com/repos/{repo}/issues"


def get_open_issues(repo: str) -> List[Dict]:
    """Fetch open issues from the GitHub repository."""
    issues = []
    page = 1
    while True:
        url = API_URL.format(repo=repo)
        params = {"state": "open", "page": page, "per_page": 30}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
    return issues


def parse_issue(issue: Dict) -> Dict:
    """Extract relevant info from a GitHub issue."""
    return {
        "id": issue.get("number"),
        "title": issue.get("title"),
        "body": issue.get("body"),
        "created_at": issue.get("created_at"),
        "url": issue.get("html_url"),
        "company": issue.get("user", {}).get("login"),
    }
