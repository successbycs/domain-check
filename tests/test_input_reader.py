"""Tests for reading company-description files."""

from pathlib import Path

import pytest

from domain_agent.input_reader import read_company_description


def test_reads_company_description_without_surrounding_whitespace(
    tmp_path: Path,
) -> None:
    """The input reader returns usable text rather than blank padding."""
    description_file = tmp_path / "company.txt"
    description_file.write_text("\n  A small New Zealand coffee roaster.  \n")

    assert read_company_description(description_file) == (
        "A small New Zealand coffee roaster."
    )


def test_rejects_an_empty_company_description(tmp_path: Path) -> None:
    """An empty input should fail early with a clear message."""
    description_file = tmp_path / "company.txt"
    description_file.write_text("  \n\t")

    with pytest.raises(ValueError, match="Company description file is empty"):
        read_company_description(description_file)
