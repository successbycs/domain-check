# Project context

## Purpose

Domain Research Agent is a proof-of-concept standalone Python application
built as a learning project. It will help research possible domain names from
a company description while preserving evidence, uncertainty, and cases that
need human judgment.

## Proof-of-concept boundary

The PoC has a simple, file-based input/output flow:

```text
company description text file → Python command → research report
```

The first version will not include a website, database, job queue, deployment
configuration, or a general-purpose agent framework. The reusable core should
remain independent of a future web layer so it can become a backend later.

The first scope is `.co.nz` domains only. Cloudflare Registrar will supply the
availability and price evidence for each candidate in Version 1.

## Intended workflow

1. Read a company description from a text file.
2. Ask an OpenAI model for ten domain-name candidates.
3. Assess pronunciation and word-of-mouth clarity.
4. Screen for potentially negative or awkward cross-language associations,
   while clearly communicating uncertainty and requiring human review.
5. Use Cloudflare Registrar to check `.co.nz` availability and price.
6. Rank candidates and write JSON, CSV, and Markdown reports with evidence,
   timestamps, caveats, and items requiring human review.
7. Evaluate the report with a repeatable quality function.

## Evaluation requirement

The project will include an evaluation function separate from the research
workflow. Its first version will use deterministic checks for report quality:

- ten distinct, plausibly domain-shaped candidates;
- an explanation connecting each candidate to the company description;
- explanations and stated caveats for each candidate;
- explicit uncertainty for pronunciation and cross-language assessments;
- source, timestamp, and success/error status for each domain lookup;
- a ranking that can be traced to recorded evidence; and
- clear items requiring human review.

Fixed test inputs and expected structural outcomes will make the rule-based
checks repeatable. A second model will also score the completed report from 1
to 5 against a written rubric; this is feedback, not proof of correctness.

Version 1 ends after the report and its evaluations are produced. A later
Version 2 may use evaluation feedback to request one revised set of candidates.

## Working approach

- Build in small, runnable steps.
- Use normal Python files and automated tests for exploration, testing, and
  learning.
- Move reusable logic into normal Python modules under `src/domain_agent/`.
- Keep the eventual application runnable directly from the command line.
- Do not treat automated language or availability checks as definitive legal,
  linguistic, or brand-clearance advice.
- Explain work in plain English and introduce code in small, runnable steps.
