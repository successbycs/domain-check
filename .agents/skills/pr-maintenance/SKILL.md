---
name: pr-maintenance
description: Keep PR code, schemas, contracts, prompts and readable documentation aligned; require relevant checks and reviewer evidence before merge. Applies to builders and reviewers.
---

# PR maintenance

Adapted from Shipright's shared skill. Apply before requesting review and again
before merge. This supplements this repository's workflow; it does not replace
its scope, approval, reviewer, human-review or deployment rules.

## Builder

1. Read the complete diff against the target branch, including renamed/deleted files.
   Identify affected database fields/settings, migrations, API/tool inputs and outputs,
   generated schemas/types, prompt loading, fixtures and component responsibilities.
2. Update each affected contract and its existing readable documentation in the same
   PR. SQL alone is not a readable product schema. Describe field meanings, states,
   relationships and compatibility/migration effects where changed. Update prompt/tool
   catalogues only where they exist; do not invent a parallel registry or extra report.
3. Regenerate affected derived artifacts using the repository's existing generator.
   Inspect the exact semantic delta. Never refresh fixtures or snapshots blindly to make
   a failure pass; establish the intended behaviour and protect it with relevant checks.
4. Run this repository's relevant contract/schema freshness checks, scope checks and
   required tests from its documented workflow and actual scripts/configuration. If it
   has a standard contract command, use it. Do not copy Shipright-specific commands or
   claim a command exists without checking. Missing dependencies, skipped checks and
   timeouts are not passes. Required failures block merge until fixed or explicitly
   excepted by Chris; recording a failure alone is not an exception.
5. For prose-only/skill-only changes, validate changed links, file references and skill
   discovery plus `git diff --check`, subject to any stronger local gate. Changes to
   prompts, migrations, generated contracts or check commands are not prose-only.
   Behaviour tests remain separate from contract checks; neither proves live deployment.
6. Add a short **Maintenance** paragraph to the PR: affected contract/document owners
   (or why none change), exact commands/results, reviewed commit and remaining gaps.
   Re-run affected checks after relevant edits or a base change that affects the result.

## Reviewer and merge

Independently compare code and schema/contract/documentation changes against the
intended behaviour. Check generated deltas and changed expected values for hidden
regressions. Verify the commands cover the affected surfaces and the evidence matches
the revision being merged; rerun where evidence is missing or uncertain. Do not approve
stale required artifacts, failed/missing required checks or unsupported live claims.
Follow the repository's independent-review and merge authority, including human review
where required. The builder updates the artifacts; the reviewer verifies the result.

This is an explicit builder/reviewer compliance step, not automatic CI or branch
protection. Do not claim mechanical enforcement or weaken existing CI. No permission
for live services, spending, schema application or deployment is granted here.

## Local references

- [AGENTS.md](../../../AGENTS.md)
- [docs/architecture.md](../../../docs/architecture.md)
- [docs/report-schema.md](../../../docs/report-schema.md)
- [docs/development-workflow.md](../../../docs/development-workflow.md)
