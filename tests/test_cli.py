"""Tests for the local command-line interface."""

from pathlib import Path

from domain_agent.cli import main


def test_cli_reads_the_requested_company_description(
    tmp_path: Path, capsys: object
) -> None:
    """The command confirms that it read a valid input file."""
    description_file = tmp_path / "company.txt"
    description = "A New Zealand coffee roaster."
    description_file.write_text(description)
    report_path = tmp_path / "report.md"

    exit_code = main(
        ["--input", str(description_file), "--output", str(report_path)]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert f"Read {len(description)} characters" in captured.out
    assert str(description_file) in captured.out
    assert f"Wrote placeholder report to {report_path}" in captured.out
    assert report_path.exists()
