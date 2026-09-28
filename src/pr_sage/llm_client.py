from gemini_client import get_client
from retry_utils import retry_with_backoff

# Tried in order: if the first is overloaded, fall back to the next
MODEL_NAMES = ["gemini-flash-latest", "gemini-3.1-flash-lite"]


@retry_with_backoff(max_attempts=4, base_delay=3.0)
def _generate_with_retry(model: str, prompt: str) -> str:
    client = get_client()
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text


def generate_review(prompt: str) -> str:
    last_error = None
    for model in MODEL_NAMES:
        try:
            return _generate_with_retry(model, prompt)
        except Exception as e:
            print(f"Model {model} failed: {e}")
            last_error = e
    raise last_error