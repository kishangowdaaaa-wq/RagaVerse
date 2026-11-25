
import io

import numpy as np
import soundfile as sf

from app.services.audio_processing import (
    AudioProcessingError,
    AudioProcessingService,
)


def create_test_audio(
    sample_rate: int = 44100,
    duration: float = 2.0,
) -> bytes:
    """Generate a 440 Hz test tone."""

    time = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False,
    )

    audio = 0.5 * np.sin(2 * np.pi * 440 * time)

    buffer = io.BytesIO()

    sf.write(
        buffer,
        audio,
        sample_rate,
        format="WAV",
    )

    return buffer.getvalue()


def test_process_audio_successfully():
    service = AudioProcessingService()

    result = service.process_audio(
        create_test_audio(),
        "test.wav",
    )

    assert result["sample_rate"] == 22050
    assert result["duration_seconds"] == 2.0
    assert result["channels"] == 1
    assert len(result["waveform"]) > 0
    assert result["peak_amplitude"] > 0


def test_process_stereo_audio():
    service = AudioProcessingService()

    sample_rate = 44100
    time = np.linspace(
        0,
        1,
        sample_rate,
        endpoint=False,
    )

    stereo = np.column_stack(
        [
            0.5 * np.sin(2 * np.pi * 440 * time),
            0.5 * np.sin(2 * np.pi * 550 * time),
        ]
    )

    buffer = io.BytesIO()

    sf.write(
        buffer,
        stereo,
        sample_rate,
        format="WAV",
    )

    result = service.process_audio(
        buffer.getvalue(),
        "stereo.wav",
    )

    assert result["channels"] == 2
    assert result["sample_rate"] == 22050


def test_reject_empty_audio():
    service = AudioProcessingService()

    try:
        service.process_audio(b"", "empty.wav")
        assert False, "Expected AudioProcessingError"
    except AudioProcessingError:
        pass


def test_reject_unsupported_format():
    service = AudioProcessingService()

    try:
        service.process_audio(b"test", "audio.mp3")
        assert False, "Expected AudioProcessingError"
    except AudioProcessingError:
        pass


def test_reject_oversized_audio():
    service = AudioProcessingService()

    oversized_audio = b"x" * (
        service.MAX_FILE_SIZE_BYTES + 1
    )

    try:
        service.process_audio(
            oversized_audio,
            "large.wav",
        )
        assert False, "Expected AudioProcessingError"
    except AudioProcessingError:
        pass
