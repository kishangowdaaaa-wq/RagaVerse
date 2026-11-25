
"""Audio loading and preprocessing services for RagaVerse."""

from io import BytesIO
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import soundfile as sf


class AudioProcessingError(Exception):
    """Raised when uploaded audio cannot be processed."""


class AudioProcessingService:
    """Load, validate, and preprocess audio for music analysis."""

    SUPPORTED_FORMATS = {
        ".wav",
        ".flac",
        ".ogg",
        ".aiff",
        ".aif",
    }

    TARGET_SAMPLE_RATE = 22050
    MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024
    MAX_DURATION_SECONDS = 300
    WAVEFORM_POINTS = 1000

    def process_audio(
        self,
        audio_bytes: bytes,
        filename: str,
    ) -> dict[str, Any]:
        """Decode and preprocess an uploaded audio file."""

        if not audio_bytes:
            raise AudioProcessingError(
                "The uploaded audio file is empty."
            )

        if len(audio_bytes) > self.MAX_FILE_SIZE_BYTES:
            raise AudioProcessingError(
                "Audio file exceeds the 20 MB size limit."
            )

        extension = Path(filename).suffix.lower()

        if extension not in self.SUPPORTED_FORMATS:
            raise AudioProcessingError(
                "Unsupported audio format. "
                "Use WAV, FLAC, OGG, or AIFF."
            )

        try:
            audio, original_sample_rate = sf.read(
                BytesIO(audio_bytes),
                dtype="float32",
                always_2d=True,
            )

            if audio.size == 0:
                raise AudioProcessingError(
                    "The audio file contains no samples."
                )

            if not np.isfinite(audio).all():
                raise AudioProcessingError(
                    "The audio contains invalid sample values."
                )

            # Convert stereo or multichannel audio to mono.
            mono_audio = np.mean(audio, axis=1)

            original_duration = (
                len(mono_audio) / original_sample_rate
            )

            if original_duration > self.MAX_DURATION_SECONDS:
                raise AudioProcessingError(
                    "Audio duration exceeds the 5-minute limit."
                )

            # Resample to a consistent sample rate.
            if original_sample_rate != self.TARGET_SAMPLE_RATE:
                mono_audio = librosa.resample(
                    mono_audio,
                    orig_sr=original_sample_rate,
                    target_sr=self.TARGET_SAMPLE_RATE,
                )

            mono_audio = np.asarray(
                mono_audio,
                dtype=np.float32,
            )

            duration = (
                len(mono_audio) / self.TARGET_SAMPLE_RATE
            )

            waveform = self._extract_waveform(mono_audio)

            return {
                "audio": mono_audio,
                "sample_rate": self.TARGET_SAMPLE_RATE,
                "original_sample_rate": original_sample_rate,
                "duration_seconds": round(duration, 3),
                "channels": audio.shape[1],
                "waveform": waveform,
                "peak_amplitude": round(
                    float(np.max(np.abs(mono_audio))),
                    4,
                ),
            }

        except AudioProcessingError:
            raise

        except Exception as exc:
            raise AudioProcessingError(
                "Unable to decode the uploaded audio file."
            ) from exc

    def _extract_waveform(
        self,
        audio: np.ndarray,
    ) -> list[float]:
        """Create a compact waveform for frontend visualization."""

        if len(audio) == 0:
            return []

        chunks = np.array_split(
            audio,
            min(self.WAVEFORM_POINTS, len(audio)),
        )

        waveform = [
            float(np.max(np.abs(chunk)))
            for chunk in chunks
            if len(chunk) > 0
        ]

        return [
            round(value, 4)
            for value in waveform
        ]
