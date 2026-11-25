
import pytest

from app.services.intent_detection import detect_intent


@pytest.mark.parametrize(
    "question, expected",
    [
        ("Explain Kalyani raga", "raga_explanation"),
        (
            "What is the arohanam of Mohanam?",
            "raga_explanation",
        ),
        (
            "Compare Kalyani and Shankarabharanam",
            "raga_comparison",
        ),
        (
            "What is the difference between two ragas?",
            "raga_comparison",
        ),
        (
            "Explain Adi tala",
            "tala_explanation",
        ),
        (
            "How many beats are in Adi tala?",
            "tala_explanation",
        ),
        (
            "Who composed Vatapi Ganapatim?",
            "composition_information",
        ),
        (
            "Teach me the seven basic swaras",
            "swaras_learning",
        ),
        (
            "Explain Carnatic music theory",
            "general_carnatic",
        ),
        (
            "Explain quantum computing",
            "out_of_scope",
        ),
    ],
)
def test_detect_intent(question, expected):
    assert detect_intent(question) == expected


@pytest.mark.parametrize("question", ["", "   "])
def test_detect_intent_rejects_empty_question(question):
    with pytest.raises(ValueError):
        detect_intent(question)


def test_detect_intent_comparison_has_priority():
    assert detect_intent(
        "Compare Kalyani raga with Mohanam raga"
    ) == "raga_comparison"
