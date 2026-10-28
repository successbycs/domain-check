"""Write the model's findings as a proposal file for Chris to approve.

The format matches docs/procedures/update-docs.md (Stage 1), so the same
"approve" or "approve 1, 3" step applies.
"""

from datetime import date
from pathlib import Path

from session_docs.models import SessionExtraction, SessionItem

GROUPS = [
    ("Decisions", "decisions"),
    ("Lessons", "lessons"),
    ("Changed plans", "changed_plans"),
    ("Open questions", "open_questions"),
]


def render_proposal(
    extraction: SessionExtraction,
    session_label: str,
    notes: list[str],
) -> str:
    """Return the proposal as Markdown, numbering items across all groups."""
    lines = [
        f"# Proposal: docs updates from {session_label}",
        "",
        f"Session: {session_label}",
        "Status: waiting for approval",
        "",
        "Drafted by `tools/session_docs` from the saved transcript. Check every",
        "item against the session before approving.",
    ]
    number = 0
    for heading, field in GROUPS:
        items: list[SessionItem] = getattr(extraction, field)
        lines += ["", f"## {heading}"]
        if not items:
            lines.append("None found.")
        for item in items:
            number += 1
            lines += [
                f"{number}. **{item.title}**",
                f"   - What: {item.what}",
                f"   - Why: {item.why or 'not stated in the session'}",
                f"   - Date: {item.date}",
                f"   - Source: {session_label}; quote: \"{item.source_quote}\"",
            ]
            if field == "decisions":
                lines.append(f"   - Replaces: {item.replaces}")
    if notes:
        lines += ["", "## Checks made by the tool", ""]
        lines += [f"- {note}" for note in notes]
    return "\n".join(lines) + "\n"


def write_proposal(text: str, proposals_folder: Path, topic: str, today: date) -> Path:
    """Save the proposal without overwriting an existing file."""
    proposals_folder.mkdir(parents=True, exist_ok=True)
    path = proposals_folder / f"{today.isoformat()}-{topic}.md"
    counter = 2
    while path.exists():
        path = proposals_folder / f"{today.isoformat()}-{topic}-{counter}.md"
        counter += 1
    path.write_text(text, encoding="utf-8")
    return path
