---
name: project-charter
description: Create or revise a concise product charter before specifications, issues, and implementation. Use when defining a new project, version, or durable delivery rules.
---

# Project Charter

Create a charter that lets a team make consistent decisions while individual
specifications, Issues, and pull requests change. It is the project's durable
agreement, not a project plan or an implementation specification.

## Use the charter to decide

Capture the smallest set of decisions that must remain true across the stated
scope:

- the problem, intended outcome, and the proof that shows it works;
- in-scope and deliberately deferred work;
- architecture boundaries and named components;
- data ownership, contracts, and public/private separation;
- approval boundaries for external or irreversible actions;
- quality, testing, review, and merge requirements;
- the completion criteria for this version.

Write explicit decisions. If a detail is unknown, record it as an open decision
with an owner or trigger rather than inventing an answer.

## Workflow

1. Read the available product brief, existing architecture, repository rules,
   and prior decisions. Ask only for a decision that cannot be inferred and
   would materially change scope or safety.
2. State the smallest demonstrable outcome first. Use it to remove work that
   does not help prove the version.
3. Define system boundaries and data contracts before proposing tables, APIs,
   services, or delivery automation.
4. State durable delivery rules: the testing evidence required, review model,
   branch and merge rules, and any approval required before live external
   actions.
5. Write the charter in the repository's established documentation location.
   If none exists, propose a clear location such as `docs/<version>/build-charter.md`.
6. Check it against the review checklist in
   [references/charter-review.md](references/charter-review.md). Link the
   charter from the relevant architecture or documentation index.

## Boundaries

- Keep a charter short enough to be used. Put evolving implementation detail in
  specifications, Issues, or ADRs.
- Do not turn a charter into a list of tickets or prescribe code structure that
  has not been decided.
- A charter does not grant permission for deployments, purchases, publishing,
  credential use, or other external changes. Preserve the user's approval
  boundary.
- Revise the charter when a durable product decision changes; record which
  later decision supersedes an earlier one.

## Suggested shape

Use headings only where they help the project. A typical charter contains:

1. Purpose and proof
2. Scope and deferrals
3. Architecture and data boundaries
4. Operating and approval rules
5. Quality and merge gate
6. Completion criteria
7. Open decisions

For a review guide and a compact example, read
[references/charter-review.md](references/charter-review.md).
