import os
import subprocess
import requests
import google.generativeai as genai

# --- Config ---
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]
PR_NUMBER = os.environ["PR_NUMBER"]
BASE_SHA = os.environ["BASE_SHA"]
HEAD_SHA = os.environ["HEAD_SHA"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_diff():
    result = subprocess.run(
        ["git", "diff", BASE_SHA, HEAD_SHA],
        capture_output=True, text=True
    )
    return result.stdout[:15000]  # truncate to keep prompt reasonable

def review_diff(diff_text):
    prompt = f"""You are a senior software engineer reviewing a GitHub pull request.
Review ONLY the following diff. Point out bugs, edge cases, style issues,
and security concerns. Be concise and use markdown bullet points.
If the code looks good, say so briefly.

DIFF:
{diff_text}
"""
    response = model.generate_content(prompt)
    return response.text

def post_comment(body):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"body": f"### 🤖 AI Code Review\n\n{body}"}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()

if __name__ == "__main__":
    diff = get_diff()
    x = 10  
    if not diff.strip():
        print("No diff found, skipping review.")
    else:
        review = review_diff(diff)
        post_comment(review)
        print("Review posted successfully.")
