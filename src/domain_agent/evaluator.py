"""Deterministic checks for a completed domain-research report."""

from datetime import datetime, timezone

from domain_agent.models import (
    AvailabilityStatus,
    EvaluationCheck,
    ResearchReport,
    RuleBasedEvaluation,
)
from domain_agent.scorer import score_candidate


def evaluate_report(report: ResearchReport) -> RuleBasedEvaluation:
    """Check report completeness and that saved scores match the scoring rules."""
    checks = [
        _candidate_count_check(report),
        _distinct_domain_check(report),
        _availability_evidence_check(report),
        _human_review_check(report),
        _score_consistency_check(report),
    ]
    return RuleBasedEvaluation(
        evaluated_at=datetime.now(timezone.utc),
        passed=all(check.passed for check in checks),
        checks=checks,
    )


def _candidate_count_check(report: ResearchReport) -> EvaluationCheck:
    count = len(report.candidates)
    return EvaluationCheck(
        name="candidate_count",
        passed=count == 10,
        detail=f"Report contains {count} candidates; expected 10.",
    )


def _distinct_domain_check(report: ResearchReport) -> EvaluationCheck:
    domains = [candidate.generated.domain for candidate in report.candidates]
    distinct_count = len(set(domains))
    return EvaluationCheck(
        name="distinct_domains",
        passed=distinct_count == len(domains),
        detail=f"Report contains {distinct_count} distinct domains out of {len(domains)}.",
    )


def _availability_evidence_check(report: ResearchReport) -> EvaluationCheck:
    incomplete_domains = []
    for candidate in report.candidates:
        availability = candidate.availability
        has_evidence = (
            availability.status != AvailabilityStatus.NOT_CHECKED
            and availability.provider is not None
            and availability.checked_at is not None
            and (
                availability.status != AvailabilityStatus.UNKNOWN
                or availability.error is not None
            )
        )
        if not has_evidence:
            incomplete_domains.append(candidate.generated.domain)

    return EvaluationCheck(
        name="availability_evidence",
        passed=not incomplete_domains,
        detail=(
            "Availability evidence is present for every candidate."
            if not incomplete_domains
            else "Missing or incomplete availability evidence for: "
            + ", ".join(incomplete_domains)
        ),
    )


def _human_review_check(report: ResearchReport) -> EvaluationCheck:
    missing_review_items = [
        candidate.generated.domain
        for candidate in report.candidates
        if not candidate.generated.human_review_items
    ]
    return EvaluationCheck(
        name="human_review_items",
        passed=not missing_review_items,
        detail=(
            "Every candidate includes human-review items."
            if not missing_review_items
            else "Missing human-review items for: " + ", ".join(missing_review_items)
        ),
    )


def _score_consistency_check(report: ResearchReport) -> EvaluationCheck:
    inconsistent_domains = [
        candidate.generated.domain
        for candidate in report.candidates
        if candidate.score != score_candidate(candidate)
    ]
    return EvaluationCheck(
        name="score_consistency",
        passed=not inconsistent_domains,
        detail=(
            "Every saved score matches the Python scoring rules."
            if not inconsistent_domains
            else "Scores do not match the rules for: "
            + ", ".join(inconsistent_domains)
        ),
    )
