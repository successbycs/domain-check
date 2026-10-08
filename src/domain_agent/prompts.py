"""Prompt templates used by the Domain Research Agent."""

GENERATION_PROMPT_VERSION = "v1"
EVALUATION_PROMPT_VERSION = "v1"


def build_candidate_generation_prompt(company_description: str) -> str:
    """Return the approved Version 1 prompt for generating domain candidates."""
    return f"""You are helping research possible .co.nz domain names for a New Zealand company.

Generate exactly 10 distinct candidate names from the company description below.
Return only one JSON object. Do not return Markdown, a table, code fences, or
extra commentary.

You are not providing legal, trademark, linguistic, cultural, or domain-
availability clearance. Do not state that a domain is available, purchasable,
trademark-safe, or culturally safe.

Return a top-level JSON object with one field named `candidates`. Its value
must be an array containing exactly 10 candidate objects.

Every candidate object must have this exact structure:

{{
  "name": "candidate brand name",
  "domain": "lowercase-name.co.nz",
  "fit_reason": "why the name fits the company description",
  "clarity": "excellent, good, or poor",
  "pronunciation": {{
    "rating": "easy_to_say, unclear, or hard_to_say",
    "reason": "short explanation"
  }},
  "concerns": [
    {{
      "concern_type": "cross_language, te_reo_maori, or maori_cultural_affiliation",
      "explanation": "possible concern",
      "uncertainty_note": "why this needs human review",
      "requires_human_review": true
    }}
  ],
  "possible_name_conflict": {{
    "status": "not_identified or possible",
    "reason": "reason for the status",
    "requires_human_review": true
  }},
  "human_review_items": ["specific item to check"],
  "editorial_comment": "short comment on appeal to intended customers"
}}

Rules for candidate values:

1. Each `domain` must end in `.co.nz` and use only lowercase letters, numbers,
   and hyphens before `.co.nz`.
2. Do not repeat a name or domain.
3. `clarity` must be exactly `excellent`, `good`, or `poor`.
4. `pronunciation.rating` must be exactly `easy_to_say`, `unclear`, or
   `hard_to_say`.
5. `possible_name_conflict.status` must be exactly `not_identified` or
   `possible`.
6. Include a concern only when you identify a specific possible concern. An
   empty `concerns` array is allowed. Every concern is incomplete and requires
   human review.
7. Every `possible_name_conflict` requires human review, even when its status
   is `not_identified`.
8. Availability, price, provider, score, and final rank are checked or
   calculated later. Do not include them.

The downstream report table uses these JSON fields as columns:

- Candidate name: `name`
- .co.nz domain: `domain`
- Why it fits: `fit_reason`
- Clarity: `clarity`
- Pronunciation: `pronunciation.rating`
- Pronunciation reason: `pronunciation.reason`
- Possible concerns: `concerns`
- Possible name conflict: `possible_name_conflict`
- Human review needed: `human_review_items`
- LLM comment: `editorial_comment`

Company description:
---
{company_description}
---
"""


def build_report_evaluation_prompt(report_json: str) -> str:
    """Return the approved Version 1 prompt for reviewing a completed report."""
    return f"""You are reviewing a domain-name research report for a New Zealand business.

Assess the usefulness of the report for a human deciding which candidate names
to investigate further. Do not provide legal, trademark, linguistic, cultural,
or domain-availability clearance. Do not claim that any name is safe, available,
or suitable for use.

Consider:
1. Whether the candidate names appear connected to the company description.
2. Whether the report clearly separates confirmed provider evidence from model
   opinions and uncertainty.
3. Whether human-review items are specific and useful.
4. Whether the report makes it easy to compare the candidates.

Return only one JSON object with this exact structure:

{{
  "rating": 1,
  "strengths": ["specific useful strength"],
  "weaknesses": ["specific issue to improve"],
  "required_human_review_items": ["important item for a person to check"],
  "summary": "short plain-English overall assessment"
}}

Rules:
- `rating` must be an integer from 1 to 5.
- A rating of 1 means the report is not yet useful for comparison.
- A rating of 3 means the report is partly useful but has important gaps.
- A rating of 5 means the report is clear and useful for comparison, while
  still preserving uncertainty and human-review needs.
- Refer only to evidence present in the report.
- Do not invent facts, searches, prices, or availability results.
- Keep every item specific and short.

Report to review:
---
{report_json}
---
"""
