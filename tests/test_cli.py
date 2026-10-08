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


def test_cli_verbose_mode_shows_safe_local_pipeline_stages(
    tmp_path: Path, capsys: object
) -> None:
    """Verbose mode explains module calls without making external requests."""
    description_file = tmp_path / "company.txt"
    description_file.write_text("A New Zealand coffee roaster.")

    exit_code = main(
        [
            "--input",
            str(description_file),
            "--output",
            str(tmp_path / "report.md"),
            "--verbose",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "[input_reader] Reading and validating" in captured.out
    assert "[report_writer] Writing the placeholder report" in captured.out
