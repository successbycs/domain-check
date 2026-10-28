# session_docs: docs proposals from saved sessions

This tool reads a saved Codex or Claude Code session and drafts a docs
proposal in `docs/proposals/`. It covers sessions that ended without anyone
saying "update the docs from this session". The proposal uses the same format
and the same approval step as
[docs/procedures/update-docs.md](../../docs/procedures/update-docs.md).
Nothing in the real docs changes until Chris approves.

It lives in `tools/`, separate from the domain research code in
`src/domain_agent/`.

## Where the transcripts are (checked on 28 Oct 2026)

| Tool | Location | Format |
| --- | --- | --- |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-<date>-<id>.jsonl` | One JSON record per line. The first record (`session_meta`) holds the project folder in `payload.cwd`. Discussion is in `response_item` records with `payload.type` `message` and `payload.role` `user` or `assistant`; the text is in `payload.content[].text`. Codex also adds its own `user` parts at the start (`<environment_context>`, `# AGENTS.md instructions`), which are skipped. |
| Claude Code | `~/.claude/projects/<project path with / replaced by ->/<session id>.jsonl` | One JSON record per line. Discussion is in records with `type` `user` or `assistant`; the text is in `message.content` (a string, or a list of parts with `type` `text`). Tool calls, tool results, thinking, subagent work (`isSidechain`), loaded skills (`isMeta`), summaries (`isCompactSummary`) and automatic messages (an `origin.kind` other than `human`) are skipped, as are `<system-reminder>` blocks inside Chris's messages. |

On this machine, the domain-check Codex sessions are from 8 and 13 October.
No Claude Code session has been started from the domain-check folder yet. Work
on domain-check from another folder's session is saved under that folder, so
use `--transcript` with its path.

On Windows outside WSL, `~` is your user folder, for example
`C:\Users\chris\.codex\sessions`.

## What it does

1. **Read** the transcript and keep only what Chris and the assistant said
   (`transcripts.py`). Messages over 40 lines are cut short, because they are
   usually pasted files or logs.
2. **Remove secrets** (`redaction.py`): API keys, tokens, `.env` style
   `NAME=value` lines, private keys, long random strings and 32-character hex
   IDs. This happens before anything is saved or sent.
3. **Build the prompt** (`prompt.py`) from the session and the current
   `docs/decisions.md`, and save it to `output/` so you can read exactly what
   would be sent.
4. **Only with `--send`:** call OpenAI with structured output
   (`extractor.py`), following the pattern in
   `src/domain_agent/candidate_generator.py`. The request and response are
   saved under `output/session-docs-<time>/`.
5. **Check the answer in code**: a decision stays a decision only if its
   quote is word for word in something Chris said. Otherwise it moves to open
   questions. Quotes not found in the transcript are marked.
6. **Write the proposal** to `docs/proposals/<date>-session-<tool>-<date>.md`
   (`proposal.py`). Then follow Step 5 of the procedure: approve, apply,
   delete the proposal.

## Commands

Run these from the domain-check folder. In WSL (Ubuntu), which is how this
project is set up:

```bash
# Look at what would be sent. Free: no OpenAI call.
PYTHONPATH=src:tools .venv/bin/python -m session_docs --latest --tool codex
PYTHONPATH=src:tools .venv/bin/python -m session_docs --transcript ~/.codex/sessions/2026/10/13/rollout-2026-10-13T15-52-57-01a1332d-6dc7-7682-92b7-274028842584.jsonl

# Make the paid call and write the proposal (needs OPENAI_API_KEY in .env).
PYTHONPATH=src:tools .venv/bin/python -m session_docs --latest --tool codex --send

# Run the tests. They make no network calls.
PYTHONPATH=src:tools .venv/bin/python -m pytest tools/session_docs/tests
```

In Windows PowerShell, with the project's virtual environment created there:

```powershell
$env:PYTHONPATH = "src;tools"
.venv\Scripts\python -m session_docs --latest --tool codex
.venv\Scripts\python -m pytest tools/session_docs/tests
```

Options:

- `--transcript <path>` or `--latest --tool codex|claude` chooses the session.
- `--tool` can be left out with `--transcript`; the tool is detected.
- `--project <folder>` is the project folder (default: the current folder).
- `--send` makes the paid OpenAI call. Without it nothing is sent.
- `--model` defaults to `gpt-4o-mini` (decision D017).

## Limits

- Sessions over 400,000 characters of discussion are refused rather than cut,
  so nothing is silently dropped.
- The model can miss things or misread them. The proposal is a draft: check
  each item against the session before approving.
- The secret patterns are broad but not perfect. Read the saved prompt in
  `output/` before using `--send` on a new kind of session.
