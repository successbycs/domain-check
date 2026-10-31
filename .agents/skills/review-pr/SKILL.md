---
name: review-pr
description: Independently review a code or planning pull request against this repository's design and evidence.
---

# Review PR

Adapted from Shipright; [AGENTS.md](../../../AGENTS.md) and [local workflow](../../../docs/development-workflow.md) own the actual gates.

1. Confirm independence from the builder; use a different model when local rules require it. Read the issue, approved design, whole diff and evidence.
2. Check behaviour, scope, meaningful tests, documentation and unresolved limitations. A plan is not implemented behaviour; a successful mock is not a live proof.
3. For agent changes use the [agent charter](../../../docs/architecture/agent-charter.md). Identify who selects items/actions and what the observed model tool calls demonstrate. Do not accept a fixed scripted pipeline as autonomous simply because it invokes an LLM.
4. Reproduce appropriate local checks. Do not make live paid calls or external mutations as review tests without authority. No invented Shipright test commands or gates.
5. Record numbered must-fix/suggestion findings, approve/revise/reject verdict, evidence/limits and Reviewed by. Update review metadata without changing the implementation under review.
6. Builder resolves findings; local rules govern merge and release. Review approval does not authorise deployment or expand scope.
