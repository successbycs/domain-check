"""Tests for report output files."""

import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from domain_agent.models import (
    CandidateGeneration,
    CompanyDescriptionInput,
    ResearchCandidate,
    ResearchReport,
)
from domain_agent.report_writer import write_placeholder_report, write_research_report
from tests.test_models import make_generated_candidate


def test_writes_a_placeholder_markdown_report(tmp_path: Path) -> None:
    """The report includes input, metadata labels, and an honest status."""
    output_path = tmp_path / "reports" / "report.md"

    written_path = write_placeholder_report(
        description="A small New Zealand coffee roaster.",
        input_path=Path("company.txt"),
        output_path=output_path,
    )

    report = written_path.read_text(encoding="utf-8")
    assert written_path == output_path
    assert "# Domain Research Agent report" in report
    assert "A small New Zealand coffee roaster." in report
    assert "OpenAI model: not used yet" in report
    assert "Cloudflare lookup: not run yet" in report
    assert "No domain candidates" in report


def test_writes_matching_json_csv_and_markdown_reports(tmp_path: Path) -> None:
    """The three output formats describe the same generated candidates."""
    generation = CandidateGeneration(
        candidates=[make_generated_candidate(number=index) for index in range(10)]
    )
    report = ResearchReport(
        created_at=datetime(2026, 10, 8, 7, 0, tzinfo=timezone.utc),
        company_input=CompanyDescriptionInput(
            input_filename="company.txt",
            description="A New Zealand coffee roaster.",
        ),
        generation_model="gpt-4o-mini",
        prompt_version="v1",
        candidates=[ResearchCandidate(generated=item) for item in generation.candidates],
    )

    paths = write_research_report(report, tmp_path / "report")

    json_report = json.loads(paths["json"].read_text(encoding="utf-8"))
    with paths["csv"].open(encoding="utf-8", newline="") as csv_file:
        csv_rows = list(csv.DictReader(csv_file))
    markdown_report = paths["markdown"].read_text(encoding="utf-8")

    assert len(json_report["candidates"]) == 10
    assert len(csv_rows) == 10
    assert csv_rows[0]["domain"] == "harbourbean0.co.nz"
    assert csv_rows[0]["availability_status"] == "not_checked"
    assert csv_rows[0]["rule_based_evaluation_passed"] == "not_run"
    assert csv_rows[0]["model_evaluation_rating"] == "not_run"
    assert "# Domain Research Agent report" in markdown_report
    assert "harbourbean0.co.nz" in markdown_report
    assert "not_checked" in markdown_report
