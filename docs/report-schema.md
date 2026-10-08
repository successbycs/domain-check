# Report schema and scoring

## Purpose

Each run will produce a report that lets a person understand the suggestions,
the evidence behind them, and what needs further checking.

## Output formats

- **JSON:** structured data for code and future integrations.
- **CSV:** one row per candidate for spreadsheet review.
- **Markdown:** a readable report for human review.

All three formats represent the same run and must include the run timestamp.

## Run metadata

Every report records the input filename, run timestamp, OpenAI model, prompt
version, Cloudflare lookup time, and any errors or missing information.

## Candidate information

Each candidate will include:

- proposed name and `.co.nz` domain;
- the reason it fits the company description;
- pronunciation and word-of-mouth assessment, with uncertainty;
- potential awkward, sensitive, cross-language, te reo Māori, or Māori
  cultural-affiliation concerns, with uncertainty and a human-review flag;
- possible name-conflict flag, explanation, and human-review requirement. This
  is not a trademark search or legal clearance;
- Cloudflare availability result, lookup timestamp, price, currency, and any
  lookup error. An available domain without a price is labelled `price unknown`;
- points awarded by the Python scoring formula;
- LLM editorial rank and written reason; and
- items requiring human review.

## Initial scoring rules

The score is calculated in Python from the recorded assessments. An unknown
result is worth zero points. The agreed starting rules are:

| Check | Result | Points |
| --- | --- | ---: |
| Availability | Available | +1 |
| Clarity | Excellent | +2 |
| Clarity | Good | +1 |
| Clarity | Poor | -1 |
| Pronunciation and word-of-mouth clarity | Easy to say | +1 |
| Pronunciation and word-of-mouth clarity | Unclear | 0 |
| Pronunciation and word-of-mouth clarity | Hard to say | -1 |
| Awkward associations | None found by the assessment | +1 |
| Awkward associations | Bad concern | -1 |
| Awkward associations | Very serious concern | -2 |

The report must show the individual points, not only the total.

## Editorial recommendation

The LLM may recommend a candidate that has fewer points, but must explain why.
For example, it might say that a name is shorter, easier to remember, or more
suited to the intended customers. This recommendation is separate from the
Python score and is not a measured confidence score.

In the CSV output, the LLM's recommendation and reason appear in separate
columns next to the Python points score.

## Evaluation results

The report includes two evaluation results:

1. **Rule-based evaluation:** checks that the report has ten distinct
   candidates, required evidence, timestamps, caveats, scores, and a priority
   list.
2. **Second-model evaluation:** asks another LLM to score the completed report
   from 1 to 5 against a written marketing and usefulness rubric. This is
   feedback, not proof that the answer is correct.
