from gemini_client import get_client

MODEL_NAME = "gemini-flash-latest"


def generate_review(prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text