"""Command-line entry point for the Domain Research Agent."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from domain_agent.input_reader import read_company_description
from domain_agent.report_writer import write_placeholder_report


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line interface used by the local application."""
    parser = argparse.ArgumentParser(
        description="Read a company description for domain research."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to a UTF-8 text file containing the company description.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/placeholder-report.md"),
        help="Path for the placeholder Markdown report.",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Read the requested input file and confirm that it is ready for research."""
    parser = build_parser()
    options = parser.parse_args(arguments)

    try:
        description = read_company_description(options.input)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    report_path = write_placeholder_report(
        description=description,
        input_path=options.input,
        output_path=options.output,
    )
    print(f"Read {len(description)} characters from {options.input}.")
    print(f"Wrote placeholder report to {report_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
