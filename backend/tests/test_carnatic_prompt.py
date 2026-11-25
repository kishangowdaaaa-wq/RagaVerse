
from app.prompts.carnatic import (
    SYSTEM_PROMPT,
    get_system_prompt,
)


def test_system_prompt_is_not_empty():
    assert len(SYSTEM_PROMPT) > 100


def test_system_prompt_contains_carnatic_topics():
    assert "Ragas" in SYSTEM_PROMPT
    assert "Swaras" in SYSTEM_PROMPT
    assert "Gamakas" in SYSTEM_PROMPT
    assert "Talas" in SYSTEM_PROMPT


def test_beginner_prompt():
    prompt = get_system_prompt("beginner")
    assert "USER KNOWLEDGE LEVEL: BEGINNER" in prompt


def test_intermediate_prompt():
    prompt = get_system_prompt("intermediate")
    assert "USER KNOWLEDGE LEVEL: INTERMEDIATE" in prompt


def test_advanced_prompt():
    prompt = get_system_prompt("advanced")
    assert "USER KNOWLEDGE LEVEL: ADVANCED" in prompt


def test_invalid_level_defaults_to_beginner():
    prompt = get_system_prompt("unknown")
    assert "USER KNOWLEDGE LEVEL: BEGINNER" in prompt


def test_level_is_case_insensitive():
    prompt = get_system_prompt("ADVANCED")
    assert "USER KNOWLEDGE LEVEL: ADVANCED" in prompt
