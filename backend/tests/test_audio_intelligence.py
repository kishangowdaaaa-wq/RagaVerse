
import asyncio
import io

import numpy as np
import soundfile as sf

from app.services.audio_intelligence import (
    AudioIntelligenceError,
    AudioIntelligenceService,
)


def create_musical_recording() -> bytes:
    """Generate a short Shankarabharanam scale recording."""

    sample_rate = 22050
    tonic = 261.63

    # Equal-tempered approximations relative to Sa.
    semitones = [0, 2, 4, 5, 7, 9, 11]

    segments = []

    for semitone in semitones:
        frequency = tonic * (2 ** (semitone / 12))

        time = np.arange(
            int(sample_rate * 0.6)
        ) / sample_rate

        tone = (
            0.5
            * np.sin(2 * np.pi * frequency * time)
        )

        segments.append(tone)

    audio = np.concatenate(segments).astype(
        np.float32
    )

    buffer = io.BytesIO()

    sf.write(
        buffer,
        audio,
        sample_rate,
        format="WAV",
    )

    return buffer.getvalue()


def test_complete_audio_intelligence_pipeline():
    service = AudioIntelligenceService()

    result = asyncio.run(
        service.analyze_audio(
            audio_bytes=create_musical_recording(),
            filename="shankarabharanam.wav",
            tonic_frequency=261.63,
        )
    )

    assert result["audio"]["duration_seconds"] > 0

    assert (
        result["pitch"]["average_frequency"]
        is not None
    )

    assert len(result["swara"]["detected_swaras"]) > 0

    assert result["raga"]["candidate_count"] == 74

    assert len(result["raga"]["candidates"]) > 0


def test_pipeline_returns_waveform():
    service = AudioIntelligenceService()

    result = asyncio.run(
        service.analyze_audio(
            audio_bytes=create_musical_recording(),
            filename="scale.wav",
            tonic_frequency=261.63,
        )
    )

    assert len(result["audio"]["waveform"]) > 0


def test_pipeline_rejects_invalid_tonic():
    service = AudioIntelligenceService()

    try:
        asyncio.run(
            service.analyze_audio(
                audio_bytes=create_musical_recording(),
                filename="scale.wav",
                tonic_frequency=0,
            )
        )

        assert False, "Expected AudioIntelligenceError"

    except AudioIntelligenceError:
        pass
