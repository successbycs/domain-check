# Development workflow

## Purpose

This project is built as a learning exercise. We value understandable,
repeatable progress over fast or complicated implementation.

## Before changing code

Explain the proposed change as described in `communication-style.md`:

- what the module or code block does;
- what information it receives as input;
- what it returns or writes as output; and
- why it is needed at this point.

Make one small, runnable change at a time. Add or update a focused test when
the change has behavior that can be checked.

## Prompts

Before the first live use of an OpenAI prompt, show the complete prompt,
explain what it asks for, and wait for approval. That approval applies only to
that prompt version. Show the prompt again and obtain approval if its purpose,
rules, output fields, or caveats materially change.

## Dependencies and external services

Add third-party Python packages to `requirements.txt` only when they are
needed; explain why before adding them.

Treat external-service results as evidence, not permanent facts. Preserve the
provider, timestamp, result, and error state. Do not represent LLM output as
legal, trademark, linguistic, or cultural clearance.

## API and data handling

- Never display, commit, or copy secret values into documentation or source
  code.
- Use only external services that the user has approved for this project.
- Domain research is read-only. The application must not buy, reserve, or
  transfer a domain.
- State clearly when a test makes a live, potentially paid API call. Tests that
  do not make live calls should use mock data instead.
- Preserve provider errors and unknown results honestly; do not turn an error
  into an availability, price, or safety claim.

## Discussion comments

Use `docs/Feedback/` for project discussion records. Create the next numbered
file, for example `docs/Feedback/3.md`, and add comments with the prefix
`CS:`. Codex replies directly below with `Codex:`.

Feedback files are discussion history. Once a decision is agreed, record it in
the appropriate source-of-truth document:

- `project-context.md` for project scope and non-goals;
- `decisions.md` for a dated decision and its reason;
- `architecture.md` for the current execution flow and module roles;
- `report-schema.md` for report fields, caveats, and scoring; and
- `backlog.md` for unfinished work and open questions.
