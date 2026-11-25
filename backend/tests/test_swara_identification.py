
import pytest

from app.services.swara_identification import (
    SwaraIdentificationError,
    SwaraIdentificationService,
)


@pytest.fixture
def service():
    return SwaraIdentificationService()


def test_identify_shadja(service):
    result = service.identify_swara(
        frequency=261.63,
        tonic_frequency=261.63,
    )

    assert result["swara"] == "S"
    assert result["octave"] == 0
    assert result["cents_deviation"] == 0.0


def test_identify_panchama(service):
    # Panchama is approximately seven semitones above Sa.
    result = service.identify_swara(
        frequency=392.0,
        tonic_frequency=261.63,
    )

    assert result["swara"] == "P"
    assert abs(result["cents_deviation"]) < 5


def test_identify_madhyama(service):
    # M1 is approximately five semitones above Sa.
    result = service.identify_swara(
        frequency=349.23,
        tonic_frequency=261.63,
    )

    assert result["swara"] == "M1"
    assert abs(result["cents_deviation"]) < 5


def test_identify_upper_octave_sa(service):
    result = service.identify_swara(
        frequency=523.26,
        tonic_frequency=261.63,
    )

    assert result["swara"] == "S"
    assert result["octave"] == 1


def test_identify_swara_sequence(service):
    frequencies = [
        261.63,
        293.66,
        329.63,
        349.23,
        392.00,
    ]

    results = service.identify_sequence(
        frequencies,
        tonic_frequency=261.63,
    )

    assert len(results) == 5

    assert [
        result["swara"]
        for result in results
    ] == ["S", "R2", "G3", "M1", "P"]


def test_preserve_unvoiced_frames(service):
    results = service.identify_sequence(
        [261.63, None, 392.00],
        tonic_frequency=261.63,
    )

    assert results[0]["swara"] == "S"
    assert results[1] is None
    assert results[2]["swara"] == "P"


def test_reject_invalid_frequency(service):
    with pytest.raises(SwaraIdentificationError):
        service.identify_swara(
            frequency=0,
            tonic_frequency=261.63,
        )


def test_reject_invalid_tonic(service):
    with pytest.raises(SwaraIdentificationError):
        service.identify_swara(
            frequency=440,
            tonic_frequency=0,
        )
