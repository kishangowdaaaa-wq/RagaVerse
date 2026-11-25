
"""Structured comparison of Carnatic ragas."""

from typing import Any

from app.knowledge.catalog import ALL_RAGAS


def normalize_name(name: str) -> str:
    """Normalize a raga name for matching."""

    return " ".join(name.casefold().strip().split())


def find_raga(name: str) -> dict[str, Any] | None:
    """Find a raga by its name or alias."""

    normalized_name = normalize_name(name)

    for raga in ALL_RAGAS:
        search_names = [
            raga.get("name", ""),
            *raga.get("aliases", []),
        ]

        if any(
            normalize_name(candidate) == normalized_name
            for candidate in search_names
        ):
            return raga

    return None


def get_scale_swara_differences(
    first_scale: str,
    second_scale: str,
) -> dict[str, list[str]]:
    """Identify swaras shared by or unique to two scales."""

    first_swaras = first_scale.split()
    second_swaras = second_scale.split()

    return {
        "common": sorted(set(first_swaras) & set(second_swaras)),
        "first_only": sorted(set(first_swaras) - set(second_swaras)),
        "second_only": sorted(set(second_swaras) - set(first_swaras)),
    }


def compare_ragas(
    first_name: str,
    second_name: str,
) -> dict[str, Any]:
    """Compare two ragas using the reference catalogue."""

    if not first_name or not first_name.strip():
        raise ValueError("The first raga name cannot be empty.")

    if not second_name or not second_name.strip():
        raise ValueError("The second raga name cannot be empty.")

    first_raga = find_raga(first_name)
    second_raga = find_raga(second_name)

    if first_raga is None:
        raise ValueError(
            f"Raga '{first_name}' was not found in the knowledge base."
        )

    if second_raga is None:
        raise ValueError(
            f"Raga '{second_name}' was not found in the knowledge base."
        )

    if first_raga["name"] == second_raga["name"]:
        raise ValueError("Please provide two different ragas.")

    first_arohanam = first_raga.get("arohanam", "")
    second_arohanam = second_raga.get("arohanam", "")

    first_avarohanam = first_raga.get("avarohanam", "")
    second_avarohanam = second_raga.get("avarohanam", "")

    melakarta_comparison = None

    if (
        first_raga.get("melakarta_number") is not None
        and second_raga.get("melakarta_number") is not None
    ):
        melakarta_comparison = {
            "first": first_raga["melakarta_number"],
            "second": second_raga["melakarta_number"],
            "same": (
                first_raga["melakarta_number"]
                == second_raga["melakarta_number"]
            ),
        }

    return {
        "first_raga": {
            "name": first_raga["name"],
            "category": first_raga.get("category"),
            "melakarta_number": first_raga.get("melakarta_number"),
            "arohanam": first_arohanam,
            "avarohanam": first_avarohanam,
            "notes": first_raga.get("notes", ""),
        },
        "second_raga": {
            "name": second_raga["name"],
            "category": second_raga.get("category"),
            "melakarta_number": second_raga.get("melakarta_number"),
            "arohanam": second_arohanam,
            "avarohanam": second_avarohanam,
            "notes": second_raga.get("notes", ""),
        },
        "melakarta_comparison": melakarta_comparison,
        "arohanam_comparison": get_scale_swara_differences(
            first_arohanam,
            second_arohanam,
        ),
        "avarohanam_comparison": get_scale_swara_differences(
            first_avarohanam,
            second_avarohanam,
        ),
        "warning": (
            "Scale similarities and differences alone do not establish "
            "the complete identity of a raga. Gamakas, characteristic "
            "phrases, and performance traditions also matter."
        ),
    }


def build_raga_comparison_context(question: str) -> str:
    """Build comparison context when two catalogue ragas are mentioned."""

    normalized_question = normalize_name(question)

    matches = []

    for raga in ALL_RAGAS:
        names = [
            raga.get("name", ""),
            *raga.get("aliases", []),
        ]

        if any(
            normalize_name(name) in normalized_question
            for name in names
            if name
        ):
            if raga["name"] not in [
                item["name"] for item in matches
            ]:
                matches.append(raga)

    if len(matches) != 2:
        return ""

    comparison = compare_ragas(
        matches[0]["name"],
        matches[1]["name"],
    )

    first = comparison["first_raga"]
    second = comparison["second_raga"]

    return "\n".join([
        "STRUCTURED RAGA COMPARISON REFERENCE",
        "Use these verified catalogue records when answering the comparison.",
        "",
        f"First raga: {first['name']}",
        f"Category: {first['category']}",
        f"Melakarta number: {first['melakarta_number']}",
        f"Arohanam: {first['arohanam']}",
        f"Avarohanam: {first['avarohanam']}",
        f"Notes: {first['notes']}",
        "",
        f"Second raga: {second['name']}",
        f"Category: {second['category']}",
        f"Melakarta number: {second['melakarta_number']}",
        f"Arohanam: {second['arohanam']}",
        f"Avarohanam: {second['avarohanam']}",
        f"Notes: {second['notes']}",
        "",
        f"Arohanam swara differences: {comparison['arohanam_comparison']}",
        f"Avarohanam swara differences: {comparison['avarohanam_comparison']}",
        f"Melakarta comparison: {comparison['melakarta_comparison']}",
        "",
        comparison["warning"],
    ])
