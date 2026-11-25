
"""Fundamental frequency detection for RagaVerse."""

from typing import Any

import librosa
import numpy as np


class PitchDetectionError(Exception):
    """Raised when pitch detection fails."""


class PitchDetectionService:
    """Detect fundamental frequencies using librosa pYIN."""

    def __init__(self) -> None:
        self.frame_length = 2048
        self.hop_length = 256
        self.minimum_frequency = 65.0
        self.maximum_frequency = 1000.0

    def detect_pitch(
        self,
        audio: np.ndarray,
        sample_rate: int = 22050,
    ) -> dict[str, Any]:
        """Detect pitch across an audio recording."""

        if audio is None or len(audio) == 0:
            raise PitchDetectionError(
                "Audio data cannot be empty."
            )

        if sample_rate <= 0:
            raise PitchDetectionError(
                "Sample rate must be positive."
            )

        audio = np.asarray(audio, dtype=np.float32)

        if not np.isfinite(audio).all():
            raise PitchDetectionError(
                "Audio contains invalid sample values."
            )

        if np.max(np.abs(audio)) < 1e-6:
            raise PitchDetectionError(
                "Audio is silent. No pitch can be detected."
            )

        try:
            f0, voiced_flag, voiced_probability = librosa.pyin(
                audio,
                fmin=self.minimum_frequency,
                fmax=self.maximum_frequency,
                sr=sample_rate,
                frame_length=self.frame_length,
                hop_length=self.hop_length,
            )

            times = librosa.times_like(
                f0,
                sr=sample_rate,
                hop_length=self.hop_length,
            )

            valid_pitch = (
                np.isfinite(f0)
                & voiced_flag
            )

            pitch_values = [
                round(float(value), 2)
                if valid
                else None
                for value, valid in zip(f0, valid_pitch)
            ]

            confidence_values = [
                round(float(value), 4)
                if valid
                else 0.0
                for value, valid in zip(
                    voiced_probability,
                    valid_pitch,
                )
            ]

            valid_frequencies = f0[valid_pitch]

            average_frequency = (
                round(float(np.mean(valid_frequencies)), 2)
                if len(valid_frequencies) > 0
                else None
            )

            return {
                "frequencies": pitch_values,
                "times": [
                    round(float(value), 3)
                    for value in times
                ],
                "confidence": confidence_values,
                "average_frequency": average_frequency,
                "voiced_frames": int(
                    np.sum(valid_pitch)
                ),
                "total_frames": len(f0),
                "voiced_ratio": round(
                    float(np.mean(voiced_flag)),
                    4,
                ),
            }

        except PitchDetectionError:
            raise

        except Exception as exc:
            raise PitchDetectionError(
                "Unable to detect pitch from audio."
            ) from exc
