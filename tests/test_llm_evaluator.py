"""Tests for the separate-model report evaluator."""

from typing import Any

from domain_agent.llm_evaluator import (
    DEFAULT_EVALUATION_MODEL,
    evaluate_report_with_model,
    save_model_evaluation_run,
)
from domain_agent.models import ModelEvaluation
from tests.test_evaluator import make_complete_report


class FakeResponse:
    """A no-network stand-in for OpenAI's parsed response."""

    def __init__(self, evaluation: ModelEvaluation) -> None:
        self.output_parsed = evaluation

    def model_dump(self, *, mode: str) -> dict[str, Any]:
        assert mode == "json"
        return {"id": "resp_evaluation_test", "status": "completed"}


class FakeResponsesResource:
    """Records the evaluator request instead of sending it over the network."""

    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.call_arguments: dict[str, Any] | None = None

    def parse(self, **kwargs: Any) -> FakeResponse:
        self.call_arguments = kwargs
        return self.response


class FakeClient:
    """A client-shaped object holding a pretend responses API."""

    def __init__(self, responses: FakeResponsesResource) -> None:
        self.responses = responses


def test_model_evaluator_uses_approved_prompt_and_saves_evidence(tmp_path: Any) -> None:
    """The evaluator returns structured feedback without a live API call."""
    expected_evaluation = ModelEvaluation(
        rating=4,
        strengths=["Clear availability evidence."],
        weaknesses=["Names need more variety."],
        required_human_review_items=["Check trademark records."],
        summary="Useful with improvements needed.",
    )
    fake_responses = FakeResponsesResource(FakeResponse(expected_evaluation))

    evaluation_run = evaluate_report_with_model(
        make_complete_report(),
        FakeClient(fake_responses),
    )
    save_model_evaluation_run(evaluation_run, tmp_path)

    assert fake_responses.call_arguments is not None
    assert fake_responses.call_arguments["model"] == DEFAULT_EVALUATION_MODEL
    assert fake_responses.call_arguments["text_format"] is ModelEvaluation
    assert evaluation_run.evaluation == expected_evaluation
    assert (tmp_path / "evaluation-request.json").exists()
    assert (tmp_path / "evaluation-response.json").exists()


def test_model_evaluator_passes_an_explicit_reasoning_effort() -> None:
    """A comparison run records the evaluator's model setting as evidence."""
    expected_evaluation = ModelEvaluation(
        rating=4,
        strengths=["Clear availability evidence."],
        weaknesses=["Names need more variety."],
        required_human_review_items=["Check trademark records."],
        summary="Useful with improvements needed.",
    )
    fake_responses = FakeResponsesResource(FakeResponse(expected_evaluation))

    evaluation_run = evaluate_report_with_model(
        make_complete_report(),
        FakeClient(fake_responses),
        model="gpt-6-astra",
        reasoning_effort="medium",
    )

    assert fake_responses.call_arguments is not None
    assert fake_responses.call_arguments["reasoning"] == {"effort": "medium"}
    assert evaluation_run.reasoning_effort == "medium"
