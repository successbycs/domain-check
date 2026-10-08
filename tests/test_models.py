"""Tests for the checked data containers used by the application."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from domain_agent.models import (
    AvailabilityCheck,
    AvailabilityStatus,
    CandidateGeneration,
    ClarityRating,
    ConcernFlag,
    ConcernType,
    GeneratedCandidate,
    NameConflictSignal,
    NameConflictStatus,
    PronunciationAssessment,
    PronunciationRating,
    ResearchCandidate,
    ScoreBreakdown,
)


def make_generated_candidate(number: int = 1) -> GeneratedCandidate:
    """Create valid sample data for one generated candidate."""
    return GeneratedCandidate(
        name=f"Harbour Bean {number}",
        domain=f"harbourbean{number}.co.nz",
        fit_reason="It reflects the coffee business and a Wellington location.",
        clarity=ClarityRating.GOOD,
        pronunciation=PronunciationAssessment(
            rating=PronunciationRating.EASY_TO_SAY,
            reason="The words are familiar English words.",
        ),
        concerns=[
            ConcernFlag(
                concern_type=ConcernType.CROSS_LANGUAGE,
                explanation="No specific concern was identified by the assessment.",
                uncertainty_note="The assessment is incomplete and needs human review.",
            )
        ],
        possible_name_conflict=NameConflictSignal(
            status=NameConflictStatus.NOT_IDENTIFIED,
            reason="No specific similarity was identified by the model.",
        ),
        human_review_items=["Check real-world business and trademark records."],
        editorial_comment="Warm, local, and easy to remember.",
    )


def test_generated_candidate_keeps_the_agreed_openai_structure() -> None:
    """A valid generated candidate matches the agreed prompt schema."""
    candidate = make_generated_candidate()

    assert candidate.domain == "harbourbean1.co.nz"
    assert candidate.pronunciation.rating is PronunciationRating.EASY_TO_SAY
    assert candidate.concerns[0].requires_human_review is True
    assert candidate.possible_name_conflict.requires_human_review is True


def test_candidate_generation_requires_ten_unique_candidates() -> None:
    """The model response must contain exactly ten different candidates."""
    generation = CandidateGeneration(
        candidates=[make_generated_candidate(number) for number in range(1, 11)]
    )

    assert len(generation.candidates) == 10


def test_candidate_generation_rejects_a_non_co_nz_domain() -> None:
    """The first PoC scope rejects other domain extensions."""
    candidate_data = make_generated_candidate().model_dump()
    candidate_data["domain"] = "harbourbean.com"

    with pytest.raises(ValidationError, match="domain"):
        GeneratedCandidate(**candidate_data)


def test_research_candidate_allows_available_with_unknown_price() -> None:
    """A provider may report availability without returning a price."""
    candidate = ResearchCandidate(
        generated=make_generated_candidate(),
        availability=AvailabilityCheck(
            status=AvailabilityStatus.AVAILABLE,
            provider="Cloudflare Registrar",
            checked_at=datetime(2026, 10, 8, tzinfo=timezone.utc),
        ),
        score=ScoreBreakdown(
            availability_points=1,
            clarity_points=1,
            pronunciation_points=1,
            association_points=1,
        ),
    )

    assert candidate.availability.price is None
    assert candidate.score.total_points == 4
