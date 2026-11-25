
"""Unified Carnatic music knowledge base for RagaVerse."""

from app.knowledge.catalog import (
    ALL_RAGAS,
    GENERAL_REFERENCE,
    MELAKARTA_NAMES,
)
from app.knowledge.talas import ALL_TALAS
from app.knowledge.swaras import ALL_SWARAS
from app.knowledge.compositions import ALL_COMPOSITIONS
from app.knowledge.learning import LEARNING_MODULES


KNOWLEDGE_BASE = {
    "ragas": ALL_RAGAS,
    "talas": ALL_TALAS,
    "swaras": ALL_SWARAS,
    "compositions": ALL_COMPOSITIONS,
    "learning_modules": LEARNING_MODULES,
}


__all__ = [
    "ALL_RAGAS",
    "ALL_TALAS",
    "ALL_SWARAS",
    "ALL_COMPOSITIONS",
    "LEARNING_MODULES",
    "GENERAL_REFERENCE",
    "MELAKARTA_NAMES",
    "KNOWLEDGE_BASE",
]
