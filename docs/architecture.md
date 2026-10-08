# Architecture

## Current state

The repository can read and validate a company-description text file through a
small command-line interface, write a placeholder Markdown report, and store
checked candidate data in Pydantic models. It does not yet make OpenAI calls or
domain lookups.

## Intended PoC flow

```text
company description text file
        ↓
command-line program
        ↓
OpenAI candidate generation and assessments
        ↓
.co.nz availability and price lookup from Cloudflare Registrar
        ↓
Python scoring and LLM editorial recommendation
        ↓
JSON, CSV, and Markdown reports
        ↓
report evaluation
```

## Planned parts and their responsibilities

| Part | Responsibility |
| --- | --- |
| Command-line program | Reads a company-description file and writes report files. |
| Candidate generator | Calls OpenAI to propose ten domain-name candidates and provide written assessments. |
| Availability provider | Checks `.co.nz` availability and price with Cloudflare Registrar. It is a normal Python module, not a web API in the PoC. |
| Scorer | Applies the agreed points formula consistently to the collected information. |
| Report writer | Writes the same results as JSON, CSV, and Markdown. |
| Evaluator | Checks report completeness and scoring, then asks a second model to review the report against a written rubric. |

## Important boundaries

- The command-line program is the first way to run the PoC.
- The Python modules must not depend on a website or FastAPI.
- If this becomes an MVP, a FastAPI endpoint or a Cloudflare-hosted website can
  call the same Python workflow rather than duplicate it.
- LLM opinions, availability results, and pricing are evidence with timestamps;
  they are not permanent guarantees or legal, trademark, or cultural clearance.

## Agentic pattern for the PoC

Version 1 uses one straightforward sequence of steps and ends after writing
and evaluating a report. Version 2 may add one refinement pass. Neither
version uses a planner, stored memory, or multiple cooperating agents unless a
real limitation shows that one is needed.
