
"""Unified audio intelligence pipeline for RagaVerse."""

import logging
from typing import Any

from app.services.audio_processing import (
    AudioProcessingError,
    AudioProcessingService,
)
from app.services.pitch_detection import (
    PitchDetectionError,
    PitchDetectionService,
)
from app.services.swara_identification import (
    SwaraIdentificationError,
    SwaraIdentificationService,
)
from app.services.raga_detection import (
    RagaDetectionError,
    RagaDetectionService,
)


logger = logging.getLogger(__name__)


class AudioIntelligenceError(Exception):
    """Raised when audio intelligence analysis fails."""


class AudioIntelligenceService:
    """Coordinate audio, pitch, swara, and raga analysis."""

    def __init__(self) -> None:
        self.audio_service = AudioProcessingService()
        self.pitch_service = PitchDetectionService()
        self.swara_service = SwaraIdentificationService()
        self.raga_service = RagaDetectionService()

    async def analyze_audio(
        self,
        audio_bytes: bytes,
        filename: str,
        tonic_frequency: float,
    ) -> dict[str, Any]:
        """Analyze an uploaded recording and identify raga candidates."""

        if tonic_frequency <= 0:
            raise AudioIntelligenceError(
                "Reference tonic frequency must be positive."
            )

        try:
            # Step 1: Load and preprocess audio.
            audio_result = self.audio_service.process_audio(
                audio_bytes,
                filename,
            )

            # Step 2: Detect fundamental frequencies.
            pitch_result = self.pitch_service.detect_pitch(
                audio_result["audio"],
                sample_rate=audio_result["sample_rate"],
            )

            # Step 3: Map detected frequencies to swaras.
            swara_results = self.swara_service.identify_sequence(
                pitch_result["frequencies"],
                tonic_frequency=tonic_frequency,
            )

            # Step 4: Collect detected swara sequence.
            detected_swaras = [
                result["swara"]
                for result in swara_results
                if result is not None
            ]

            if not detected_swaras:
                raise AudioIntelligenceError(
                    "No identifiable musical pitches were detected."
                )

            # Step 5: Identify candidate ragas.
            raga_result = self.raga_service.detect_raga(
                detected_swaras,
                limit=5,
            )

            # Step 6: Return combined analysis.
            return {
                "audio": {
                    "sample_rate": audio_result["sample_rate"],
                    "duration_seconds": audio_result[
                        "duration_seconds"
                    ],
                    "channels": audio_result["channels"],
                    "waveform": audio_result["waveform"],
                    "peak_amplitude": audio_result[
                        "peak_amplitude"
                    ],
                },
                "pitch": {
                    "average_frequency": pitch_result[
                        "average_frequency"
                    ],
                    "frequencies": pitch_result["frequencies"],
                    "times": pitch_result["times"],
                    "confidence": pitch_result["confidence"],
                    "voiced_frames": pitch_result[
                        "voiced_frames"
                    ],
                    "total_frames": pitch_result["total_frames"],
                    "voiced_ratio": pitch_result["voiced_ratio"],
                },
                "swara": {
                    "tonic_frequency": tonic_frequency,
                    "sequence": swara_results,
                    "detected_swaras": detected_swaras,
                },
                "raga": raga_result,
            }

        except (
            AudioProcessingError,
            PitchDetectionError,
            SwaraIdentificationError,
            RagaDetectionError,
            AudioIntelligenceError,
        ):
            raise

        except Exception as exc:
            logger.exception(
                "Audio intelligence analysis failed."
            )
            raise AudioIntelligenceError(
                "Unable to complete audio analysis."
            ) from exc
