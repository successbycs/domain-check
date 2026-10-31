# Agent instructions

Read and follow these project documents before working:

- `docs/communication-style.md` — how to communicate in this learning project.
- `docs/development-workflow.md` — how to make, test, and document changes.
- `docs/README.md` — where to find the source-of-truth project documents.

Put reusable code in `src/domain_agent/` and tests in `tests/`.

## Updating the docs from a session

When Chris says **"update the docs from this session"**, follow
`docs/procedures/update-docs.md`. It writes a proposal to `docs/proposals/`
first. Real docs change only after Chris approves.

## Agent architecture and imported builder skills

Read [the agent architecture charter](docs/architecture/agent-charter.md) when
changing application-agent objectives, tools, prompts, work selection or lifecycle.
It requires honest decision ownership and observable proof; it does not replace the
local product design or authorise new runtime agents/background execution.

Imported from Shipright and adapted to this repository: [start-issue](.agents/skills/start-issue/SKILL.md),
[investigate](.agents/skills/investigate/SKILL.md), [review-pr](.agents/skills/review-pr/SKILL.md),
[SDD reference](.agents/skills/sdd/SKILL.md), and
[project-charter](.codex/skills/project-charter/SKILL.md). Codex and Claude can discover
these through their skill directories. Existing local workflows, SDD, prompt approvals,
review/merge checks and production permissions take precedence over imported examples.
