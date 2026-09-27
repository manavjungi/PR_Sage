import os
import sys

from diff_utils import get_diff
from chunker import chunk_repo
from embeddings import embed_text, embed_chunks
from retriever import get_top_k_chunks
from prompts import build_review_prompt
from gemini_client import configure
from llm_client import generate_review
from github_api import post_comment


def main():
    gemini_key = os.environ["GEMINI_API_KEY"]
    github_token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["REPO"]
    pr_number = os.environ["PR_NUMBER"]
    base_sha = os.environ["BASE_SHA"]
    head_sha = os.environ["HEAD_SHA"]

    # New: where is the repo we're actually reviewing?
    # Defaults to "../../" so your own PR_Sage workflow keeps working unchanged.
    target_repo_path = os.environ.get("TARGET_REPO_PATH", "../../")
    top_k = int(os.environ.get("TOP_K", "3"))

    configure(gemini_key)

    diff = get_diff(base_sha, head_sha, repo_path=target_repo_path)
    if not diff.strip():
        print("No diff found, skipping review.")
        return

    print(f"Chunking repo at {target_repo_path}...")
    chunks = chunk_repo(root_dir=target_repo_path)
    print(f"Found {len(chunks)} chunks. Embedding...")
    embedded_chunks = embed_chunks(chunks)

    print("Embedding diff for retrieval...")
    diff_embedding = embed_text(diff)
    top_chunks = get_top_k_chunks(diff_embedding, embedded_chunks, k=top_k)
    print(f"Retrieved context from: {[c['file'] for c in top_chunks]}")

    prompt = build_review_prompt(diff, context_chunks=top_chunks)
    review = generate_review(prompt)

    post_comment(repo, pr_number, github_token, review)
    print("Review posted successfully.")


if __name__ == "__main__":
    sys.exit(main() or 0)