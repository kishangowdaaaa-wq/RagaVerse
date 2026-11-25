
"""Intent detection for the RagaVerse Carnatic music assistant."""

import re


INTENT_KEYWORDS = {
    "raga_comparison": [
        "compare",
        "difference between",
        "differentiate",
        "similarities between",
        "contrast",
        "versus",
        "vs",
    ],
    "tala_explanation": [
        "tala",
        "taalam",
        "rhythm",
        "beats",
        "akshara",
        "anga",
    ],
    "composition_information": [
        "composition",
        "composed",
        "composer",
        "kriti",
        "krithi",
        "song",
        "vatapi",
        "endaro",
        "nagumomu",
        "brochevarevarura",
        "krishna nee begane",
    ],
    "swaras_learning": [
        "swara",
        "swaras",
        "svara",
        "svaras",
        "notes",
        "sapta swara",
        "seven basic notes",
    ],
    "raga_explanation": [
        "raga",
        "ragam",
        "arohanam",
        "avarohanam",
        "melakarta",
        "janya",
        "gamakas",
        "prayoga",
    ],
    "general_carnatic": [
        "carnatic",
        "music theory",
        "shruti",
        "sruti",
        "laya",
        "practice",
        "learn",
        "teach",
    ],
}

OUT_OF_SCOPE_KEYWORDS = [
    "quantum computing",
    "stock market",
    "football",
    "weather",
    "politics",
]

INTENT_INSTRUCTIONS = {
    "raga_comparison": (
        "The user wants a comparison of ragas. Compare their "
        "arohanam, avarohanam, swara differences, and Melakarta "
        "relationships when reliable reference data is available. "
        "Explain that gamakas and characteristic phrases also "
        "contribute to raga identity."
    ),
    "tala_explanation": (
        "The user wants information about tala or rhythm. Explain "
        "the tala structure, beat count, and relevant rhythmic "
        "concepts using retrieved reference data where available."
    ),
    "composition_information": (
        "The user wants information about a Carnatic composition. "
        "Explain its composer, associated raga, tala, language, "
        "and composition type only when supported by reliable data. "
        "Do not invent missing details."
    ),
    "swaras_learning": (
        "The user wants to learn about Carnatic swaras. Explain "
        "the seven basic swaras and relevant variants clearly. "
        "Use examples appropriate to the learner's level."
    ),
    "raga_explanation": (
        "The user wants to understand a raga. Explain its category, "
        "Melakarta relationship, arohanam, avarohanam, and "
        "characteristic features using retrieved data where available."
    ),
    "general_carnatic": (
        "Answer the user's Carnatic music question directly. "
        "Explain technical terms and use suitable musical examples."
    ),
    "out_of_scope": (
        "The question appears unrelated to Carnatic music. Politely "
        "explain that RagaVerse specializes in Carnatic music and "
        "invite the user to ask a related question. Do not invent "
        "an answer outside the assistant's intended domain."
    ),
}


def detect_intent(question: str) -> str:
    """Identify the most relevant intent in a user question."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    normalized = re.sub(
        r"\s+",
        " ",
        question.casefold().strip(),
    )

    if any(
        keyword in normalized
        for keyword in OUT_OF_SCOPE_KEYWORDS
    ):
        return "out_of_scope"

    for keyword in INTENT_KEYWORDS["raga_comparison"]:
        if keyword in normalized:
            return "raga_comparison"

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return intent

    return "general_carnatic"


def build_intent_instructions(question: str) -> str:
    """Build additional system instructions for the detected intent."""

    intent = detect_intent(question)

    return (
        f"DETECTED QUESTION INTENT: {intent}\n"
        "Follow these intent-specific response guidelines:\n"
        f"{INTENT_INSTRUCTIONS[intent]}"
    )
