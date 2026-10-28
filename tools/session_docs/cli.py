"""Command line: turn one saved session into a docs proposal.

By default nothing is sent anywhere. The tool reads the transcript, removes
secrets, and saves the exact prompt to output/ so it can be checked. Add
--send to make the paid OpenAI call and write the proposal.
"""

import argparse
from datetime import date
from pathlib import Path

from session_docs.extractor import (
    DEFAULT_EXTRACTION_MODEL,
    MAX_PROMPT_CHARACTERS,
    build_prompt,
    check_against_transcript,
    extract_session_items,
    save_extraction_run,
)
from session_docs.proposal import render_proposal, write_proposal
from session_docs.redaction import redact_secrets
from session_docs.transcripts import (
    Message,
    detect_tool,
    find_latest_transcript,
    read_transcript,
)

TOOL_NAMES = {"claude": "Claude Code", "codex": "Codex"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m session_docs",
        description="Draft a docs proposal from a saved Codex or Claude Code session.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--transcript", type=Path, help="Path to a session .jsonl file.")
    source.add_argument("--latest", action="store_true", help="Use the newest session for this project.")
    parser.add_argument("--tool", choices=["codex", "claude"], help="Which tool wrote the session.")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project folder (default: here).")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Folder holding .claude and .codex.")
    parser.add_argument("--send", action="store_true", help="Make the paid OpenAI call and write the proposal.")
    parser.add_argument("--model", default=DEFAULT_EXTRACTION_MODEL, help="OpenAI model to use.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(argv)
    if options.latest and not options.tool:
        parser.error("--latest needs --tool codex or --tool claude.")

    try:
        if options.latest:
            path = find_latest_transcript(options.tool, options.project, options.home)
        else:
            path = options.transcript
        tool = options.tool or detect_tool(path)
        messages = read_transcript(path, tool)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if not messages:
        parser.error(f"No discussion found in {path}.")

    messages, removed = _redact_messages(messages)
    project = options.project.resolve()
    prompt = build_prompt(messages, project / "docs" / "decisions.md")
    # Check the finished prompt too, in case decisions.md held something.
    prompt, removed_from_prompt = redact_secrets(prompt)
    session_date = messages[0].timestamp[:10] or date.today().isoformat()
    session_label = f"{TOOL_NAMES[tool]} session {session_date} ({path.name})"

    print(f"Read {len(messages)} messages from {path}.")
    print(f"Secrets removed: {removed + removed_from_prompt}.")
    print(f"Prompt size: {len(prompt):,} characters (limit {MAX_PROMPT_CHARACTERS:,}).")

    output_folder = project / "output"
    output_folder.mkdir(exist_ok=True)
    prompt_file = output_folder / f"session-docs-prompt-{path.stem}.txt"
    prompt_file.write_text(prompt, encoding="utf-8")
    print(f"Saved the exact prompt to {prompt_file}.")

    if not options.send:
        print("Nothing was sent. Check the prompt, then run again with --send.")
        return 0

    from dotenv import load_dotenv
    from openai import OpenAI

    load_dotenv(project / ".env")
    print(f"Calling OpenAI ({options.model}). This is a paid call.")
    run = extract_session_items(prompt, OpenAI(), options.model)
    evidence_folder = save_extraction_run(run, output_folder)
    extraction, notes = check_against_transcript(run.extraction, messages)

    proposal = render_proposal(extraction, session_label, notes)
    topic = f"session-{tool}-{session_date}"
    proposal_path = write_proposal(proposal, project / "docs" / "proposals", topic, date.today())
    print(f"Saved the API evidence to {evidence_folder}.")
    print(f"Wrote the proposal to {proposal_path}. Nothing in the real docs has changed.")
    return 0


def _redact_messages(messages: list[Message]) -> tuple[list[Message], int]:
    """Remove secrets from every message before anything else uses them."""
    cleaned = []
    total = 0
    for message in messages:
        text, count = redact_secrets(message.text)
        total += count
        cleaned.append(Message(message.speaker, message.timestamp, text))
    return cleaned, total
