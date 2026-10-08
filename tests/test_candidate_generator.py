"""Tests for the OpenAI candidate-generation boundary."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from domain_agent.candidate_generator import (
    DEFAULT_GENERATION_MODEL,
    generate_candidates,
    save_generation_run,
)
from domain_agent.models import CandidateGeneration, CompanyDescriptionInput
from tests.test_models import make_generated_candidate


class FakeResponse:
    """A no-network stand-in for OpenAI's parsed response."""

    def __init__(self, candidates: CandidateGeneration) -> None:
        self.output_parsed = candidates

    def model_dump(self, *, mode: str) -> dict[str, Any]:
        assert mode == "json"
        return {"id": "resp_test", "status": "completed"}


class FakeResponsesResource:
    """Records the request instead of sending it over the network."""

    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.call_arguments: dict[str, Any] | None = None

    def parse(self, **kwargs: Any) -> FakeResponse:
        self.call_arguments = kwargs
        return self.response


class FakeClient:
    """A client-shaped object holding the pretend responses API."""

    def __init__(self, responses: FakeResponsesResource) -> None:
        self.responses = responses


def test_generator_uses_the_prompt_and_saves_request_response_evidence(
    tmp_path: Path,
) -> None:
    """A test run records what would be sent and what was accepted."""
    candidates = CandidateGeneration(
        candidates=[make_generated_candidate(number=index) for index in range(10)]
    )
    fake_responses = FakeResponsesResource(FakeResponse(candidates))
    company_input = CompanyDescriptionInput(
        input_filename="company.txt",
        description="A New Zealand coffee roaster.",
    )

    generation_run = generate_candidates(
        company_input=company_input,
        client=FakeClient(fake_responses),
    )
    output_directory = save_generation_run(generation_run, tmp_path)

    assert fake_responses.call_arguments is not None
    assert fake_responses.call_arguments["model"] == DEFAULT_GENERATION_MODEL
    assert fake_responses.call_arguments["text_format"] is CandidateGeneration
    assert "A New Zealand coffee roaster." in fake_responses.call_arguments["input"][0]["content"]
    assert generation_run.candidates == candidates
    assert (output_directory / "request.json").exists()
    assert (output_directory / "response.json").exists()
    assert (output_directory / "candidates.json").exists()


def test_generator_passes_an_explicit_reasoning_effort_to_the_api() -> None:
    """An experiment can record exactly which model setting was used."""
    candidates = CandidateGeneration(
        candidates=[make_generated_candidate(number=index) for index in range(10)]
    )
    fake_responses = FakeResponsesResource(FakeResponse(candidates))

    generation_run = generate_candidates(
        CompanyDescriptionInput(
            input_filename="company.txt",
            description="A New Zealand coffee roaster.",
        ),
        FakeClient(fake_responses),
        model="gpt-6-astra",
        reasoning_effort="medium",
    )

    assert fake_responses.call_arguments is not None
    assert fake_responses.call_arguments["reasoning"] == {"effort": "medium"}
    assert generation_run.reasoning_effort == "medium"
