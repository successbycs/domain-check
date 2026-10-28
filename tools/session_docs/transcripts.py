"""Read Codex and Claude Code transcripts into one simple message list.

Both tools save a session as a JSONL file: one JSON record per line. The
records differ between tools, so each tool has its own reader. Both readers
return the same `Message` objects, keeping only what Chris and the assistant
said to each other. Tool calls, tool output and injected instructions are
skipped.
"""

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterator, Literal

Tool = Literal["claude", "codex"]

# Messages longer than this are usually pasted files or logs, not discussion.
MAX_LINES_PER_MESSAGE = 40

# Text Claude Code adds to Chris's messages that he did not type.
CLAUDE_INJECTED_BLOCKS = re.compile(
    r"<(system-reminder|ide_selection|ide_opened_file|command-message|"
    r"command-name|command-args|local-command-stdout)>.*?</\1>",
    re.DOTALL,
)

# Codex adds these as separate "user" text parts at the start of a session.
CODEX_INJECTED_PREFIXES = (
    "<environment_context>",
    "<recommended_plugins>",
    "<user_instructions>",
    "<INSTRUCTIONS>",
    "# AGENTS.md instructions",
)


@dataclass(frozen=True)
class Message:
    """One turn of the discussion."""

    speaker: str
    timestamp: str
    text: str


def read_transcript(path: Path, tool: Tool) -> list[Message]:
    """Read a transcript with the reader for the given tool."""
    if tool == "claude":
        return read_claude_transcript(path)
    return read_codex_transcript(path)


def detect_tool(path: Path) -> Tool:
    """Guess which tool wrote a transcript from its first records."""
    for record in _records(path):
        if record.get("type") in ("session_meta", "response_item", "turn_context"):
            return "codex"
        if "sessionId" in record or "uuid" in record:
            return "claude"
    raise ValueError(f"Could not tell which tool wrote {path}.")


def read_claude_transcript(path: Path) -> list[Message]:
    """Read a Claude Code session file (~/.claude/projects/<project>/<id>.jsonl)."""
    messages = []
    for record in _records(path):
        role = record.get("type")
        if role not in ("user", "assistant"):
            continue
        # Skip subagent work, skill text and summaries that Chris did not type.
        if record.get("isSidechain") or record.get("isMeta"):
            continue
        if record.get("isCompactSummary"):
            continue
        origin = record.get("origin")
        if role == "user" and origin and origin.get("kind") != "human":
            continue

        content = record.get("message", {}).get("content")
        text = _join_text_parts(content, wanted_types=("text",))
        if role == "user":
            text = CLAUDE_INJECTED_BLOCKS.sub("", text)
        text = _trim(text)
        if text:
            speaker = "Chris" if role == "user" else "Claude"
            messages.append(Message(speaker, record.get("timestamp", ""), text))
    return messages


def read_codex_transcript(path: Path) -> list[Message]:
    """Read a Codex session file (~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl)."""
    messages = []
    for record in _records(path):
        payload = record.get("payload") or {}
        if record.get("type") != "response_item" or payload.get("type") != "message":
            continue
        role = payload.get("role")
        if role not in ("user", "assistant"):
            continue

        parts = [
            part
            for part in payload.get("content") or []
            if not str(part.get("text", "")).lstrip().startswith(CODEX_INJECTED_PREFIXES)
        ]
        text = _trim(_join_text_parts(parts, wanted_types=("input_text", "output_text")))
        if text:
            speaker = "Chris" if role == "user" else "Codex"
            messages.append(Message(speaker, record.get("timestamp", ""), text))
    return messages


def find_latest_transcript(tool: Tool, project: Path, home: Path) -> Path:
    """Return the newest transcript for a project folder.

    Claude Code keeps sessions in a folder named after the project path, with
    "/" and "." replaced by "-". Codex keeps all sessions together, so we read
    the first record of each file to find the project folder it ran in.
    """
    project = project.resolve()
    if tool == "claude":
        folder = home / ".claude" / "projects" / re.sub(r"[/.\\:]", "-", str(project))
        candidates = list(folder.glob("*.jsonl"))
    else:
        candidates = [
            path
            for path in (home / ".codex" / "sessions").rglob("rollout-*.jsonl")
            if _codex_session_folder(path) == str(project)
        ]
    if not candidates:
        raise FileNotFoundError(
            f"No {tool} transcript found for {project}. "
            "Use --transcript <path> to choose a file."
        )
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _codex_session_folder(path: Path) -> str | None:
    """Return the working folder recorded at the start of a Codex session."""
    for record in _records(path):
        if record.get("type") == "session_meta":
            return (record.get("payload") or {}).get("cwd")
        return None
    return None


def _records(path: Path) -> Iterator[dict[str, Any]]:
    """Yield each JSON record in a JSONL file, skipping unreadable lines."""
    with path.open(encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                yield record


def _join_text_parts(content: Any, wanted_types: tuple[str, ...]) -> str:
    """Join the text parts of a message, ignoring images and tool parts."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    texts = [
        part.get("text", "")
        for part in content
        if isinstance(part, dict) and part.get("type") in wanted_types
    ]
    return "\n".join(texts)


def _trim(text: str) -> str:
    """Shorten very long messages, which are usually pasted files or logs."""
    lines = text.strip().splitlines()
    if len(lines) <= MAX_LINES_PER_MESSAGE:
        return "\n".join(lines)
    kept = lines[:MAX_LINES_PER_MESSAGE]
    kept.append(f"[... {len(lines) - MAX_LINES_PER_MESSAGE} more lines left out]")
    return "\n".join(kept)
