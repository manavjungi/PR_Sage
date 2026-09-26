import requests

def post_comment(repo: str, pr_number: str, token: str, body: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"body": f"### 🤖 AI Code Review\n\n{body}"}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()