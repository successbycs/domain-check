# Domain Research Agent

A proof-of-concept Python application for researching and ranking potential
domain names from a company description.

The project is being built incrementally with normal Python files and tests.
Reusable application code lives in `src/domain_agent/`, separate from test
code, so it can later run as a standalone application.

## Initial setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the test suite with:

```bash
PYTHONPATH=src .venv/bin/python -m pytest
```

Run the complete workflow with safe progress messages:

```bash
PYTHONPATH=src .venv/bin/python -m domain_agent.cli \
  --input examples/knocknoc_company_description.txt \
  --generate \
  --verbose
```

This makes two OpenAI calls and one read-only Cloudflare lookup. It writes a
timestamped folder under `output/` containing the API evidence and final JSON,
CSV, and Markdown reports.

## Debugging in VS Code

Open the repository folder in VS Code, open **Run and Debug**, choose a launch
choice, and press **F5**.

- **Domain Agent: placeholder (free)** runs only the local input-to-placeholder
  report path.
- **Domain Agent: full workflow (paid)** runs OpenAI generation, Cloudflare
  lookup, scoring, and the model evaluation.

To pause the program, click in the left margin beside a line number to set a
breakpoint. Good first breakpoints are:

- `src/domain_agent/cli.py` on `generation_run = generate_candidates(...)`;
- `src/domain_agent/cloudflare_lookup.py` on `response = self.session.post(...)`;
- `src/domain_agent/scorer.py` on the `return ScoreBreakdown(...)` line.

When execution pauses, use **Step Over** to run the next line, **Step Into** to
enter the called function, and the **Variables** panel to inspect current data.

## Proof-of-concept goal

The first usable version has one clear path:

```text
company description text file → Python command → research report
```

The report contains ranked domain candidates, supporting evidence, timestamps,
caveats, items requiring human review, a rule-based evaluation, and a separate
model evaluation.

Deployment as a website backend is a future possibility, not part of the PoC.

## Project layout

- `docs/` — project context, decisions, and learning notes.
- `src/domain_agent/` — reusable application package.
- `tests/` — automated tests for reusable application code.
