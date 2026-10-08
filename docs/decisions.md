# Decisions

## 2026-10-08 — Use a `src/` package layout

Reusable code will live in `src/domain_agent/`, separate from tests. This
makes packaging and tests easier later.

## 2026-10-08 — Use Python files and tests for learning

This project will not use Jupyter notebooks. Small scripts and focused
automated tests will make each learning step runnable and reproducible.

## 2026-10-08 — Introduce integrations incrementally

The first milestone creates only the project foundation. OpenAI usage, domain
availability services, and agent orchestration will follow in small,
individually testable steps.

## 2026-10-08 — Optimize the first version for a file-to-report PoC

The first usable workflow will read a company-description text file and write
a research report. A website backend, database, queue, deployment setup, and
agent framework are explicitly deferred. The core remains framework-independent
so those additions can be made later without rewriting the research logic.

## 2026-10-08 — Evaluate reports separately from the workflow (superseded)

The project will include a repeatable `evaluate_report()` capability. Initial
checks will be deterministic and testable: candidate structure, completeness,
evidence fields, uncertainty statements, traceability, and human-review flags.
This initial decision was replaced by “Use two forms of evaluation” below,
which includes a second-model evaluation in Version 1.

## 2026-10-08 — Limit the PoC to `.co.nz`

The first version will generate and check `.co.nz` names only. Cloudflare
Registrar is the Version 1 provider for availability and price. The report
will record the provider and lookup timestamp.

## 2026-10-08 — Write three report formats

Each run will write JSON for structured data, CSV for spreadsheet review, and
Markdown for human review. All formats describe the same run.

## 2026-10-08 — Keep scoring and editorial recommendation separate

Python will calculate the agreed points score from recorded assessments. The
LLM may provide a separately labelled recommendation and reason, including
when it prefers a lower-scoring candidate. It must not be presented as a
measured confidence score.

## 2026-10-08 — Use two forms of evaluation

The project will validate required report fields and calculate scores with
rule-based Python checks. A second LLM call will also rate a completed report
from 1 to 5 against a written rubric. This second rating is useful feedback,
not proof of correctness.

## 2026-10-08 — Start with a simple agentic workflow (superseded)

This initial decision allowed one evaluation-and-refinement pass. It was
replaced by “Keep refinement for Version 2” below. Planning agents, persistent
memory, and multiple specialist agents remain deferred until a demonstrated
need arises.

## 2026-10-08 — Keep refinement for Version 2

Version 1 produces and evaluates one report. Version 2 may use the evaluation
result to request one revised set of candidates. Keeping this out of Version 1
makes each report easier to understand.

## 2026-10-08 — Score pronunciation and word-of-mouth clarity simply

Version 1 awards +1 when a name is easy to say, 0 when it is unclear, and -1
when it is hard to say. The assessment comes from the LLM and is marked as a
judgment with uncertainty.

## 2026-10-08 — Score possible associations without invented severity

Version 1 gives a candidate +1 when no possible associations were flagged and
-1 when one or more concerns were flagged. The current input schema has no
severity field, so it cannot honestly apply a more serious -2 penalty. A later
version can add that field and decision criteria if evidence shows it is useful.

## 2026-10-08 — Keep available names when price is unknown

If Cloudflare reports a domain as available but does not provide a price, it
will remain in the results with the label `price unknown`. Human review of real
reports will inform any later change to this rule.

## 2026-10-08 — Use cautious LLM concern flags in Version 1

Version 1 uses the LLM's general knowledge to flag possible cross-language,
te reo Māori, Māori cultural-affiliation, and name-conflict concerns. Every
such flag must state uncertainty and require human review. Research into more
specialised sources is deferred to Version 2.

## 2026-10-08 — Show LLM comments beside the calculated score

The report will place the LLM's written recommendation and reason in a
separate column beside the Python points score. This keeps the model's opinion
separate from the calculated score.

## 2026-10-08 — Start model testing with `gpt-4o-mini`

Version 1 will initially use `gpt-4o-mini` to keep test costs low. It supports
the fixed response format needed by this project. We will move to
`gpt-4.1-mini` or a newer model only if real reports show weak candidate
quality or unreliable formatting.
