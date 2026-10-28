# Decisions

Each entry follows the format in [procedures/update-docs.md](procedures/update-docs.md). Status is `Accepted` or `Superseded by D<ID> on <date>`. IDs are never reused.

## D001 — Use a `src/` package layout

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Reusable code will live in `src/domain_agent/`, separate from tests.
- **Reason:** This makes packaging and tests easier later.
- **Source:** recorded in commit 71832c4

## D002 — Use Python files and tests for learning

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** This project will not use Jupyter notebooks.
- **Reason:** Small scripts and focused automated tests will make each learning step runnable and reproducible.
- **Source:** recorded in commit 71832c4

## D003 — Introduce integrations incrementally

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** The first milestone creates only the project foundation. OpenAI usage, domain availability services, and agent orchestration will follow in small, individually testable steps.
- **Reason:** Each step stays small enough to understand and test on its own.
- **Source:** recorded in commit 71832c4

## D004 — Optimize the first version for a file-to-report PoC

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** The first usable workflow will read a company-description text file and write a research report. A website backend, database, queue, deployment setup, and agent framework are explicitly deferred.
- **Reason:** The core remains framework-independent so those additions can be made later without rewriting the research logic.
- **Source:** recorded in commit 71832c4

## D005 — Evaluate reports separately from the workflow

- **Date:** 2026-10-08
- **Status:** Superseded by D009 on 2026-10-08
- **Decision:** The project will include a repeatable `evaluate_report()` capability. Initial checks will be deterministic and testable: candidate structure, completeness, evidence fields, uncertainty statements, traceability, and human-review flags.
- **Reason:** Report quality can be checked the same way on every run.
- **Source:** docs/Feedback/1.md lines 53–55; recorded in commit 71832c4

## D006 — Limit the PoC to `.co.nz`

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** The first version will generate and check `.co.nz` names only. Cloudflare Registrar is the Version 1 provider for availability and price, and the report will record the provider and lookup timestamp.
- **Reason:** One extension and one provider keep the PoC simple; the provider can sell `.co.nz` domains.
- **Source:** docs/Feedback/1.md lines 4–8 and docs/Feedback/2.md line 108; recorded in commit 71832c4

## D007 — Write three report formats

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Each run will write JSON for structured data, CSV for spreadsheet review, and Markdown for human review. All formats describe the same run.
- **Reason:** Each format suits a different use: structured data, spreadsheet review and human reading.
- **Source:** recorded in commit 71832c4

## D008 — Keep scoring and editorial recommendation separate

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Python will calculate the agreed points score from recorded assessments. The LLM may provide a separately labelled recommendation and reason, including when it prefers a lower-scoring candidate.
- **Reason:** The recommendation must not be presented as a measured confidence score.
- **Source:** docs/Feedback/1.md line 50; recorded in commit 71832c4

## D009 — Use two forms of evaluation

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** The project will validate required report fields and calculate scores with rule-based Python checks. A second LLM call will also rate a completed report from 1 to 5 against a written rubric.
- **Reason:** This second rating is useful feedback, not proof of correctness.
- **Source:** docs/Feedback/1.md lines 53–59; recorded in commit 71832c4

## D010 — Start with a simple agentic workflow

- **Date:** 2026-10-08
- **Status:** Superseded by D011 on 2026-10-08
- **Decision:** This initial decision allowed one evaluation-and-refinement pass. Planning agents, persistent memory, and multiple specialist agents remain deferred until a demonstrated need arises.
- **Reason:** Start with the simplest useful workflow.
- **Source:** docs/Feedback/1.md lines 69–73; recorded in commit 71832c4

## D011 — Keep refinement for Version 2

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Version 1 produces and evaluates one report. Version 2 may use the evaluation result to request one revised set of candidates.
- **Reason:** Keeping this out of Version 1 makes each report easier to understand.
- **Source:** docs/Feedback/2.md lines 35–37; recorded in commit 71832c4

## D012 — Score pronunciation and word-of-mouth clarity simply

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Version 1 awards +1 when a name is easy to say, 0 when it is unclear, and -1 when it is hard to say. The assessment comes from the LLM and is marked as a judgment with uncertainty.
- **Reason:** A simple three-step score is enough for a first version.
- **Source:** docs/Feedback/2.md line 111; recorded in commit 71832c4

## D013 — Score possible associations without invented severity

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Version 1 gives a candidate +1 when no possible associations were flagged and -1 when one or more concerns were flagged. A later version can add a severity field and decision criteria if evidence shows it is useful.
- **Reason:** The current input schema has no severity field, so it cannot honestly apply a more serious -2 penalty.
- **Source:** commit 2296b5e

## D014 — Keep available names when price is unknown

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** If Cloudflare reports a domain as available but does not provide a price, it will remain in the results with the label `price unknown`.
- **Reason:** Human review of real reports will inform any later change to this rule.
- **Source:** docs/Feedback/2.md lines 118–121; recorded in commit 71832c4

## D015 — Use cautious LLM concern flags in Version 1

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Version 1 uses the LLM's general knowledge to flag possible cross-language, te reo Māori, Māori cultural-affiliation, and name-conflict concerns. Every such flag must state uncertainty and require human review.
- **Reason:** Research into more specialised sources is deferred to Version 2.
- **Source:** docs/Feedback/2.md lines 45–47; recorded in commit 71832c4

## D016 — Show LLM comments beside the calculated score

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** The report will place the LLM's written recommendation and reason in a separate column beside the Python points score.
- **Reason:** This keeps the model's opinion separate from the calculated score.
- **Source:** recorded in commit 71832c4

## D017 — Start model testing with `gpt-4o-mini`

- **Date:** 2026-10-08
- **Status:** Accepted
- **Decision:** Version 1 will initially use `gpt-4o-mini`. We will move to `gpt-4.1-mini` or a newer model only if real reports show weak candidate quality or unreliable formatting.
- **Reason:** It keeps test costs low and supports the fixed response format needed by this project.
- **Source:** recorded in commit 71832c4
