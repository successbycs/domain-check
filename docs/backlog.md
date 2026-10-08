# Backlog

## Next

1. Design and approve the first OpenAI prompt, then add an OpenAI call to
   generate ten candidates in a structured format.
2. Implement the points formula and complete JSON, CSV, and Markdown report
   writers.

## Research before integration

- Define the written rubric for the second-model evaluation.
- Confirm Cloudflare account, billing, and API-token requirements, then perform
  a read-only `.co.nz` availability-and-price check.
- Review `gpt-4o-mini` output from representative company descriptions and
  move to a stronger model only if needed.

## Later, only if the PoC demonstrates a need

- Research specialist sources for cross-language and cultural concern checks.
- IPONZ trademark-search integration.
- FastAPI or Cloudflare-hosted web/API entry point.
- Learn and add CI with GitHub Actions so every code change automatically runs
  `PYTHONPATH=src pytest`; consider deployment only after the local PoC works.
- Remembering prior accepted and rejected names.
- One evaluation-and-refinement loop or multiple specialist agents.
