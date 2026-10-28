"""The extraction step, the proposal file and the command line, with no network."""

from datetime import date
from pathlib import Path
import shutil
from typing import Any

import pytest

from session_docs import cli
from session_docs.extractor import check_against_transcript, extract_session_items
from session_docs.models import SessionExtraction, SessionItem
from session_docs.proposal import render_proposal, write_proposal
from session_docs.transcripts import Message

FIXTURES = Path(__file__).parent / "fixtures"


def make_item(title: str, quote: str, replaces: str = "none") -> SessionItem:
    return SessionItem(
        title=title, what=f"{title}.", why="", date="2026-10-28", source_quote=quote, replaces=replaces
    )


class FakeResponse:
    def __init__(self, extraction: SessionExtraction) -> None:
        self.output_parsed = extraction

    def model_dump(self, *, mode: str) -> dict[str, Any]:
        return {"id": "resp_test", "status": "completed"}


class FakeClient:
    """Records the request instead of sending it over the network."""

    def __init__(self, extraction: SessionExtraction) -> None:
        self.requests: list[dict[str, Any]] = []
        self.responses = self
        self.extraction = extraction

    def parse(self, **kwargs: Any) -> FakeResponse:
        self.requests.append(kwargs)
        return FakeResponse(self.extraction)


EXTRACTION = SessionExtraction(
    decisions=[
        make_item("Keep gpt-4o-mini", "yes agreed, keep gpt-4o-mini", replaces="D017"),
        make_item("Use Postgres", "we should use postgres"),
    ],
    open_questions=[],
    changed_plans=[],
    lessons=[make_item("Invented lesson", "this was never said")],
)


def test_extract_uses_structured_output() -> None:
    client = FakeClient(EXTRACTION)
    run = extract_session_items("prompt text", client, model="test-model")
    assert client.requests[0]["text_format"] is SessionExtraction
    assert client.requests[0]["input"] == [{"role": "user", "content": "prompt text"}]
    assert run.extraction == EXTRACTION


def test_too_large_prompt_is_refused_before_any_call() -> None:
    client = FakeClient(EXTRACTION)
    with pytest.raises(ValueError, match="limit"):
        extract_session_items("x" * 500_000, client)
    assert client.requests == []


def test_only_chris_agreement_counts_as_a_decision() -> None:
    messages = [
        Message("Claude", "t", "we should use postgres"),
        Message("Chris", "t", "Yes agreed,\nkeep gpt-4o-mini please"),
    ]
    checked, notes = check_against_transcript(EXTRACTION, messages)
    assert [d.title for d in checked.decisions] == ["Keep gpt-4o-mini"]
    assert [q.title for q in checked.open_questions] == ["Use Postgres"]
    assert "could not be found" in checked.open_questions[0].why
    assert checked.lessons[0].source_quote.endswith("(quote not found in transcript)")
    assert len(notes) == 2


def test_proposal_matches_the_stage_one_format(tmp_path: Path) -> None:
    text = render_proposal(EXTRACTION, "Claude Code session 2026-10-28", ["a note"])
    assert text.startswith("# Proposal: docs updates from Claude Code session 2026-10-28")
    assert "Status: waiting for approval" in text
    assert "1. **Keep gpt-4o-mini**" in text
    assert "   - Replaces: D017" in text
    assert "3. **Invented lesson**" in text
    assert "## Open questions\nNone found." in text
    first = write_proposal(text, tmp_path, "session", date(2026, 10, 28))
    second = write_proposal(text, tmp_path, "session", date(2026, 10, 28))
    assert first.name == "2026-10-28-session.md"
    assert second.name == "2026-10-28-session-2.md"


def make_project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    (project / "docs").mkdir(parents=True)
    (project / "docs" / "decisions.md").write_text("## D017 — Start with gpt-4o-mini\n", encoding="utf-8")
    shutil.copy(FIXTURES / "claude_session.jsonl", project / "session.jsonl")
    return project


def test_cli_without_send_makes_no_call_and_writes_no_proposal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    project = make_project(tmp_path)

    def no_network(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("no OpenAI call should be made without --send")

    monkeypatch.setattr(cli, "extract_session_items", no_network)
    assert cli.main(["--transcript", str(project / "session.jsonl"), "--project", str(project)]) == 0
    prompt = (project / "output" / "session-docs-prompt-session.txt").read_text(encoding="utf-8")
    assert "sk-proj-abcdefghijklmnopqrstuvwx1234" not in prompt
    assert "[REDACTED]" in prompt
    assert "D017" in prompt
    assert not (project / "docs" / "proposals").exists()
    assert "Nothing was sent" in capsys.readouterr().out


def test_cli_send_strips_secrets_before_the_call_and_writes_a_proposal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = make_project(tmp_path)
    client = FakeClient(EXTRACTION)
    monkeypatch.setattr("openai.OpenAI", lambda: client)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: None)

    assert cli.main(["--transcript", str(project / "session.jsonl"), "--project", str(project), "--send"]) == 0

    sent = client.requests[0]["input"][0]["content"]
    assert "sk-proj-abcdefghijklmnopqrstuvwx1234" not in sent
    assert "injected text Chris did not type" not in sent
    [proposal] = (project / "docs" / "proposals").glob("*.md")
    text = proposal.read_text(encoding="utf-8")
    assert "Keep gpt-4o-mini" in text
    assert "Claude Code session 2026-10-28 (session.jsonl)" in text
