# Procedure: update the docs from this session

Use this when Chris says **"update the docs from this session"**. It works the
same way in Codex and Claude Code: it only asks the agent to read, write files
and wait for approval.

The repository docs are the source of truth. Nothing reaches them until Chris
approves it.

## Step 1 — Gather what happened

1. Read the current conversation from the start.
2. List the changes made this session: run `git status` and `git diff`, and
   `git log` for any commits made today.
3. Note any Feedback file (`docs/Feedback/<n>.md`) that was written or
   answered this session.

## Step 2 — Pick out only what was decided or learned

Sort each item into one of four groups:

| Group | What belongs here | Goes to |
| --- | --- | --- |
| Decisions | Something Chris clearly agreed to, such as "yes", "agreed" or "do that". | `docs/decisions.md` |
| Lessons | Something we learned by doing, such as a test result, an error and its cause, or a surprise. | `docs/learning-log.md` |
| Changed plans | Work added, finished, moved or dropped. | `docs/backlog.md` |
| Open questions | Ideas discussed but not agreed, and anything you are unsure about. | `docs/backlog.md` |

Also check `docs/architecture.md` when the way the program runs has changed.

Rules:

- **Never** put something under Decisions unless Chris agreed to it. If you are
  unsure, put it under Open questions and say why.
- Skip small talk, dead ends that taught nothing, and routine steps.
- Keep each item to at most three sentences.

For each item record:

- **What:** the decision, lesson, plan change or question.
- **Why:** the reason given in the session.
- **Date:** YYYY-MM-DD.
- **Source:** where it came from, for example `Codex session 2026-10-28`,
  `Claude Code session 2026-10-28`, a commit hash, or a Feedback file and line.

## Step 3 — Compare with the existing docs

1. Read `docs/decisions.md`, `docs/learning-log.md`, `docs/backlog.md` and
   `docs/architecture.md`.
2. Drop items that are already recorded.
3. If a new decision replaces an old one, plan to set the old entry's status to
   `Superseded by D<new ID> on <date>`. Never delete the old entry.
4. If a backlog item is now done or dropped, plan to move or mark it, not erase
   its history.

## Step 4 — Write a proposal, not the real docs

1. Create `docs/proposals/<YYYY-MM-DD>-<short-topic>.md` using the format below.
2. Number every item (1, 2, 3 …) so Chris can approve some and not others.
3. Show Chris a short summary: how many items in each group, and the file path.
4. **Do not edit the real docs yet.**

Proposal format:

```markdown
# Proposal: <short topic>

Session: <Codex or Claude Code> session <YYYY-MM-DD>
Status: waiting for approval

## Decisions
1. **<Decision title>**
   - What: …
   - Why: …
   - Date: YYYY-MM-DD
   - Source: …
   - Replaces: D<old ID> (or "none")

## Lessons
2. **<Lesson title>**
   - What: … / Why: … / Date: … / Source: …

## Changed plans
3. **<Backlog change>**
   - What: … / Why: … / Date: … / Source: …

## Open questions
4. **<Question>**
   - What: … / Why it is still open: … / Date: … / Source: …
```

## Step 5 — Apply only after approval

Wait for Chris to say **"approve"** (all items) or **"approve 1, 3"** (chosen
items). Then:

1. Add each approved decision to `docs/decisions.md` in the entry format below,
   using the next free ID. Mark any replaced decision as superseded.
2. Add approved lessons to `docs/learning-log.md` under a dated heading.
3. Apply approved plan changes and open questions to `docs/backlog.md`, and
   update `docs/architecture.md` if the item changes how the program runs.
4. Items Chris did not approve stay out. If he wants to keep one for later,
   move it to Open questions in `docs/backlog.md`.
5. Delete the proposal file.
6. Show Chris what changed. Do not commit or push unless he asks.

## Decision entry format (`docs/decisions.md`)

```markdown
## D018 — <short decision title>

- **Date:** YYYY-MM-DD
- **Status:** Accepted
- **Decision:** <what was decided, at most three sentences>
- **Reason:** <why>
- **Source:** <session, commit hash, Feedback file and line, or PR link>
```

`Status` is either `Accepted` or `Superseded by D<ID> on <YYYY-MM-DD>`. IDs
count up and are never reused.
