
"""Preliminary raga identification using Carnatic scale matching."""

import re
from typing import Any

from app.knowledge.catalog import ALL_RAGAS


class RagaDetectionError(Exception):
    """Raised when raga identification fails."""


class RagaDetectionService:
    """Compare detected swaras against the RagaVerse raga catalogue."""

    SWARA_PATTERN = re.compile(
        r"^(S|R[123]|G[123]|M[12]|P|D[123]|N[123])$"
    )

    def _normalize_swaras(
        self,
        swaras: list[str],
    ) -> list[str]:
        """Validate and normalize detected swara names."""

        normalized = []

        for swara in swaras:
            value = swara.strip().upper()

            if not self.SWARA_PATTERN.fullmatch(value):
                continue

            normalized.append(value)

        return normalized

    def _extract_scale(
        self,
        scale: str,
    ) -> list[str]:
        """Extract individual swara tokens from a scale string."""

        return re.findall(
            r"S|R[123]|G[123]|M[12]|P|D[123]|N[123]",
            scale.upper(),
        )

    def detect_raga(
        self,
        detected_swaras: list[str],
        limit: int = 5,
    ) -> dict[str, Any]:
        """Rank ragas by compatibility with observed swaras."""

        if not detected_swaras:
            raise RagaDetectionError(
                "At least one detected swara is required."
            )

        if limit < 1 or limit > 20:
            raise RagaDetectionError(
                "Limit must be between 1 and 20."
            )

        normalized = self._normalize_swaras(
            detected_swaras
        )

        if not normalized:
            raise RagaDetectionError(
                "No valid Carnatic swaras were detected."
            )

        observed = set(normalized)
        candidates = []

        for raga in ALL_RAGAS:
            arohanam = self._extract_scale(
                raga["arohanam"]
            )

            avarohanam = self._extract_scale(
                raga["avarohanam"]
            )

            expected = set(arohanam + avarohanam)

            if not expected:
                continue

            matched = observed.intersection(expected)

            match_ratio = (
                len(matched) / len(observed)
            )

            candidates.append(
                {
                    "name": raga["name"],
                    "category": raga["category"],
                    "melakarta_number": raga.get(
                        "melakarta_number"
                    ),
                    "arohanam": raga["arohanam"],
                    "avarohanam": raga["avarohanam"],
                    "matched_swaras": sorted(matched),
                    "unmatched_swaras": sorted(
                        observed - expected
                    ),
                    "match_ratio": round(
                        match_ratio,
                        4,
                    ),
                    "match_percentage": round(
                        match_ratio * 100,
                        2,
                    ),
                    "notes": raga.get("notes", ""),
                }
            )

        candidates.sort(
            key=lambda item: (
                item["match_ratio"],
                len(item["matched_swaras"]),
            ),
            reverse=True,
        )

        return {
            "detected_swaras": normalized,
            "unique_swaras": sorted(observed),
            "candidate_count": len(candidates),
            "identification_method": "scale_matching",
            "warning": (
                "Scale compatibility is not definitive raga "
                "identification. Gamakas and characteristic "
                "phrases must also be considered."
            ),
            "candidates": candidates[:limit],
        }
