"""Local semantic search over job offers."""


import re
from functools import lru_cache
from html import unescape

MODEL_NAME = "intfloat/multilingual-e5-small"

@lru_cache(maxsize=1)
def _get_model():
    """Load the model once and reuse it for later searches."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)

def _job_text(job: dict[str, object]) -> str:
    """Prepare the job fields used for semantic comparison."""
    parts = (
        str(job.get("title") or ""),
        str(job.get("technology") or ""),
        str(job.get("description") or ""),
    )
    text = unescape(" ".join(parts))
    return re.sub(r"<[^>]+>", " ", text).strip()


def search_jobs(
    query: str,
    jobs: list[dict[str, object]],
    limit: int = 5,
) -> list[dict[str, object]]:
    """Rank jobs by similarity to a natural-language query."""
    if not query.strip():
        raise ValueError("The search query cannot be empty.")
    if limit < 1:
        raise ValueError("The result limit must be positive.")
    if not jobs:
        return []

    texts = [f"query: {query.strip()}"]
    texts.extend(f"passage: {_job_text(job)}" for job in jobs)

    vectors = _get_model().encode(texts, normalize_embeddings=True)
    query_vector = vectors[0]

    ranked = []
    for job, vector in zip(jobs, vectors[1:], strict=True):
        score = sum(
            float(a) * float(b)
            for a, b in zip(query_vector, vector, strict=True)
        )
        ranked.append({**job, "similarity": round(score, 4)})

    ranked.sort(key=lambda job: job["similarity"], reverse=True)
    return ranked[:limit]