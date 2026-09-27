from pathlib import Path

# Extend this list if your repo uses other languages
CODE_EXTENSIONS = (".py", ".js", ".ts", ".java", ".go")

# Folders we never want to pull code context from
IGNORE_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache"}


def chunk_repo(root_dir: str = ".", max_chunk_chars: int = 4000) -> list[dict]:
    """
    Walk the repo starting at root_dir and return one chunk per source file.
    Each chunk is {"file": relative_path, "content": file_text}.
    """
    chunks = []
    root = Path(root_dir)

    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix not in CODE_EXTENSIONS:
            continue

        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        if not content.strip():
            continue

        chunks.append({
            "file": str(path.relative_to(root)),
            "content": content[:max_chunk_chars],
        })

    return chunks