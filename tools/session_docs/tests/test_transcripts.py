"""Both readers turn a transcript into the same simple message list."""

import json
import os
from pathlib import Path

import pytest

from session_docs.transcripts import (
    MAX_LINES_PER_MESSAGE,
    detect_tool,
    find_latest_transcript,
    read_claude_transcript,
    read_codex_transcript,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_claude_reader_keeps_only_the_discussion() -> None:
    messages = read_claude_transcript(FIXTURES / "claude_session.jsonl")
    assert [(m.speaker, m.text) for m in messages] == [
        ("Chris", "Should we keep gpt-4o-mini?"),
        ("Claude", "I suggest keeping gpt-4o-mini because it is cheap."),
        (
            "Chris",
            "yes agreed, keep gpt-4o-mini. my key is "
            "OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwx1234",
        ),
    ]
    assert messages[0].timestamp == "2026-10-28T01:00:00Z"


def test_codex_reader_skips_injected_context_and_tools() -> None:
    messages = read_codex_transcript(FIXTURES / "codex_session.jsonl")
    assert [(m.speaker, m.text) for m in messages] == [
        ("Chris", "we will not be using jupyter notebook"),
        ("Codex", "Understood: plain Python files and tests."),
    ]


def test_detect_tool() -> None:
    assert detect_tool(FIXTURES / "claude_session.jsonl") == "claude"
    assert detect_tool(FIXTURES / "codex_session.jsonl") == "codex"


def test_long_messages_are_shortened(tmp_path: Path) -> None:
    long_text = "\n".join(f"line {n}" for n in range(100))
    record = {
        "type": "response_item",
        "timestamp": "t",
        "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": long_text}]},
    }
    path = tmp_path / "rollout-long.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    [message] = read_codex_transcript(path)
    assert len(message.text.splitlines()) == MAX_LINES_PER_MESSAGE + 1
    assert "60 more lines left out" in message.text


def test_find_latest_codex_session_for_the_project(tmp_path: Path) -> None:
    sessions = tmp_path / ".codex" / "sessions" / "2026" / "10" / "08"
    sessions.mkdir(parents=True)
    project = tmp_path / "domain-check"
    project.mkdir()
    other = tmp_path / "other"
    other.mkdir()

    def write(name: str, cwd: Path, mtime: int) -> Path:
        path = sessions / name
        path.write_text(json.dumps({"type": "session_meta", "payload": {"cwd": str(cwd)}}) + "\n", encoding="utf-8")
        os.utime(path, (mtime, mtime))
        return path

    write("rollout-old.jsonl", project, 100)
    newest = write("rollout-new.jsonl", project, 200)
    write("rollout-other.jsonl", other, 300)
    assert find_latest_transcript("codex", project, tmp_path) == newest


def test_find_latest_claude_session_uses_the_project_folder(tmp_path: Path) -> None:
    project = tmp_path / "domain-check"
    project.mkdir()
    folder = tmp_path / ".claude" / "projects" / str(project.resolve()).replace("/", "-")
    folder.mkdir(parents=True)
    path = folder / "abc.jsonl"
    path.write_text("{}\n", encoding="utf-8")
    assert find_latest_transcript("claude", project, tmp_path) == path


def test_missing_transcript_gives_a_clear_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="--transcript"):
        find_latest_transcript("claude", tmp_path, tmp_path)
