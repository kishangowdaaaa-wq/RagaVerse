
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.embedding import EmbeddingService
from app.services.semantic_search import SemanticSearchService


@pytest.mark.parametrize("text", ["", "   "])
def test_embedding_rejects_empty_text(text):
    service = EmbeddingService.__new__(EmbeddingService)
    service.generate_embeddings = AsyncMock()

    with pytest.raises(ValueError):
        import asyncio
        asyncio.run(service.generate_embedding(text))


def test_embedding_generates_local_document_embeddings():
    import asyncio

    service = EmbeddingService.__new__(EmbeddingService)
    service.model = "nomic-embed-text"
    service.dimensions = 768
    service.client = MagicMock()

    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "embeddings": [[0.1] * 768, [0.2] * 768]
    }

    service.client.post = AsyncMock(return_value=response)

    embeddings = asyncio.run(
        service.generate_embeddings(
            ["Kalyani raga", "Adi tala"]
        )
    )

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 768

    request = service.client.post.call_args
    assert request.kwargs["json"]["model"] == "nomic-embed-text"
    assert request.kwargs["json"]["input"][0].startswith(
        "search_document:"
    )


def test_embedding_generates_query_with_search_prefix():
    import asyncio

    service = EmbeddingService.__new__(EmbeddingService)
    service.model = "nomic-embed-text"
    service.dimensions = 768
    service.client = MagicMock()

    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "embeddings": [[0.1] * 768]
    }

    service.client.post = AsyncMock(return_value=response)

    embedding = asyncio.run(
        service.generate_embedding("Explain Kalyani")
    )

    assert len(embedding) == 768

    request = service.client.post.call_args
    assert request.kwargs["json"]["input"] == [
        "search_query: Explain Kalyani"
    ]


def test_semantic_search_rejects_empty_question():
    import asyncio

    service = SemanticSearchService()

    with pytest.raises(ValueError):
        asyncio.run(service.search(""))


def test_semantic_search_rejects_invalid_limit():
    import asyncio

    service = SemanticSearchService()

    with pytest.raises(ValueError):
        asyncio.run(
            service.search(
                question="Explain Kalyani",
                limit=25,
            )
        )


def test_semantic_search_returns_retrieved_records():
    import asyncio

    embedding_service = MagicMock()
    embedding_service.generate_embedding = AsyncMock(
        return_value=[0.1] * 768
    )
    embedding_service.close = AsyncMock()

    knowledge_record = SimpleNamespace(
        content="Kalyani: S R2 G3 M2 P D2 N3 S",
        source_type="raga",
        source_id="Kalyani",
        metadata_json={"name": "Kalyani"},
    )

    result_row = SimpleNamespace(
        KnowledgeEmbedding=knowledge_record,
        distance=0.2,
    )

    session = MagicMock()
    session.execute.return_value.all.return_value = [
        result_row
    ]

    session_context = MagicMock()
    session_context.__enter__.return_value = session
    session_context.__exit__.return_value = False

    with patch(
        "app.services.semantic_search.EmbeddingService",
        return_value=embedding_service,
    ), patch(
        "app.services.semantic_search.SessionLocal",
        return_value=session_context,
    ):
        results = asyncio.run(
            SemanticSearchService().search(
                "Explain Kalyani",
                limit=5,
            )
        )

    assert len(results) == 1
    assert results[0]["source_type"] == "raga"
    assert results[0]["source_id"] == "Kalyani"
    assert results[0]["metadata"]["name"] == "Kalyani"
    assert results[0]["similarity"] == 0.8

    embedding_service.close.assert_awaited_once()
