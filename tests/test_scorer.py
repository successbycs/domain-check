"""Tests for the fixed, inspectable candidate score."""

from domain_agent.models import (
    AvailabilityCheck,
    AvailabilityStatus,
    ClarityRating,
    ConcernFlag,
    ConcernType,
    PronunciationAssessment,
    PronunciationRating,
    ResearchCandidate,
)
from domain_agent.scorer import score_candidate
from tests.test_models import make_generated_candidate


def test_score_candidate_awards_points_for_available_clear_easy_candidate() -> None:
    """The happy path keeps every point source visible."""
    generated = make_generated_candidate()
    generated.clarity = ClarityRating.EXCELLENT
    generated.pronunciation = PronunciationAssessment(
        rating=PronunciationRating.EASY_TO_SAY,
        reason="Simple familiar words.",
    )
    generated.concerns = []

    score = score_candidate(
        ResearchCandidate(
            generated=generated,
            availability=AvailabilityCheck(status=AvailabilityStatus.AVAILABLE),
        )
    )

    assert score.availability_points == 1
    assert score.clarity_points == 2
    assert score.pronunciation_points == 1
    assert score.association_points == 1
    assert score.total_points == 5


def test_score_candidate_penalises_flagged_concerns_but_not_unknown_availability() -> None:
    """An unverified domain is not treated as available or unavailable."""
    generated = make_generated_candidate()
    generated.clarity = ClarityRating.POOR
    generated.pronunciation = PronunciationAssessment(
        rating=PronunciationRating.HARD_TO_SAY,
        reason="Several syllables are unclear.",
    )
    generated.concerns = [
        ConcernFlag(
            concern_type=ConcernType.CROSS_LANGUAGE,
            explanation="Possible unintended meaning.",
            uncertainty_note="This needs a human language review.",
        )
    ]

    score = score_candidate(
        ResearchCandidate(
            generated=generated,
            availability=AvailabilityCheck(status=AvailabilityStatus.UNKNOWN),
        )
    )

    assert score.availability_points == 0
    assert score.clarity_points == -1
    assert score.pronunciation_points == -1
    assert score.association_points == -1
    assert score.total_points == -3
