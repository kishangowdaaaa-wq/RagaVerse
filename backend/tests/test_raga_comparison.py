
import pytest

from app.services.raga_comparison import (
    compare_ragas,
    find_raga,
    get_scale_swara_differences,
)


def test_find_raga_by_name():
    raga = find_raga("Kalyani")

    assert raga is not None
    assert raga["name"] == "Kalyani"


def test_find_raga_is_case_insensitive():
    raga = find_raga("kalyani")

    assert raga is not None
    assert raga["name"] == "Kalyani"


def test_find_raga_by_alias():
    raga = find_raga("Mechakalyani")

    assert raga is not None
    assert raga["name"] == "Kalyani"


def test_find_unknown_raga():
    assert find_raga("Unknown Raga") is None


def test_compare_kalyani_and_shankarabharanam():
    result = compare_ragas(
        "Kalyani",
        "Shankarabharanam",
    )

    assert result["first_raga"]["melakarta_number"] == 65
    assert result["second_raga"]["melakarta_number"] == 29

    assert result["melakarta_comparison"]["same"] is False

    assert "M2" in result["first_raga"]["arohanam"]
    assert "M1" in result["second_raga"]["arohanam"]


def test_compare_rejects_unknown_raga():
    with pytest.raises(ValueError):
        compare_ragas("Kalyani", "Unknown Raga")


def test_compare_rejects_same_raga():
    with pytest.raises(ValueError):
        compare_ragas("Kalyani", "Kalyani")


def test_compare_rejects_empty_name():
    with pytest.raises(ValueError):
        compare_ragas("", "Kalyani")


def test_scale_swara_differences():
    result = get_scale_swara_differences(
        "S R2 G3 M1 P D2 N3 S",
        "S R2 G3 M2 P D2 N3 S",
    )

    assert result["first_only"] == ["M1"]
    assert result["second_only"] == ["M2"]
    assert "S" in result["common"]

from app.services.raga_comparison import (
    build_raga_comparison_context,
)


def test_build_comparison_context_for_two_ragas():
    context = build_raga_comparison_context(
        "Compare Kalyani and Shankarabharanam"
    )

    assert "STRUCTURED RAGA COMPARISON REFERENCE" in context
    assert "Kalyani" in context
    assert "Shankarabharanam" in context
    assert "Melakarta number: 65" in context
    assert "Melakarta number: 29" in context


def test_build_comparison_context_for_one_raga():
    context = build_raga_comparison_context(
        "Explain Kalyani raga"
    )

    assert context == ""
