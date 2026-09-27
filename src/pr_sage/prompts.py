def build_review_prompt(diff_text: str, context_chunks: list[dict] | None = None) -> str:
    context_block = ""
    if context_chunks:
        formatted = "\n\n".join(
            f"--- {c['file']} ---\n{c['content']}" for c in context_chunks
        )
        context_block = f"""
RELEVANT CODEBASE CONTEXT (for reference — not part of the change itself):
{formatted}
"""

    return f"""You are a senior software engineer reviewing a GitHub pull request.
{context_block}
Review the following diff. Point out bugs, edge cases, style issues, and any
inconsistencies with the rest of the codebase shown above (e.g. if a changed
function is used elsewhere in a way this diff breaks). Be concise, use markdown
bullet points. If the code looks good, say so briefly.

DIFF:
{diff_text}
"""