
"""Knowledge retrieval helpers for the Carnatic reference catalogue."""

import logging

from app.database.connection import SessionLocal
from app.knowledge.catalog import ALL_RAGAS, GENERAL_REFERENCE
from app.models import KnowledgeEmbedding
from app.services.semantic_search import SemanticSearchService


logger = logging.getLogger(__name__)


def get_knowledge_context(question: str) -> str:
    """Return relevant catalogue entries using exact name matching."""

    normalized_question = question.casefold()
    matches = []

    for raga in ALL_RAGAS:
        search_terms = [
            raga["name"],
            *raga.get("aliases", []),
        ]

        if any(
            term.casefold() in normalized_question
            for term in search_terms
        ):
            matches.append(raga)

    if not matches:
        return (
            "No exact raga entry was found in the current reference "
            "catalogue. Do not claim that catalogue data was retrieved. "
            + GENERAL_REFERENCE
        )

    sections = [
        "RETRIEVED CARNATIC REFERENCE DATA",
        "Use these records as reference material. Preserve their notation.",
        GENERAL_REFERENCE,
    ]

    for raga in matches:
        sections.append(
            "\n".join(
                [
                    f"Raga: {raga['name']}",
                    f"Category: {raga['category']}",
                    f"Melakarta number: "
                    f"{raga.get('melakarta_number') or 'Not specified'}",
                    (
                        f"Commonly associated melakarta: "
                        f"{raga['commonly_associated_melakarta']}"
                        if raga.get("commonly_associated_melakarta")
                        else ""
                    ),
                    f"Arohanam: {raga['arohanam']}",
                    f"Avarohanam: {raga['avarohanam']}",
                    f"Notes: {raga['notes']}",
                ]
            )
        )

    return "\n\n".join(sections)


async def get_rag_knowledge_context(
    question: str,
    limit: int = 5,
) -> str:
    """Retrieve semantic knowledge, with exact catalogue fallback."""

    session = SessionLocal()

    try:
        has_embeddings = (
            session.query(KnowledgeEmbedding.id).first()
            is not None
        )
    finally:
        session.close()

    if not has_embeddings:
        logger.info(
            "Vector database is empty. Using exact catalogue retrieval."
        )
        return get_knowledge_context(question)

    results = await SemanticSearchService().search(
        question=question,
        limit=limit,
    )

    if not results:
        return get_knowledge_context(question)

    sections = [
        "RETRIEVED CARNATIC MUSIC KNOWLEDGE",
        (
            "Use the following retrieved records as reference material. "
            "Preserve Carnatic notation and distinguish retrieved facts "
            "from general explanations."
        ),
    ]

    for result in results:
        sections.append(
            "\n".join(
                [
                    f"Source category: {result['source_type']}",
                    f"Source ID: {result['source_id']}",
                    f"Similarity: {result['similarity']}",
                    result["content"],
                ]
            )
        )

    return "\n\n".join(sections)
