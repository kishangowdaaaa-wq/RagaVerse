
from types import SimpleNamespace

from app.services.personalization import build_personalization_context


def test_personalization_without_profile():
    result = build_personalization_context(None)

    assert result == ""


def test_personalization_with_complete_profile():
    profile = SimpleNamespace(
        experience_level="intermediate",
        preferred_learning_level="advanced",
        musical_background="Learning Carnatic music",
        primary_instrument="Vocal",
        years_of_experience=3,
        favorite_ragas=["Kalyani", "Mohanam"],
        musical_goals=[
            "Improve swara identification",
            "Learn compositions",
        ],
    )

    result = build_personalization_context(profile)

    assert "INTERMEDIATE" in result.upper()
    assert "ADVANCED" in result.upper()
    assert "Vocal" in result
    assert "Kalyani" in result
    assert "Mohanam" in result
    assert "Improve swara identification" in result
    assert "Learn compositions" in result


def test_personalization_with_minimal_profile():
    profile = SimpleNamespace(
        experience_level="beginner",
        preferred_learning_level="beginner",
        musical_background=None,
        primary_instrument=None,
        years_of_experience=None,
        favorite_ragas=[],
        musical_goals=[],
    )

    result = build_personalization_context(profile)

    assert "beginner" in result
    assert "PERSONALIZATION GUIDELINES" in result
    assert "Vocal" not in result
