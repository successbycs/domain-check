"""Read and validate the company description supplied to the application."""

from pathlib import Path


def read_company_description(path: Path) -> str:
    """Return non-empty UTF-8 text from a company-description file.

    Args:
        path: The location of the text file supplied by the user.

    Raises:
        ValueError: If the file contains only whitespace.
    """
    description = path.read_text(encoding="utf-8").strip()

    if not description:
        raise ValueError("Company description file is empty.")

    return description
