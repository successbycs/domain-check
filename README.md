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
pytest
```

Try the current command-line input check with the included fictional example:

```bash
PYTHONPATH=src python3 -m domain_agent.cli --input examples/company_description.txt
```

This repository starts with structure only. Subsequent small steps will add
OpenAI API calls, domain lookups, and the agent workflow, each with a runnable
way to verify it.

## Proof-of-concept goal

The first usable version has one clear path:

```text
company description text file → Python command → research report
```

The report will contain ranked domain candidates, supporting evidence,
timestamps, caveats, and items requiring human review. It will also be checked
by a repeatable evaluation function.

Deployment as a website backend is a future possibility, not part of the PoC.

## Project layout

- `docs/` — project context, decisions, and learning notes.
- `src/domain_agent/` — reusable application package.
- `tests/` — automated tests for reusable application code.
