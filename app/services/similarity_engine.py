from typing import Dict

import numpy as np
from loguru import logger

from app.models.embedding_model import EmbeddingModel


class SimilarityEngine:
    """Computes semantic similarity between resume and job description."""

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        """Initialize with embedding model."""
        self.embedding_model = embedding_model

    def compute_similarity(self, resume_text: str, jd_text: str) -> Dict[str, float]:
        """Compute normalized similarity score between resume and JD."""

        logger.debug("Computing semantic similarity")

        resume_embedding = self.embedding_model.encode(resume_text)
        jd_embedding = self.embedding_model.encode(jd_text)

        similarity = self._cosine_similarity(resume_embedding, jd_embedding)

        normalized_score = self._normalize_score(similarity)

        return {
            "cosine_similarity": similarity,
            "match_score": normalized_score,
        }

    def _cosine_similarity(self, vec1, vec2) -> float:
        """Compute cosine similarity."""
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return float(dot_product / (norm_v1 * norm_v2))

    def _normalize_score(self, similarity: float) -> float:
        """Convert cosine similarity (-1 to 1) → (0 to 100)."""
        return round((similarity + 1) * 50, 2)