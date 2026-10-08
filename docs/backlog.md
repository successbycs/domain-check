# Backlog

## Next

1. Design and approve the first OpenAI prompt, then add an OpenAI call to
   generate ten candidates in a structured format.
2. Implement the points formula and complete JSON, CSV, and Markdown report
   writers.

## Research before integration

- Define the written rubric for the second-model evaluation.
- Confirm Cloudflare account, billing, and API-token requirements, then perform
  a read-only `.co.nz` availability-and-price check.
- Review `gpt-4o-mini` output from representative company descriptions and
  move to a stronger model only if needed.

## Later, only if the PoC demonstrates a need

- Research specialist sources for cross-language and cultural concern checks.
- IPONZ trademark-search integration.
- FastAPI or Cloudflare-hosted web/API entry point.
- Learn and add CI with GitHub Actions so every code change automatically runs
  `PYTHONPATH=src pytest`; consider deployment only after the local PoC works.
- Remembering prior accepted and rejected names.
- One evaluation-and-refinement loop or multiple specialist agents.

## Version 2 research candidates

These are references to assess later. They are not installed, connected, or
approved as application dependencies.

- [mcp-domain-availability](https://github.com/imprvhub/mcp-domain-availability)
  is an MCP server that checks domains through RDAP, WHOIS, and DNS. Assess it
  as a possible alternative or additional availability source. First confirm
  whether it supports `.co.nz`, whether its results and rate limits are useful
  for this product, and how its `available`, `taken`, and `undetermined`
  statuses map to our evidence model. It is not a registrar or a purchase tool.
- [awesome-codex-skills](https://github.com/composio-community/awesome-codex-skills)
  is a catalogue of optional skills for Codex development work. Review only
  individual skills that solve a demonstrated project problem; assess their
  source, permissions, external services, and instructions before installation.
  This catalogue does not become part of the deployed Domain Research Agent.
- [codex-seo](https://github.com/AgriciDaniel/codex-seo) is a large SEO analysis
  skill suite with optional third-party services. It is outside the current
  domain-research PoC. Consider it only if a later product need includes website
  or SEO analysis, and assess its credentials, dependencies, permissions, and
  overlap with existing tooling before installation.
- [OpenAI Ads](https://ads.openai.com/) is an advertising product for reaching
  people in ChatGPT as they explore and compare options. It is not an API or a
  Domain Research Agent feature. Consider it only after a deployable product,
  target customer, budget, landing page, and a way to measure sign-ups or sales
  have been defined.

## Version 2: run observability and cost estimates

- Record the start time, finish time, elapsed milliseconds, success state, and
  error state for every OpenAI and Cloudflare request.
- Record OpenAI input, output, total, and cached-input tokens when returned by
  the API. Calculate a clearly labelled estimated USD cost per OpenAI call and
  per report run from recorded, versioned price rates. Do not present the
  estimate as an invoice; the OpenAI billing dashboard or Costs API is the
  source of truth for actual spend.
- Include this information in the JSON report and a readable summary in the
  Markdown report; make it available in CSV where a per-candidate value is
  meaningful.

## Version 3 research: human shortlist validation

- [PickFu case studies](https://www.pickfu.com/case-studies) describe consumer
  feedback research and link to survey, API, and MCP material. Assess it as a
  possible optional human-validation step after the automated report has
  produced a shortlist.
- Before any integration, define the research question, intended respondent
  group (including New Zealand relevance), sample size, consent and privacy
  approach, budget, and how human feedback will be shown separately from the
  application’s calculated score.
- Do not automatically create surveys, contact respondents, or spend money.
  A human must approve the question, audience, budget, and launch of every
  study.
