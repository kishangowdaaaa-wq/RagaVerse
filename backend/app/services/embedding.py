
"""Local Ollama embedding generation service for RagaVerse."""

import logging

import httpx

from app.core.config import get_settings


logger = logging.getLogger(__name__)


class EmbeddingService:
    """Generate document and query embeddings using local Ollama."""

    def __init__(self) -> None:
        settings = get_settings()

        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions
        self.base_url = settings.ollama_base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=settings.llm_timeout_seconds,
        )

    async def _generate(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for already-prefixed texts."""

        if not texts:
            return []

        response = await self.client.post(
            "/api/embed",
            json={
                "model": self.model,
                "input": texts,
            },
        )

        response.raise_for_status()

        embeddings = response.json().get("embeddings", [])

        if len(embeddings) != len(texts):
            raise ValueError(
                "Ollama returned an unexpected number of embeddings."
            )

        if any(
            len(embedding) != self.dimensions
            for embedding in embeddings
        ):
            raise ValueError(
                "Ollama returned an unexpected embedding dimension."
            )

        return embeddings

    async def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
        """Generate an embedding for a search query."""

        if not text or not text.strip():
            raise ValueError(
                "Cannot generate an embedding for empty text."
            )

        try:
            embeddings = await self._generate(
                [f"search_query: {text.strip()}"]
            )
            return embeddings[0]

        except Exception:
            logger.exception(
                "Local Ollama query embedding generation failed."
            )
            raise

    async def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for knowledge documents."""

        if not texts:
            return []

        if any(not text or not text.strip() for text in texts):
            raise ValueError(
                "All texts must contain non-empty content."
            )

        try:
            prefixed_texts = [
                f"search_document: {text.strip()}"
                for text in texts
            ]

            return await self._generate(prefixed_texts)

        except Exception:
            logger.exception(
                "Local Ollama document embedding generation failed."
            )
            raise

    async def close(self) -> None:
        """Close the asynchronous HTTP client."""

        await self.client.aclose()
