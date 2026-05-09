"""EmbeddingService protocol — vector embeddings + similarity search.

APEX-M satisfies via Eventhouse SLM `ai_embeddings` plugin (preview Jan
2026) for in-data-tier embeddings, with Azure OpenAI embeddings as the
external option.
APEX-G satisfies via Vertex AI text-embedding-005.
APEX-A satisfies via AWS Bedrock Titan Embeddings.

The Pricer (RC-E2E-03) is the canonical heavy consumer — episodic memory
similarity search for past pricing decisions per Services Guide §25.8.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Embedding:
    vector: list[float]
    dim: int
    model: str          # e.g., "ai_embeddings:slm-v1" or "text-embedding-005"
    text_hash: str      # content-addressed input hash


@dataclass(frozen=True)
class SimilarityResult:
    text_hash: str      # the hit
    score: float        # cosine similarity, 0..1
    metadata: dict[str, str]


@runtime_checkable
class EmbeddingService(Protocol):
    """Embed text and run similarity search."""

    variant: str
    model_default: str

    def embed(self, *, text: str, model: str | None = None) -> Embedding:
        """Compute the embedding for one text."""
        ...

    def embed_batch(self, *, texts: list[str], model: str | None = None) -> list[Embedding]:
        """Batch variant — preferred for high-volume."""
        ...

    def similarity_search(
        self,
        *,
        query: str | Embedding,
        index: str,
        top_k: int = 10,
        filter: dict[str, str] | None = None,
    ) -> list[SimilarityResult]:
        """Top-K similar items from the named index."""
        ...
