from gemini_client import get_client
from retry_utils import retry_with_backoff

EMBED_MODEL = "gemini-embedding-001"


@retry_with_backoff(max_attempts=3, base_delay=2.0)
def embed_text(text: str) -> list[float]:
    client = get_client()
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=text,
    )
    return result.embeddings[0].values


def embed_chunks(chunks: list[dict]) -> list[dict]:
    embedded = []
    for chunk in chunks:
        try:
            vector = embed_text(chunk["content"])
            embedded.append({**chunk, "embedding": vector})
        except Exception as e:
            print(f"Skipping {chunk['file']} (embedding failed after retries: {e})")
    return embedded