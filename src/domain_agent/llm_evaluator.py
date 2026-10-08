"""A separate OpenAI review of a completed domain-research report."""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from domain_agent.candidate_generator import OpenAIClient
from domain_agent.models import ModelEvaluation, ResearchReport
from domain_agent.prompts import build_report_evaluation_prompt

DEFAULT_EVALUATION_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class ModelEvaluationRun:
    """One evaluator request, raw response, and checked review."""

    requested_at: datetime
    model: str
    reasoning_effort: str | None
    request: dict[str, Any]
    raw_response: dict[str, Any]
    evaluation: ModelEvaluation


def evaluate_report_with_model(
    report: ResearchReport,
    client: OpenAIClient,
    model: str = DEFAULT_EVALUATION_MODEL,
    reasoning_effort: str | None = None,
) -> ModelEvaluationRun:
    """Ask a separate LLM call to assess the completed report's usefulness."""
    report_json = report.model_dump_json(indent=2)
    request: dict[str, Any] = {
        "model": model,
        "input": [
            {
                "role": "user",
                "content": build_report_evaluation_prompt(report_json),
            }
        ],
        "structured_output_model": "ModelEvaluation",
        "structured_output_schema": ModelEvaluation.model_json_schema(),
    }
    if reasoning_effort is not None:
        request["reasoning"] = {"effort": reasoning_effort}

    parse_arguments: dict[str, Any] = {
        "model": model,
        "input": request["input"],
        "text_format": ModelEvaluation,
    }
    if reasoning_effort is not None:
        parse_arguments["reasoning"] = {"effort": reasoning_effort}
    response = client.responses.parse(**parse_arguments)
    if response.output_parsed is None:
        raise ValueError("OpenAI returned no structured report evaluation.")

    return ModelEvaluationRun(
        requested_at=datetime.now(timezone.utc),
        model=model,
        reasoning_effort=reasoning_effort,
        request=request,
        raw_response=response.model_dump(mode="json"),
        evaluation=ModelEvaluation.model_validate(response.output_parsed),
    )


def save_model_evaluation_run(
    evaluation_run: ModelEvaluationRun, output_directory: Path
) -> None:
    """Save local evidence for the evaluator request and response."""
    (output_directory / "evaluation-request.json").write_text(
        json.dumps(evaluation_run.request, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_directory / "evaluation-response.json").write_text(
        json.dumps(evaluation_run.raw_response, indent=2) + "\n",
        encoding="utf-8",
    )
