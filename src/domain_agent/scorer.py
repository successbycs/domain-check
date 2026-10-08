"""Repeatable Python scoring for completed domain candidates."""

from domain_agent.models import (
    AvailabilityStatus,
    ClarityRating,
    GeneratedCandidate,
    PronunciationRating,
    ResearchCandidate,
    ScoreBreakdown,
)


def score_candidate(candidate: ResearchCandidate) -> ScoreBreakdown:
    """Calculate visible points from recorded evidence and LLM assessments."""
    return ScoreBreakdown(
        availability_points=_availability_points(candidate.availability.status),
        clarity_points=_clarity_points(candidate.generated),
        pronunciation_points=_pronunciation_points(candidate.generated),
        association_points=_association_points(candidate.generated),
    )


def _availability_points(status: AvailabilityStatus) -> int:
    """Award one point only for current provider evidence of availability."""
    return 1 if status == AvailabilityStatus.AVAILABLE else 0


def _clarity_points(candidate: GeneratedCandidate) -> int:
    """Map the fixed clarity rating to the agreed points."""
    return {
        ClarityRating.EXCELLENT: 2,
        ClarityRating.GOOD: 1,
        ClarityRating.POOR: -1,
    }[candidate.clarity]


def _pronunciation_points(candidate: GeneratedCandidate) -> int:
    """Map the fixed pronunciation rating to the agreed points."""
    return {
        PronunciationRating.EASY_TO_SAY: 1,
        PronunciationRating.UNCLEAR: 0,
        PronunciationRating.HARD_TO_SAY: -1,
    }[candidate.pronunciation.rating]


def _association_points(candidate: GeneratedCandidate) -> int:
    """Reward no flagged concerns; otherwise require human review and deduct one."""
    return 1 if not candidate.concerns else -1
