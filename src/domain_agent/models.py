"""Checked data containers used by the Domain Research Agent."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class AvailabilityStatus(StrEnum):
    """States returned by a domain availability provider."""

    NOT_CHECKED = "not_checked"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class ConcernType(StrEnum):
    """Types of concern that require careful human interpretation."""

    CROSS_LANGUAGE = "cross_language"
    TE_REO_MAORI = "te_reo_maori"
    MAORI_CULTURAL_AFFILIATION = "maori_cultural_affiliation"


class ConcernFlag(BaseModel):
    """A possible concern, never a claim of cultural or linguistic clearance."""

    concern_type: ConcernType
    explanation: str = Field(min_length=1)
    uncertainty_note: str = Field(min_length=1)
    requires_human_review: bool = True


class AvailabilityCheck(BaseModel):
    """Availability and price evidence from a provider such as Cloudflare."""

    status: AvailabilityStatus = AvailabilityStatus.NOT_CHECKED
    provider: str | None = None
    checked_at: datetime | None = None
    price: Decimal | None = Field(default=None, gt=0)
    currency: str | None = None
    error: str | None = None


class ScoreBreakdown(BaseModel):
    """The individual points that make a candidate's total score visible."""

    availability_points: int = 0
    clarity_points: int = 0
    pronunciation_points: int = 0
    association_points: int = 0

    @property
    def total_points(self) -> int:
        """Return the total without hiding the individual point values."""
        return sum(
            (
                self.availability_points,
                self.clarity_points,
                self.pronunciation_points,
                self.association_points,
            )
        )


class DomainCandidate(BaseModel):
    """One potential `.co.nz` domain and its recorded research information."""

    name: str = Field(min_length=1)
    domain: str = Field(
        pattern=r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.co\.nz$"
    )
    fit_reason: str = Field(min_length=1)
    clarity: str = Field(min_length=1)
    pronunciation_assessment: str = Field(min_length=1)
    concerns: list[ConcernFlag] = Field(default_factory=list)
    possible_name_conflict: str | None = None
    availability: AvailabilityCheck = Field(default_factory=AvailabilityCheck)
    score: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    editorial_recommendation: str | None = None
    human_review_items: list[str] = Field(default_factory=list)
