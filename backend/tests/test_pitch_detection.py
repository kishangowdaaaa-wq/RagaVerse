
import numpy as np
import pytest

from app.services.pitch_detection import (
    PitchDetectionError,
    PitchDetectionService,
)


def generate_tone(
    frequency: float = 440.0,
    duration: float = 2.0,
    sample_rate: int = 22050,
) -> np.ndarray:
    """Generate a pure sine-wave test tone."""

    time = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False,
    )

    return (
        0.5 * np.sin(2 * np.pi * frequency * time)
    ).astype(np.float32)


def test_detect_440_hz_tone():
    service = PitchDetectionService()

    result = service.detect_pitch(
        generate_tone(440.0)
    )

    assert result["average_frequency"] is not None

    assert abs(
        result["average_frequency"] - 440.0
    ) < 5.0

    assert result["voiced_frames"] > 0


def test_detect_261_hz_tone():
    service = PitchDetectionService()

    result = service.detect_pitch(
        generate_tone(261.63)
    )

    assert result["average_frequency"] is not None

    assert abs(
        result["average_frequency"] - 261.63
    ) < 5.0


def test_pitch_result_contains_timeline():
    service = PitchDetectionService()

    result = service.detect_pitch(
        generate_tone(440.0)
    )

    assert len(result["frequencies"]) > 0
    assert len(result["times"]) > 0
    assert len(result["confidence"]) > 0

    assert (
        len(result["frequencies"])
        == len(result["times"])
        == len(result["confidence"])
    )


def test_reject_empty_audio():
    service = PitchDetectionService()

    with pytest.raises(PitchDetectionError):
        service.detect_pitch(
            np.array([], dtype=np.float32)
        )


def test_reject_silent_audio():
    service = PitchDetectionService()

    silent_audio = np.zeros(
        22050,
        dtype=np.float32,
    )

    with pytest.raises(PitchDetectionError):
        service.detect_pitch(silent_audio)


def test_reject_invalid_sample_rate():
    service = PitchDetectionService()

    with pytest.raises(PitchDetectionError):
        service.detect_pitch(
            generate_tone(),
            sample_rate=0,
        )
