
"""Hybrid semantic and keyword search for RagaVerse."""

import logging
import re
from typing import Any

from sqlalchemy import case, func, select

from app.database.connection import SessionLocal
from app.models import KnowledgeEmbedding
from app.services.embedding import EmbeddingService


logger = logging.getLogger(__name__)

STOP_WORDS = {
    "a", "an", "and", "are", "as", "be", "by",
    "can", "do", "for", "from", "has", "how",
    "in", "is", "it", "of", "on", "or", "the",
    "to", "what", "which", "who", "with",
    "explain", "describe", "tell", "about",
    "carnatic", "music", "basic", "ascending",
    "descending", "scale",
}


class SemanticSearchService:
    """Retrieve relevant knowledge using hybrid search."""

    async def search(
        self,
        question: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Find relevant records using semantic and keyword ranking."""

        if not question or not question.strip():
            raise ValueError(
                "Search question cannot be empty."
            )

        if not 1 <= limit <= 20:
            raise ValueError(
                "Search limit must be between 1 and 20."
            )

        embedding_service = EmbeddingService()

        try:
            query_embedding = (
                await embedding_service.generate_embedding(
                    question.strip()
                )
            )

            distance = (
                KnowledgeEmbedding.embedding.cosine_distance(
                    query_embedding
                )
            )

            keywords = [
                word
                for word in re.findall(
                    r"[a-zA-Z0-9]+",
                    question.casefold(),
                )
                if word not in STOP_WORDS and len(word) > 1
            ]

            keyword_score = sum(
                (
                    case(
                        (
                            func.lower(
                                KnowledgeEmbedding.content
                            ).contains(keyword),
                            1,
                        ),
                        else_=0,
                    )
                    for keyword in keywords
                ),
                start=0,
            )

            statement = (
                select(
                    KnowledgeEmbedding,
                    distance.label("distance"),
                )
                .order_by(
                    keyword_score.desc(),
                    distance.asc(),
                )
                .limit(limit)
            )

            with SessionLocal() as session:
                rows = session.execute(statement).all()

                return [
                    {
                        "content": row.KnowledgeEmbedding.content,
                        "source_type": (
                            row.KnowledgeEmbedding.source_type
                        ),
                        "source_id": (
                            row.KnowledgeEmbedding.source_id
                        ),
                        "metadata": (
                            row.KnowledgeEmbedding.metadata_json
                        ),
                        "similarity": round(
                            1 - float(row.distance),
                            4,
                        ),
                    }
                    for row in rows
                ]

        except Exception:
            logger.exception(
                "Hybrid knowledge search failed."
            )
            raise

        finally:
            await embedding_service.close()
