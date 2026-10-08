"""Tests for the initial Markdown report writer."""

from pathlib import Path

from domain_agent.report_writer import write_placeholder_report


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
