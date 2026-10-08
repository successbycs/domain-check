"""Tests for deterministic report evaluation."""

from datetime import datetime, timezone

from domain_agent.evaluator import evaluate_report
from domain_agent.models import (
    AvailabilityCheck,
    AvailabilityStatus,
    CandidateGeneration,
    CompanyDescriptionInput,
    ResearchCandidate,
    ResearchReport,
)
from domain_agent.scorer import score_candidate
from tests.test_models import make_generated_candidate


def make_complete_report() -> ResearchReport:
    """Create a complete, consistently scored report for evaluator tests."""
    generation = CandidateGeneration(
        candidates=[make_generated_candidate(number=index) for index in range(10)]
    )
    candidates = []
    for generated in generation.candidates:
        candidate = ResearchCandidate(
            generated=generated,
            availability=AvailabilityCheck(
                status=AvailabilityStatus.AVAILABLE,
                provider="Test provider",
                checked_at=datetime(2026, 10, 8, tzinfo=timezone.utc),
            ),
        )
        candidates.append(candidate.model_copy(update={"score": score_candidate(candidate)}))
    return ResearchReport(
        created_at=datetime(2026, 10, 8, tzinfo=timezone.utc),
        company_input=CompanyDescriptionInput(
            input_filename="company.txt",
            description="A New Zealand coffee roaster.",
        ),
        generation_model="gpt-4o-mini",
        prompt_version="v1",
        candidates=candidates,
    )


def test_evaluate_report_passes_a_complete_consistent_report() -> None:
    """The evaluator reports each required check rather than one opaque result."""
    evaluation = evaluate_report(make_complete_report())

    assert evaluation.passed is True
    assert {check.name for check in evaluation.checks} == {
        "candidate_count",
        "distinct_domains",
        "availability_evidence",
        "human_review_items",
        "score_consistency",
    }
    assert all(check.passed for check in evaluation.checks)


def test_evaluate_report_fails_when_a_saved_score_does_not_match() -> None:
    """The evaluation catches a report that was edited after scoring."""
    report = make_complete_report()
    report.candidates[0].score.availability_points = 99

    evaluation = evaluate_report(report)

    score_check = next(check for check in evaluation.checks if check.name == "score_consistency")
    assert evaluation.passed is False
    assert score_check.passed is False
