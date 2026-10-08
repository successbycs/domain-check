"""OpenAI candidate generation and local evidence capture."""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Protocol

from domain_agent.models import CandidateGeneration, CompanyDescriptionInput
from domain_agent.prompts import build_candidate_generation_prompt

DEFAULT_GENERATION_MODEL = "gpt-4o-mini"


class ParsedResponse(Protocol):
    """The small part of an OpenAI parsed response this project needs."""

    output_parsed: CandidateGeneration | None

    def model_dump(self, *, mode: str) -> dict[str, Any]:
        """Return the complete API response as JSON-compatible data."""


class ResponsesResource(Protocol):
    """The structured-output operation used by the candidate generator."""

    def parse(self, **kwargs: Any) -> ParsedResponse:
        """Send a request and parse it with the supplied Pydantic model."""


class OpenAIClient(Protocol):
    """The part of the OpenAI client used here, including its responses API."""

    responses: ResponsesResource


@dataclass(frozen=True)
class CandidateGenerationRun:
    """One OpenAI request, its raw API response, and validated candidates."""

    requested_at: datetime
    model: str
    reasoning_effort: str | None
    request: dict[str, Any]
    raw_response: dict[str, Any]
    candidates: CandidateGeneration


def generate_candidates(
    company_input: CompanyDescriptionInput,
    client: OpenAIClient,
    model: str = DEFAULT_GENERATION_MODEL,
    reasoning_effort: str | None = None,
) -> CandidateGenerationRun:
    """Generate and validate ten candidates from a company description.

    The client is an argument rather than being created here. This keeps the
    reusable logic easy to test with a pretend client and keeps credentials at
    the command-line boundary.
    """
    request: dict[str, Any] = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": build_candidate_generation_prompt(
                    company_input.description
                ),
            }
        ],
        "structured_output_model": "CandidateGeneration",
        "structured_output_schema": CandidateGeneration.model_json_schema(),
    }
    if reasoning_effort is not None:
        request["reasoning"] = {"effort": reasoning_effort}

    parse_arguments: dict[str, Any] = {
        "model": model,
        "input": request["input"],
        "text_format": CandidateGeneration,
    }
    if reasoning_effort is not None:
        parse_arguments["reasoning"] = {"effort": reasoning_effort}
    response = client.responses.parse(**parse_arguments)

    if response.output_parsed is None:
        raise ValueError("OpenAI returned no structured candidate response.")

    candidates = CandidateGeneration.model_validate(response.output_parsed)
    return CandidateGenerationRun(
        requested_at=datetime.now(timezone.utc),
        model=model,
        reasoning_effort=reasoning_effort,
        request=request,
        raw_response=response.model_dump(mode="json"),
        candidates=candidates,
    )


def save_generation_run(
    generation_run: CandidateGenerationRun,
    output_root: Path = Path("output"),
) -> Path:
    """Write inspectable request and response evidence to an ignored folder."""
    timestamp = generation_run.requested_at.strftime("%Y%m%dT%H%M%SZ")
    run_directory = output_root / f"candidate-generation-{timestamp}"
    run_directory.mkdir(parents=True, exist_ok=False)

    (run_directory / "request.json").write_text(
        json.dumps(generation_run.request, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_directory / "response.json").write_text(
        json.dumps(generation_run.raw_response, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_directory / "candidates.json").write_text(
        generation_run.candidates.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    return run_directory
