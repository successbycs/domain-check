# Agent instructions

Read and follow these project documents before working:

- `docs/communication-style.md` — how to communicate in this learning project.
- `docs/development-workflow.md` — how to make, test, and document changes.
- `docs/README.md` — where to find the source-of-truth project documents.

Put reusable code in `src/domain_agent/` and tests in `tests/`.

## Application versions

Use [the application-version skill](.agents/skills/application-versions/SKILL.md) when defining, sequencing or reporting a version or milestone. It keeps planned, implemented, merged, deployed and proven-live work distinct; it does not authorise delivery.

## PR maintenance compliance

Before review and merge, builders and reviewers must use
[pr-maintenance](.agents/skills/pr-maintenance/SKILL.md). Update affected schemas,
contracts, prompts and readable documentation together, run the relevant existing
checks, and record their results in the PR. The reviewer verifies this evidence.
This supplements the existing merge gates; it is not automated CI enforcement
and does not change approval, deployment or human-review authority.
