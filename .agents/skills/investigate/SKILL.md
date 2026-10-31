---
name: investigate
description: Investigate a bug or design gap and produce an evidence-backed local plan without implementing a fix.
---

# Investigate

Adapted from Shipright. Follow [AGENTS.md](../../../AGENTS.md) and [local workflow](../../../docs/development-workflow.md).

1. Confirm the requested investigation scope. Read the relevant code, design, issue and existing plan; preserve known authority and unrelated changes.
2. Reproduce with local/fake evidence where possible. Investigation does not authorise paid calls, publication or production changes. Label hypotheses.
3. Write the smallest plan allowed by [local planning rules](../../../docs/development-workflow.md): observed cause, options, chosen fix, affected files, meaningful checks and handover. Do not create Shipright's plan directory in this repo.
4. For agent gaps, apply the [agent charter](../../../docs/architecture/agent-charter.md): inspect who chooses work and next actions, not merely whether an SDK is imported.
5. Follow local review requirements. Leave implementation unstarted unless separately authorised; reuse explicit existing authorisation where it already covers the fix.
