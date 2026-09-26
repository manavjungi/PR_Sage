def build_review_prompt(diff_text: str) -> str:
    return f"""You are a senior software engineer reviewing a GitHub pull request.
Review ONLY the following diff. Point out bugs, edge cases, style issues,
and security concerns. Be concise and use markdown bullet points.
If the code looks good, say so briefly.

DIFF:
{diff_text}
"""