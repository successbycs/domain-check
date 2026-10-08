"""Command-line entry point for the Domain Research Agent."""

import argparse
from collections.abc import Sequence
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from domain_agent.candidate_generator import (
    DEFAULT_GENERATION_MODEL,
    generate_candidates,
    save_generation_run,
)
from domain_agent.cloudflare_lookup import CloudflareRegistrarClient
from domain_agent.evaluator import evaluate_report
from domain_agent.input_reader import read_company_description
from domain_agent.llm_evaluator import (
    DEFAULT_EVALUATION_MODEL,
    evaluate_report_with_model,
    save_model_evaluation_run,
)
from domain_agent.models import CompanyDescriptionInput, ResearchCandidate, ResearchReport
from domain_agent.prompts import GENERATION_PROMPT_VERSION
from domain_agent.report_writer import write_placeholder_report, write_research_report
from domain_agent.scorer import score_candidate


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
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Call OpenAI and save the request and response evidence locally.",
    )
    parser.add_argument(
        "--generation-output-directory",
        type=Path,
        default=Path("output"),
        help="Directory for saved OpenAI generation evidence.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show the safe pipeline stages as the command runs.",
    )
    parser.add_argument(
        "--openai-model",
        default=DEFAULT_GENERATION_MODEL,
        help=(
            "OpenAI model for candidate generation and model evaluation "
            f"(default: {DEFAULT_GENERATION_MODEL})."
        ),
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["low", "medium", "high", "xhigh", "max"],
        default=None,
        help="Optional OpenAI reasoning level for models that support it.",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Read the requested input file and confirm that it is ready for research."""
    parser = build_parser()
    options = parser.parse_args(arguments)

    _announce(options.verbose, "[input_reader] Reading and validating the company description.")
    try:
        description = read_company_description(options.input)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Read {len(description)} characters from {options.input}.")

    if options.generate:
        load_dotenv()
        company_input = CompanyDescriptionInput(
            input_filename=str(options.input),
            description=description,
        )
        _announce(
            options.verbose,
            "[candidate_generator] Calling OpenAI to generate ten candidates.",
        )
        _announce(
            options.verbose,
            "[candidate_generator] "
            f"Model: {options.openai_model}; "
            f"reasoning effort: {options.reasoning_effort or 'not set'}.",
        )
        generation_run = generate_candidates(
            company_input=company_input,
            client=OpenAI(),
            model=options.openai_model,
            reasoning_effort=options.reasoning_effort,
        )
        _announce(
            options.verbose,
            "[candidate_generator] Saving the OpenAI request and response evidence.",
        )
        run_directory = save_generation_run(
            generation_run,
            options.generation_output_directory,
        )
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        if not account_id or not api_token:
            parser.error(
                "--generate requires CLOUDFLARE_ACCOUNT_ID and "
                "CLOUDFLARE_API_TOKEN in .env."
            )
        _announce(
            options.verbose,
            "[cloudflare_lookup] Checking the ten .co.nz domains with Cloudflare.",
        )
        availability_by_domain = CloudflareRegistrarClient(
            account_id=account_id,
            api_token=api_token,
        ).check_domains(
            [candidate.domain for candidate in generation_run.candidates.candidates]
        )
        _announce(
            options.verbose,
            "[scorer] Calculating visible Python points for each candidate.",
        )
        report = ResearchReport(
                created_at=generation_run.requested_at,
                company_input=company_input,
                generation_model=generation_run.model,
                prompt_version=GENERATION_PROMPT_VERSION,
                candidates=[
                    ResearchCandidate(
                        generated=candidate,
                        availability=availability_by_domain[candidate.domain],
                        score=score_candidate(
                            ResearchCandidate(
                                generated=candidate,
                                availability=availability_by_domain[candidate.domain],
                            )
                        ),
                    )
                    for candidate in generation_run.candidates.candidates
                ],
        )
        _announce(
            options.verbose,
            "[evaluator] Running deterministic completeness and score checks.",
        )
        report = report.model_copy(
            update={"rule_based_evaluation": evaluate_report(report)}
        )
        _announce(
            options.verbose,
            "[llm_evaluator] Calling OpenAI to review the completed report.",
        )
        evaluation_model = (
            options.openai_model
            if options.openai_model != DEFAULT_GENERATION_MODEL
            else DEFAULT_EVALUATION_MODEL
        )
        evaluation_run = evaluate_report_with_model(
            report,
            OpenAI(),
            model=evaluation_model,
            reasoning_effort=options.reasoning_effort,
        )
        save_model_evaluation_run(evaluation_run, run_directory)
        report = report.model_copy(
            update={"model_evaluation": evaluation_run.evaluation}
        )
        _announce(
            options.verbose,
            "[report_writer] Writing the final JSON, CSV, and Markdown reports.",
        )
        report_paths = write_research_report(
            report,
            run_directory,
        )
        print(f"Saved OpenAI request and response evidence to {run_directory}.")
        print(f"Wrote JSON report to {report_paths['json']}.")
        print(f"Wrote CSV report to {report_paths['csv']}.")
        print(f"Wrote Markdown report to {report_paths['markdown']}.")
        return 0

    _announce(
        options.verbose,
        "[report_writer] Writing the placeholder report without external calls.",
    )
    report_path = write_placeholder_report(
        description=description,
        input_path=options.input,
        output_path=options.output,
    )
    print(f"Wrote placeholder report to {report_path}.")
    return 0


def _announce(verbose: bool, message: str) -> None:
    """Print a safe learning-oriented progress message when requested."""
    if verbose:
        print(message)


if __name__ == "__main__":
    raise SystemExit(main())
