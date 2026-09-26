import os
import sys

from diff_utils import get_diff
from prompts import build_review_prompt
from llm_client import configure, generate_review
from github_api import post_comment

def main():
    gemini_key = os.environ["GEMINI_API_KEY"]
    github_token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["REPO"]
    pr_number = os.environ["PR_NUMBER"]
    base_sha = os.environ["BASE_SHA"]
    head_sha = os.environ["HEAD_SHA"]

    configure(gemini_key)

    diff = get_diff(base_sha, head_sha)
    if not diff.strip():
        print("No diff found, skipping review.")
        return

    prompt = build_review_prompt(diff)
    review = generate_review(prompt)

    post_comment(repo, pr_number, github_token, review)
    print("Review posted successfully.")

if __name__ == "__main__":
    sys.exit(main() or 0)