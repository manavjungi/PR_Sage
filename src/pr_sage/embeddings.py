import google.generativeai as genai

EMBED_MODEL = "models/text-embedding-004"


def embed_text(text: str) -> list[float]:
    """Get an embedding vector for a single piece of text."""
    result = genai.embed_content(model=EMBED_MODEL, content=text)
    return result["embedding"]


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Embed each chunk's content; return chunks with an added 'embedding' key."""
    embedded = []
    for chunk in chunks:
        try:
            vector = embed_text(chunk["content"])
            embedded.append({**chunk, "embedding": vector})
        except Exception as e:
            print(f"Skipping {chunk['file']} (embedding failed: {e})")
    return embedded