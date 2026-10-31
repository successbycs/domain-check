---
name: start-issue
description: Start or resume an authorised scoped issue using this repository's own workflow.
---

# Start issue

Adapted from Shipright's builder skill at Chris's request. Local rules take precedence.

1. Read [AGENTS.md](../../../AGENTS.md), the owning issue, [local workflow](../../../docs/development-workflow.md), relevant design and current worktree state.
2. Preserve explicit session authorisation and unrelated work. Do not import Shipright readiness labels, branch/merge permissions or deployment authority.
3. Record the scoped outcome, files and acceptance evidence before code. Follow the local branch/PR rules; do not duplicate existing work.
4. Use the repository's [planning rules](../../../docs/development-workflow.md) for material work. A plan request is not implementation approval.
5. Build the smallest authorised slice. For agent behaviour read the [agent charter](../../../docs/architecture/agent-charter.md); identify model decisions, deterministic tools and runtime separately.
6. Run the project's real scoped checks, record results and remaining gaps. Do not substitute Shipright commands or invent CI gates.
7. Follow local review/merge rules, record Built by and Reviewed by where a PR is used. Independent model review must not be claimed as self-review. Stop at the authorised delivery boundary; a merge is not deployment approval.
