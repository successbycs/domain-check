# Agent instructions

Read and follow these project documents before working:

- `docs/communication-style.md` — how to communicate in this learning project.
- `docs/development-workflow.md` — how to make, test, and document changes.
- `docs/README.md` — where to find the source-of-truth project documents.

Put reusable code in `src/domain_agent/` and tests in `tests/`.

## Application versions

Use [the application-version skill](.agents/skills/application-versions/SKILL.md) when defining, sequencing or reporting a version or milestone. It keeps planned, implemented, merged, deployed and proven-live work distinct; it does not authorise delivery.

## Reconcile linked issues after delivery

Within this repository’s existing authority and workflow rules, link each PR to its
scoped issue. Use a closing keyword only when merging satisfies all remaining
acceptance and approval requirements; otherwise use a non-closing reference.
After merge, and again after any required deployment, live proof or human review,
check the actual issue state and record links to evidence. Close it only when its
retained acceptance is met and this repository permits closure. Otherwise keep it
open with the next action, dependency and accurate implemented, merged, deployed
or proven status. If an issue closed before required proof, reopen it when permitted
and explain what remains. Do not silently move version scope. This is a builder
workflow rule, not an automated GitHub gate.
