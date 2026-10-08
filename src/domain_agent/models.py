"""Checked data containers used by the Domain Research Agent."""

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class ClarityRating(StrEnum):
    """Allowed clarity assessments returned by the generation model."""

    EXCELLENT = "excellent"
    GOOD = "good"
    POOR = "poor"


class PronunciationRating(StrEnum):
    """Allowed pronunciation assessments returned by the generation model."""

    EASY_TO_SAY = "easy_to_say"
    UNCLEAR = "unclear"
    HARD_TO_SAY = "hard_to_say"


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


class NameConflictStatus(StrEnum):
    """Whether the model identified a specific possible name conflict."""

    NOT_IDENTIFIED = "not_identified"
    POSSIBLE = "possible"


class CompanyDescriptionInput(BaseModel):
    """The company-description data supplied to the application."""

    input_filename: str = Field(min_length=1)
    description: str = Field(min_length=1)


class PronunciationAssessment(BaseModel):
    """The model's opinion about how easy a candidate is to say."""

    rating: PronunciationRating
    reason: str = Field(min_length=1)


class ConcernFlag(BaseModel):
    """A possible concern, never a claim of cultural or linguistic clearance."""

    concern_type: ConcernType
    explanation: str = Field(min_length=1)
    uncertainty_note: str = Field(min_length=1)
    requires_human_review: Literal[True] = True


class NameConflictSignal(BaseModel):
    """An LLM signal, not a trademark search or legal conclusion."""

    status: NameConflictStatus
    reason: str = Field(min_length=1)
    requires_human_review: Literal[True] = True


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


class GeneratedCandidate(BaseModel):
    """One candidate returned by OpenAI before lookup and scoring."""

    name: str = Field(min_length=1)
    domain: str = Field(
        pattern=r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.co\.nz$"
    )
    fit_reason: str = Field(min_length=1)
    clarity: ClarityRating
    pronunciation: PronunciationAssessment
    concerns: list[ConcernFlag] = Field(default_factory=list)
    possible_name_conflict: NameConflictSignal
    human_review_items: list[str] = Field(min_length=1)
    editorial_comment: str = Field(min_length=1)


class CandidateGeneration(BaseModel):
    """The complete structured response expected from the generation model."""

    candidates: list[GeneratedCandidate] = Field(min_length=10, max_length=10)

    @model_validator(mode="after")
    def candidates_are_unique(self) -> "CandidateGeneration":
        """Reject repeated names or domains in the required set of ten."""
        names = [candidate.name.casefold() for candidate in self.candidates]
        domains = [candidate.domain for candidate in self.candidates]

        if len(set(names)) != len(names):
            raise ValueError("Candidate names must be distinct.")
        if len(set(domains)) != len(domains):
            raise ValueError("Candidate domains must be distinct.")

        return self


class ResearchCandidate(BaseModel):
    """One completed candidate after lookup and Python scoring."""

    generated: GeneratedCandidate
    availability: AvailabilityCheck = Field(default_factory=AvailabilityCheck)
    score: ScoreBreakdown = Field(default_factory=ScoreBreakdown)


class EvaluationCheck(BaseModel):
    """One transparent pass/fail check performed against a report."""

    name: str = Field(min_length=1)
    passed: bool
    detail: str = Field(min_length=1)


class RuleBasedEvaluation(BaseModel):
    """Repeatable completeness and consistency checks for one report."""

    evaluated_at: datetime
    passed: bool
    checks: list[EvaluationCheck] = Field(min_length=1)


class ModelEvaluation(BaseModel):
    """A separate LLM's usefulness review of a completed report."""

    rating: int = Field(ge=1, le=5)
    strengths: list[str] = Field(min_length=1)
    weaknesses: list[str] = Field(min_length=1)
    required_human_review_items: list[str] = Field(min_length=1)
    summary: str = Field(min_length=1)


class ResearchReport(BaseModel):
    """The complete report for one domain-research run."""

    created_at: datetime
    company_input: CompanyDescriptionInput
    generation_model: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    candidates: list[ResearchCandidate] = Field(min_length=10, max_length=10)
    rule_based_evaluation: RuleBasedEvaluation | None = None
    model_evaluation: ModelEvaluation | None = None

    @model_validator(mode="after")
    def candidate_domains_are_unique(self) -> "ResearchReport":
        """Protect report integrity if candidates are assembled outside OpenAI."""
        domains = [candidate.generated.domain for candidate in self.candidates]

        if len(set(domains)) != len(domains):
            raise ValueError("Report candidate domains must be distinct.")

        return self
