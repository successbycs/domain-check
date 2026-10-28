"""Send a session to OpenAI and check what comes back.

This follows the pattern in src/domain_agent/candidate_generator.py: the
OpenAI client is passed in, so tests can use a pretend client and no test
makes a network call.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Protocol

from session_docs.models import SessionExtraction, SessionItem
from session_docs.prompt import PROMPT_VERSION, build_extraction_prompt, format_transcript
from session_docs.transcripts import Message

DEFAULT_EXTRACTION_MODEL = "gpt-4o-mini"

# Stop before sending a very large session; gpt-4o-mini reads about four
# characters per token and accepts about 128,000 tokens.
MAX_PROMPT_CHARACTERS = 400_000


class ParsedResponse(Protocol):
    """The small part of an OpenAI parsed response this tool needs."""

    output_parsed: SessionExtraction | None

    def model_dump(self, *, mode: str) -> dict[str, Any]:
        """Return the complete API response as JSON-compatible data."""


class ResponsesResource(Protocol):
    """The structured-output operation used here."""

    def parse(self, **kwargs: Any) -> ParsedResponse:
        """Send a request and parse it with the supplied Pydantic model."""


class OpenAIClient(Protocol):
    """The part of the OpenAI client used here."""

    responses: ResponsesResource


@dataclass(frozen=True)
class ExtractionRun:
    """One OpenAI request, its raw response, and the checked result."""

    requested_at: datetime
    model: str
    prompt_version: str
    request: dict[str, Any]
    raw_response: dict[str, Any]
    extraction: SessionExtraction


def extract_session_items(
    prompt: str,
    client: OpenAIClient,
    model: str = DEFAULT_EXTRACTION_MODEL,
) -> ExtractionRun:
    """Ask the model for decisions, open questions, plan changes and lessons.

    The prompt must already have had secrets removed.
    """
    if len(prompt) > MAX_PROMPT_CHARACTERS:
        raise ValueError(
            f"The prompt is {len(prompt):,} characters, over the "
            f"{MAX_PROMPT_CHARACTERS:,} limit. Use a shorter session."
        )
    request: dict[str, Any] = {
        "model": model,
        "input": [{"role": "user", "content": prompt}],
        "structured_output_model": "SessionExtraction",
        "structured_output_schema": SessionExtraction.model_json_schema(),
    }
    response = client.responses.parse(
        model=model,
        input=request["input"],
        text_format=SessionExtraction,
    )
    if response.output_parsed is None:
        raise ValueError("OpenAI returned no structured response.")

    return ExtractionRun(
        requested_at=datetime.now(timezone.utc),
        model=model,
        prompt_version=PROMPT_VERSION,
        request=request,
        raw_response=response.model_dump(mode="json"),
        extraction=SessionExtraction.model_validate(response.output_parsed),
    )


def check_against_transcript(
    extraction: SessionExtraction, messages: list[Message]
) -> tuple[SessionExtraction, list[str]]:
    """Apply the "never write a decision Chris did not agree to" rule in code.

    A decision stays a decision only if its quote appears word for word in
    something Chris said. Otherwise it moves to open questions with a note.
    Any other item whose quote is not in the transcript gets a note too.
    """
    chris_text = _normalise(" ".join(m.text for m in messages if m.speaker == "Chris"))
    all_text = _normalise(" ".join(m.text for m in messages))
    notes: list[str] = []

    decisions: list[SessionItem] = []
    open_questions = list(extraction.open_questions)
    for item in extraction.decisions:
        if _normalise(item.source_quote) in chris_text:
            decisions.append(item)
        else:
            notes.append(f"Moved '{item.title}' to open questions: quote not found in Chris's words.")
            open_questions.append(
                item.model_copy(
                    update={
                        "why": (item.why + " " if item.why else "")
                        + "(Suggested as a decision, but Chris's agreement could not be found in the transcript.)",
                        "replaces": "none",
                    }
                )
            )

    def flag_unverified(items: list[SessionItem]) -> list[SessionItem]:
        checked = []
        for item in items:
            if _normalise(item.source_quote) not in all_text:
                notes.append(f"Quote for '{item.title}' was not found in the transcript.")
                item = item.model_copy(update={"source_quote": item.source_quote + " (quote not found in transcript)"})
            checked.append(item)
        return checked

    checked = SessionExtraction(
        decisions=decisions,
        open_questions=flag_unverified(open_questions),
        changed_plans=flag_unverified(extraction.changed_plans),
        lessons=flag_unverified(extraction.lessons),
    )
    return checked, notes


def build_prompt(messages: list[Message], decisions_path: Path) -> str:
    """Build the prompt from the session and the current decisions file."""
    existing = decisions_path.read_text(encoding="utf-8") if decisions_path.exists() else ""
    return build_extraction_prompt(format_transcript(messages), existing)


def save_extraction_run(run: ExtractionRun, output_root: Path = Path("output")) -> Path:
    """Write the request and response evidence to the ignored output folder."""
    timestamp = run.requested_at.strftime("%Y%m%dT%H%M%SZ")
    run_directory = output_root / f"session-docs-{timestamp}"
    run_directory.mkdir(parents=True, exist_ok=False)
    (run_directory / "request.json").write_text(json.dumps(run.request, indent=2) + "\n", encoding="utf-8")
    (run_directory / "response.json").write_text(json.dumps(run.raw_response, indent=2) + "\n", encoding="utf-8")
    (run_directory / "extraction.json").write_text(run.extraction.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return run_directory


def _normalise(text: str) -> str:
    """Lower-case and collapse spaces so line breaks do not break a match."""
    return " ".join(text.lower().split())
