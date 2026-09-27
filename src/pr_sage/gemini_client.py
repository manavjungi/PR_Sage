from google import genai

_client = None


def configure(api_key: str):
    global _client
    _client = genai.Client(api_key=api_key)


def get_client() -> genai.Client:
    if _client is None:
        raise RuntimeError("Gemini client not configured. Call configure() first.")
    return _client