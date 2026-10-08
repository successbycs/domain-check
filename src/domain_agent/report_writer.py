"""Write the first human-readable report produced by the application."""

from datetime import datetime, timezone
from pathlib import Path


def write_placeholder_report(
    *, description: str, input_path: Path, output_path: Path
) -> Path:
    """Write a Markdown report for a validated company description.

    This temporary report proves the local input-to-output flow. It does not
    generate names or call any external service.
    """
    created_at = datetime.now(timezone.utc).isoformat()
    report = f"""# Domain Research Agent report

## Run details

- Created at: {created_at}
- Input file: {input_path}
- OpenAI model: not used yet
- Prompt version: not used yet
- Cloudflare lookup: not run yet

## Company description

{description}

## Status

This is a placeholder report. No domain candidates, domain availability checks,
or external API calls have been made yet.
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return output_path
