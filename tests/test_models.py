"""Tests for the checked data containers used by the application."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from domain_agent.models import (
    AvailabilityCheck,
    AvailabilityStatus,
    ConcernFlag,
    ConcernType,
    DomainCandidate,
    ScoreBreakdown,
)


def test_domain_candidate_keeps_assessments_and_visible_scores() -> None:
    """A valid candidate stores evidence without claiming certainty."""
    candidate = DomainCandidate(
        name="Harbour Bean",
        domain="harbourbean.co.nz",
        fit_reason="It reflects the coffee business and a Wellington location.",
        clarity="good",
        pronunciation_assessment="easy to say for English speakers",
        concerns=[
            ConcernFlag(
                concern_type=ConcernType.CROSS_LANGUAGE,
                explanation="No specific concern was identified by the assessment.",
                uncertainty_note="The assessment is incomplete and needs human review.",
            )
        ],
        availability=AvailabilityCheck(
            status=AvailabilityStatus.AVAILABLE,
            provider="Cloudflare Registrar",
            checked_at=datetime(2026, 10, 8, tzinfo=timezone.utc),
            price=Decimal("24.00"),
            currency="NZD",
        ),
        score=ScoreBreakdown(
            availability_points=1,
            clarity_points=1,
            pronunciation_points=1,
            association_points=1,
        ),
    )

    assert candidate.score.total_points == 4
    assert candidate.availability.status is AvailabilityStatus.AVAILABLE
    assert candidate.concerns[0].requires_human_review is True


def test_candidate_requires_a_co_nz_domain() -> None:
    """The first PoC scope rejects other domain extensions."""
    with pytest.raises(ValidationError, match="domain"):
        DomainCandidate(
            name="Harbour Bean",
            domain="harbourbean.com",
            fit_reason="A coffee-business name.",
            clarity="good",
            pronunciation_assessment="easy to say",
        )


def test_availability_can_be_available_when_price_is_unknown() -> None:
    """A provider may report availability without returning a price."""
    availability = AvailabilityCheck(
        status=AvailabilityStatus.AVAILABLE,
        provider="Cloudflare Registrar",
        checked_at=datetime(2026, 10, 8, tzinfo=timezone.utc),
    )

    assert availability.price is None
    assert availability.status is AvailabilityStatus.AVAILABLE
