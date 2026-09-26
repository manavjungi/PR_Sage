import subprocess

def get_diff(base_sha: str, head_sha: str, max_chars: int = 15000) -> str:
    """Return the git diff between two commits, truncated to a safe prompt size."""
    result = subprocess.run(
        ["git", "diff", base_sha, head_sha],
        capture_output=True, text=True
    )
    return result.stdout[:max_chars]