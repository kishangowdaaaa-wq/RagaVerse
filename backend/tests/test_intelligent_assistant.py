
import asyncio
from unittest.mock import patch

import pytest

from app.services.intent_detection import detect_intent
from app.services.raga_comparison import (
    build_raga_comparison_context,
)
from app.services.knowledge import (
    get_knowledge_context,
    get_rag_knowledge_context,
)


@pytest.mark.parametrize(
    "question, expected_intent",
    [
        ("Explain Kalyani raga", "raga_explanation"),
        ("Compare Mohanam and Hamsadhwani", "raga_comparison"),
        ("Explain Adi tala", "tala_explanation"),
        ("Who composed Vatapi Ganapatim?", "composition_information"),
        ("Teach me the seven swaras", "swaras_learning"),
        ("Explain Carnatic music theory", "general_carnatic"),
        ("Explain quantum computing", "out_of_scope"),
    ],
)
def test_intelligent_assistant_detects_question_intent(
    question,
    expected_intent,
):
    assert detect_intent(question) == expected_intent


def test_intelligent_assistant_retrieves_raga_context():
    context = get_knowledge_context("Explain Kalyani raga")

    assert "Kalyani" in context
    assert "Arohanam" in context
    assert "Avarohanam" in context


def test_intelligent_assistant_builds_raga_comparison():
    context = build_raga_comparison_context(
        "Compare Kalyani and Mohanam"
    )

    assert "STRUCTURED RAGA COMPARISON REFERENCE" in context
    assert "Kalyani" in context
    assert "Mohanam" in context
    assert "Arohanam" in context
    assert "Avarohanam" in context


def test_intelligent_assistant_does_not_build_single_raga_comparison():
    context = build_raga_comparison_context("Explain Kalyani")

    assert context == ""


def test_intelligent_assistant_rag_retrieval_fallback():
    async def run_test():
        with patch(
            "app.services.knowledge.SessionLocal"
        ) as mock_session_local:
            mock_session = mock_session_local.return_value
            mock_session.query.return_value.first.return_value = None

            context = await get_rag_knowledge_context(
                "Explain Kalyani",
                limit=5,
            )

            assert "Kalyani" in context
            mock_session.close.assert_called_once()

    asyncio.run(run_test())
