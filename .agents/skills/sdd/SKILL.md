---
name: sdd
description: Apply the imported Shipright specification-to-evidence approach using this repository's local workflow.
---

# Specification-driven development

Imported and adapted from Shipright at Chris's request. Existing local SDD and
[AGENTS.md](../../../AGENTS.md) take precedence; this is not a second delivery process.

Read the owning issue, current specification/design, [workflow](../../../docs/development-workflow.md)
and [planning rules](../../../docs/development-workflow.md). State the user outcome and observable acceptance
check. Use an issue plan for small work and the local ExecPlan process where required.
Keep design and implementation aligned. Preserve known user approval; a planning-only
request does not authorise code or live effects. Use start-issue/investigate/review-pr
when applicable, following the existing local review and merge gates.

For agent features apply the [agent charter](../../../docs/architecture/agent-charter.md).
Keep the smallest useful proof genuinely agentic when that is the requested design:
reduce data/scope, not the decision-making under test. Record real evidence and what
is still unproven. Do not import Shipright-specific versions, schemas, tools, commands,
readiness labels, agent counts or deployment permissions into this product.
