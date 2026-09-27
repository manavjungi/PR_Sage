import subprocess

def get_diff(base_sha: str, head_sha: str, repo_path: str = "../../", max_chars: int = 15000) -> str:
    """Return the git diff between two commits, run inside repo_path."""
    result = subprocess.run(
        ["git", "diff", base_sha, head_sha],
        capture_output=True, text=True,
        cwd=repo_path,
    )
    return result.stdout[:max_chars]