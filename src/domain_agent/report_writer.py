"""Write report files produced by the Domain Research Agent."""

import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from domain_agent.models import ResearchReport


def write_research_report(report: ResearchReport, output_directory: Path) -> dict[str, Path]:
    """Write one report as JSON, CSV, and Markdown in ``output_directory``.

    Each file is created from the same checked ``ResearchReport`` object, so
    spreadsheet and human-readable views cannot silently drift from the JSON.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": output_directory / "report.json",
        "csv": output_directory / "report.csv",
        "markdown": output_directory / "report.md",
    }

    paths["json"].write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    _write_csv_report(report, paths["csv"])
    paths["markdown"].write_text(
        _render_markdown_report(report),
        encoding="utf-8",
    )
    return paths


def _write_csv_report(report: ResearchReport, output_path: Path) -> None:
    """Write one flat spreadsheet row for each candidate."""
    fieldnames = [
        "report_created_at",
        "input_filename",
        "generation_model",
        "prompt_version",
        "name",
        "domain",
        "fit_reason",
        "clarity",
        "pronunciation_rating",
        "pronunciation_reason",
        "concerns",
        "possible_name_conflict_status",
        "possible_name_conflict_reason",
        "human_review_items",
        "editorial_comment",
        "availability_status",
        "availability_provider",
        "availability_checked_at",
        "availability_price",
        "availability_currency",
        "availability_error",
        "availability_points",
        "clarity_points",
        "pronunciation_points",
        "association_points",
        "total_points",
        "rule_based_evaluation_passed",
        "model_evaluation_rating",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in report.candidates:
            generated = candidate.generated
            availability = candidate.availability
            writer.writerow(
                {
                    "report_created_at": report.created_at.isoformat(),
                    "input_filename": report.company_input.input_filename,
                    "generation_model": report.generation_model,
                    "prompt_version": report.prompt_version,
                    "name": generated.name,
                    "domain": generated.domain,
                    "fit_reason": generated.fit_reason,
                    "clarity": generated.clarity.value,
                    "pronunciation_rating": generated.pronunciation.rating.value,
                    "pronunciation_reason": generated.pronunciation.reason,
                    "concerns": json.dumps(
                        [concern.model_dump(mode="json") for concern in generated.concerns]
                    ),
                    "possible_name_conflict_status": (
                        generated.possible_name_conflict.status.value
                    ),
                    "possible_name_conflict_reason": (
                        generated.possible_name_conflict.reason
                    ),
                    "human_review_items": "; ".join(generated.human_review_items),
                    "editorial_comment": generated.editorial_comment,
                    "availability_status": availability.status.value,
                    "availability_provider": availability.provider or "",
                    "availability_checked_at": (
                        availability.checked_at.isoformat()
                        if availability.checked_at
                        else ""
                    ),
                    "availability_price": (
                        str(availability.price) if availability.price else ""
                    ),
                    "availability_currency": availability.currency or "",
                    "availability_error": availability.error or "",
                    "availability_points": candidate.score.availability_points,
                    "clarity_points": candidate.score.clarity_points,
                    "pronunciation_points": candidate.score.pronunciation_points,
                    "association_points": candidate.score.association_points,
                    "total_points": candidate.score.total_points,
                    "rule_based_evaluation_passed": (
                        str(report.rule_based_evaluation.passed).lower()
                        if report.rule_based_evaluation
                        else "not_run"
                    ),
                    "model_evaluation_rating": (
                        report.model_evaluation.rating
                        if report.model_evaluation
                        else "not_run"
                    ),
                }
            )


def _render_markdown_report(report: ResearchReport) -> str:
    """Return a readable report that preserves uncertainty and evidence gaps."""
    lines = [
        "# Domain Research Agent report",
        "",
        "## Run details",
        "",
        f"- Created at: {report.created_at.isoformat()}",
        f"- Input file: {report.company_input.input_filename}",
        f"- OpenAI model: {report.generation_model}",
        f"- Prompt version: {report.prompt_version}",
        "",
        "## Company description",
        "",
        report.company_input.description,
        "",
        "## Candidate summary",
        "",
        "| Name | Domain | Availability | Score | Human review needed |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for candidate in report.candidates:
        generated = candidate.generated
        availability = candidate.availability
        review_items = "; ".join(generated.human_review_items)
        lines.append(
            "| "
            f"{_markdown_cell(generated.name)} | "
            f"{_markdown_cell(generated.domain)} | "
            f"{availability.status.value} | "
            f"{candidate.score.total_points} | "
            f"{_markdown_cell(review_items)} |"
        )

    lines.extend(
        [
            "",
            "## Important caveats",
            "",
            "- Domain availability is evidence at the recorded lookup time, not a guarantee.",
            "- Name-conflict and cultural or cross-language concern flags are not legal, trademark, or cultural clearance.",
            "- `not_checked` means no availability lookup has been performed yet.",
            "",
        ]
    )
    lines.extend(_render_rule_based_evaluation(report))
    lines.extend(_render_model_evaluation(report))
    return "\n".join(lines)


def _markdown_cell(value: str) -> str:
    """Keep plain text safe inside a Markdown table cell."""
    return value.replace("|", "\\|").replace("\n", " ")


def _render_rule_based_evaluation(report: ResearchReport) -> list[str]:
    """Render the deterministic evaluation when the report has one."""
    evaluation = report.rule_based_evaluation
    if evaluation is None:
        return ["## Rule-based evaluation", "", "Not run.", ""]

    lines = [
        "## Rule-based evaluation",
        "",
        f"- Evaluated at: {evaluation.evaluated_at.isoformat()}",
        f"- Overall result: {'passed' if evaluation.passed else 'failed'}",
        "",
    ]
    for check in evaluation.checks:
        result = "passed" if check.passed else "failed"
        lines.append(f"- {check.name}: {result} — {check.detail}")
    lines.append("")
    return lines


def _render_model_evaluation(report: ResearchReport) -> list[str]:
    """Render the separate model review when the report has one."""
    evaluation = report.model_evaluation
    if evaluation is None:
        return ["## Model evaluation", "", "Not run.", ""]

    lines = [
        "## Model evaluation",
        "",
        f"- Rating: {evaluation.rating}/5",
        f"- Summary: {evaluation.summary}",
        "- Strengths:",
    ]
    lines.extend(f"  - {item}" for item in evaluation.strengths)
    lines.append("- Weaknesses:")
    lines.extend(f"  - {item}" for item in evaluation.weaknesses)
    lines.append("- Required human review:")
    lines.extend(f"  - {item}" for item in evaluation.required_human_review_items)
    lines.append("")
    return lines


def write_placeholder_report(
    *, description: str, input_path: Path, output_path: Path
) -> Path:
    """Write a Markdown report for a validated company description.

    This temporary report proves the local input-to-output flow. It does not
    generate names or call any external service.
    """
    created_at = datetime.now(timezone.utc).isoformat()
    report = f"""# Domain Research Agent report

## Run details

- Created at: {created_at}
- Input file: {input_path}
- OpenAI model: not used yet
- Prompt version: not used yet
- Cloudflare lookup: not run yet

## Company description

{description}

## Status

This is a placeholder report. No domain candidates, domain availability checks,
or external API calls have been made yet.
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path
