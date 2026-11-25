
"""Prepare and ingest Carnatic music knowledge into PostgreSQL."""

import asyncio
import logging
from typing import Any

from sqlalchemy.dialects.postgresql import insert

from app.database.connection import SessionLocal
from app.knowledge import (
    ALL_COMPOSITIONS,
    ALL_RAGAS,
    ALL_SWARAS,
    ALL_TALAS,
    GENERAL_REFERENCE,
)
from app.models import KnowledgeEmbedding
from app.services.embedding import EmbeddingService


logger = logging.getLogger(__name__)

EMBEDDING_BATCH_SIZE = 50


def serialize_record(record: dict[str, Any]) -> str:
    """Convert a knowledge record into searchable text."""

    sections = []

    for key, value in record.items():
        if value is None or value == "":
            continue

        if isinstance(value, (list, tuple)):
            value = ", ".join(str(item) for item in value)

        elif isinstance(value, dict):
            value = "; ".join(
                f"{nested_key}: {nested_value}"
                for nested_key, nested_value in value.items()
            )

        sections.append(
            f"{key.replace('_', ' ').title()}: {value}"
        )

    return "\n".join(sections)


def build_knowledge_documents() -> list[dict[str, Any]]:
    """Build searchable documents from all knowledge categories."""

    documents = []

    catalogues = {
        "raga": ALL_RAGAS,
        "tala": ALL_TALAS,
        "swara": ALL_SWARAS,
        "composition": ALL_COMPOSITIONS,
    }

    for source_type, records in catalogues.items():
        for index, record in enumerate(records):
            name = (
                record.get("name")
                or record.get("symbol")
                or f"{source_type}_{index + 1}"
            )

            source_id = str(record.get("id", name))

            content = (
                f"Carnatic music knowledge category: {source_type}\n"
                f"{serialize_record(record)}"
            )

            documents.append(
                {
                    "source_type": source_type,
                    "source_id": source_id,
                    "content": content,
                    "metadata": {
                        "name": name,
                        "category": source_type,
                    },
                }
            )

    documents.append(
        {
            "source_type": "general_reference",
            "source_id": "general_reference",
            "content": GENERAL_REFERENCE,
            "metadata": {
                "name": "General Carnatic Music Reference",
                "category": "general_reference",
            },
        }
    )

    return documents


async def ingest_knowledge() -> int:
    """Generate embeddings and upsert knowledge into PostgreSQL."""

    documents = build_knowledge_documents()

    embedding_service = EmbeddingService()
    session = SessionLocal()

    try:
        for start in range(
            0,
            len(documents),
            EMBEDDING_BATCH_SIZE,
        ):
            batch = documents[
                start:start + EMBEDDING_BATCH_SIZE
            ]

            embeddings = await embedding_service.generate_embeddings(
                [document["content"] for document in batch]
            )

            records = [
                {
                    "source_type": document["source_type"],
                    "source_id": document["source_id"],
                    "content": document["content"],
                    "embedding": embedding,
                    "metadata_json": document["metadata"],
                }
                for document, embedding in zip(
                    batch,
                    embeddings,
                )
            ]

            statement = insert(
                KnowledgeEmbedding
            ).values(records)

            statement = statement.on_conflict_do_update(
                constraint="uq_knowledge_source",
                set_={
                    "content": statement.excluded.content,
                    "embedding": statement.excluded.embedding,
                    "metadata_json": statement.excluded.metadata_json,
                },
            )

            session.execute(statement)
            session.commit()

            logger.info(
                "Ingested knowledge records %s to %s of %s",
                start + 1,
                start + len(batch),
                len(documents),
            )

        return len(documents)

    except Exception:
        session.rollback()
        logger.exception("Knowledge ingestion failed.")
        raise

    finally:
        session.close()
        await embedding_service.close()


if __name__ == "__main__":
    total = asyncio.run(ingest_knowledge())
    print(f"Successfully ingested {total} knowledge documents.")
