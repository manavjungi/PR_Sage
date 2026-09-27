from gemini_client import get_client
from retry_utils import retry_with_backoff

MODEL_NAME = "gemini-flash-latest"


@retry_with_backoff(max_attempts=3, base_delay=2.0)
def generate_review(prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text