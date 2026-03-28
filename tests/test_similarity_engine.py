from unittest.mock import Mock

from app.services.similarity_engine import SimilarityEngine


def test_similarity_engine_basic():
    """Test similarity computation with mocked embeddings."""

    # Mock embedding model
    mock_embedding_model = Mock()

    # Define fake embeddings
    # Same vectors → similarity should be 1
    mock_embedding_model.encode.side_effect = [
        [1.0, 0.0, 0.0],  # resume embedding
        [1.0, 0.0, 0.0],  # jd embedding
    ]

    engine = SimilarityEngine(mock_embedding_model)

    result = engine.compute_similarity(
        "resume text",
        "job description text"
    )

    assert result["cosine_similarity"] == 1.0
    assert result["match_score"] == 100.0


def test_similarity_engine_opposite_vectors():
    """Test completely opposite vectors."""

    mock_embedding_model = Mock()

    mock_embedding_model.encode.side_effect = [
        [1.0, 0.0],
        [-1.0, 0.0],
    ]

    engine = SimilarityEngine(mock_embedding_model)

    result = engine.compute_similarity("a", "b")

    assert round(result["cosine_similarity"], 2) == -1.0
    assert result["match_score"] == 0.0


def test_similarity_engine_orthogonal_vectors():
    """Test orthogonal vectors (no similarity)."""

    mock_embedding_model = Mock()

    mock_embedding_model.encode.side_effect = [
        [1.0, 0.0],
        [0.0, 1.0],
    ]

    engine = SimilarityEngine(mock_embedding_model)

    result = engine.compute_similarity("a", "b")

    assert round(result["cosine_similarity"], 2) == 0.0
    assert result["match_score"] == 50.0


def test_similarity_engine_zero_vector():
    """Test handling of zero vectors."""

    mock_embedding_model = Mock()

    mock_embedding_model.encode.side_effect = [
        [0.0, 0.0],
        [1.0, 1.0],
    ]

    engine = SimilarityEngine(mock_embedding_model)

    result = engine.compute_similarity("a", "b")

    assert result["cosine_similarity"] == 0.0
    assert result["match_score"] == 50.0