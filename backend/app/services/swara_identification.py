
"""Carnatic swara identification relative to a reference tonic."""

from typing import Any

import numpy as np


class SwaraIdentificationError(Exception):
    """Raised when swara identification fails."""


class SwaraIdentificationService:
    """Map detected pitches to approximate Carnatic swara positions."""

    SWARAS = [
        {"name": "S", "semitones": 0},
        {"name": "R1", "semitones": 1},
        {"name": "R2", "semitones": 2},
        {"name": "R3", "semitones": 3},
        {"name": "G2", "semitones": 3},
        {"name": "G3", "semitones": 4},
        {"name": "M1", "semitones": 5},
        {"name": "M2", "semitones": 6},
        {"name": "P", "semitones": 7},
        {"name": "D1", "semitones": 8},
        {"name": "D2", "semitones": 9},
        {"name": "D3", "semitones": 10},
        {"name": "N2", "semitones": 10},
        {"name": "N3", "semitones": 11},
    ]

    def identify_swara(
        self,
        frequency: float,
        tonic_frequency: float,
    ) -> dict[str, Any]:
        """Identify the nearest swara relative to the tonic."""

        if not np.isfinite(frequency) or frequency <= 0:
            raise SwaraIdentificationError(
                "Pitch frequency must be positive and finite."
            )

        if (
            not np.isfinite(tonic_frequency)
            or tonic_frequency <= 0
        ):
            raise SwaraIdentificationError(
                "Tonic frequency must be positive and finite."
            )

        cents = 1200 * np.log2(
            frequency / tonic_frequency
        )

        # Find the nearest octave and semitone position.
        octave = int(np.floor(cents / 1200))
        octave_cents = cents - (octave * 1200)

        semitone_position = octave_cents / 100

        best_swara = min(
            self.SWARAS,
            key=lambda swara: abs(
                semitone_position - swara["semitones"]
            ),
        )

        expected_cents = (
            octave * 1200
            + best_swara["semitones"] * 100
        )

        deviation = cents - expected_cents

        return {
            "swara": best_swara["name"],
            "octave": octave,
            "frequency": round(float(frequency), 2),
            "tonic_frequency": round(
                float(tonic_frequency), 2
            ),
            "cents_deviation": round(
                float(deviation), 2
            ),
            "cents_from_sa": round(float(cents), 2),
        }

    def identify_sequence(
        self,
        frequencies: list[float | None],
        tonic_frequency: float,
    ) -> list[dict[str, Any] | None]:
        """Identify a sequence of detected pitch frames."""

        results = []

        for frequency in frequencies:
            if frequency is None:
                results.append(None)
                continue

            results.append(
                self.identify_swara(
                    frequency,
                    tonic_frequency,
                )
            )

        return results
