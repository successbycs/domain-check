---
name: application-versions
description: Define, sequence and report application versions and milestones without confusing planned work, delivered code, deployment or live proof.
---

# Application versions

Use this skill when creating or changing a version or milestone, placing work in
one, reporting its status, or deciding whether later-version work may start.

## What each record owns

- **Version:** a coherent product scope, such as V4 or V4.5.
- **Milestone and issue:** the delivery record and its current scope.
- **Pull request:** a proposed change. A draft pull request is not delivery.
- **ExecPlan:** the current implementation findings and handover.
- **Design and specification:** the intended behaviour.

Do not use one record as proof of another. In particular, an issue being open,
labelled, or assigned to a milestone does not mean its behaviour is built or live.

## Use precise status language

| Say | Only when |
| --- | --- |
| **planned** | Scope is recorded but no work is authorised. |
| **ready** | Chris has explicitly authorised the issue or applied the label. Do not add this label yourself. |
| **in progress** | Authorised work has begun on the issue branch. |
| **implemented** | The scoped code or documentation exists and its checks pass. |
| **merged** | The pull request is merged to the default branch. |
| **deployed** | The merged change is running in its intended environment. |
| **proven live** | A named real-world check demonstrates the intended outcome. |
| **deferred** | The work remains useful but is intentionally not active. State the destination version or review point. |
| **complete** | The version's acceptance criteria are met and every in-scope item is delivered, deferred, moved, or withdrawn with evidence. |

Never shorten these distinctions into “done” when the evidence only supports one
of them. State the strongest claim that the records prove.

## Sequence versions deliberately

1. Read the current version's charter/design and inspect its open issues before
   proposing later-version work.
2. Reconcile the current version: finish an item, defer it, move it with a
   linked reason, or withdraw it. Do not silently leave it behind.
3. Create the next version or milestone with a concise outcome and boundaries.
4. Keep later-version issues and draft PRs **deferred** until Chris explicitly
   starts that version. A draft PR, a future milestone, or a plan never starts
   implementation.

For Shipright now, Version 4 is the active delivery sequence. Version 4.5 work,
including analytics, remains deferred until Version 4 has been reconciled and
Chris chooses to begin Version 4.5.

## Report a version clearly

Lead with the version and its real state, then name the evidence:

> Version 4 is active: comment-response work is merged and awaiting deployment
> proof; three scoped issues remain. Version 4.5 analytics is deferred.

For a completion claim, link the charter or acceptance record, the resolved
issues, and the live proof where one is required. If that evidence is missing,
say what remains instead of calling the version complete.

## Boundaries

This skill governs product language and sequencing. It does not grant build,
merge, deployment, or live-action authority. Follow the repository's issue,
review and deployment rules for those actions.
