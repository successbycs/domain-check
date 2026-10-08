"""Tests for the approved prompt template."""

from domain_agent.prompts import (
    EVALUATION_PROMPT_VERSION,
    GENERATION_PROMPT_VERSION,
    build_candidate_generation_prompt,
    build_report_evaluation_prompt,
)


def test_candidate_generation_prompt_includes_the_company_description() -> None:
    """The prompt includes the input that the model needs to assess."""
    prompt = build_candidate_generation_prompt("A small New Zealand coffee roaster.")

    assert GENERATION_PROMPT_VERSION == "v1"
    assert "A small New Zealand coffee roaster." in prompt
    assert "exactly 10" in prompt
    assert "Return only one JSON object" in prompt
    assert "Availability, price, provider, score, and final rank" in prompt


def test_report_evaluation_prompt_includes_the_complete_report() -> None:
    """The approved evaluator prompt receives the report it must assess."""
    prompt = build_report_evaluation_prompt('{"candidates": []}')

    assert EVALUATION_PROMPT_VERSION == "v1"
    assert '{"candidates": []}' in prompt
    assert "rating" in prompt
    assert "Do not invent facts" in prompt
