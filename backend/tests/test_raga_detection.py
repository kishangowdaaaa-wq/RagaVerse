
import pytest

from app.services.raga_detection import (
    RagaDetectionError,
    RagaDetectionService,
)


@pytest.fixture
def service():
    return RagaDetectionService()


def test_detect_shankarabharanam(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "M1", "P", "D2", "N3"],
    )

    assert result["candidate_count"] == 74

    assert (
        result["candidates"][0]["name"]
        == "Shankarabharanam"
    )

    assert (
        result["candidates"][0]["match_percentage"]
        == 100.0
    )


def test_detect_kalyani(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "M2", "P", "D2", "N3"],
    )

    names = [
        candidate["name"]
        for candidate in result["candidates"]
    ]

    assert "Kalyani" in names


def test_detect_mohanam(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "P", "D2"],
    )

    names = [
        candidate["name"]
        for candidate in result["candidates"]
    ]

    assert "Mohanam" in names


def test_return_matched_and_unmatched_swaras(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "M1", "P", "N3"],
    )

    candidate = result["candidates"][0]

    assert "S" in candidate["matched_swaras"]
    assert "R2" in candidate["matched_swaras"]
    assert isinstance(
        candidate["unmatched_swaras"],
        list,
    )


def test_reject_empty_swara_sequence(service):
    with pytest.raises(RagaDetectionError):
        service.detect_raga([])


def test_reject_invalid_swara_sequence(service):
    with pytest.raises(RagaDetectionError):
        service.detect_raga(
            ["INVALID", "XYZ"]
        )


def test_reject_invalid_limit(service):
    with pytest.raises(RagaDetectionError):
        service.detect_raga(
            ["S", "R2", "G3"],
            limit=0,
        )


def test_respect_candidate_limit(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "M1", "P"],
        limit=3,
    )

    assert len(result["candidates"]) == 3


def test_include_identification_warning(service):
    result = service.detect_raga(
        ["S", "R2", "G3", "M1", "P"],
    )

    assert "not definitive" in result["warning"]
