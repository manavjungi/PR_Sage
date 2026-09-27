import numpy as np


def cosine_sim(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def get_top_k_chunks(query_embedding: list[float], embedded_chunks: list[dict], k: int = 3) -> list[dict]:
    """Return the k chunks most similar to the query embedding."""
    if not embedded_chunks:
        return []

    scored = [
        (cosine_sim(query_embedding, c["embedding"]), c)
        for c in embedded_chunks
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]