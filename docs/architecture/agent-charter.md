# Agent architecture charter

Agreed with Chris on 31 October 2026. This is lasting design guidance for builders
and reviewers. Versioned specifications define implementation details; Issues and
ExecPlans track delivery. This document does not claim autonomy is already delivered.

## The agreement

An agent receives an objective and available tools. It discovers relevant work,
chooses its next action from the evidence, uses tools, observes the result and
continues or decides when to check again. Its model owns those decisions.

Application code implements tools, maintains execution and enforces concrete
business rules. It must not silently replace the agent's decisions with a fixed
business sequence and describe that sequence as autonomous agent behaviour.
A manually started, bounded agent can still be agentic. Background execution alone
also does not make a workflow agentic. State both decision ownership and lifecycle.

## domain-check's local scope

This guidance was imported from Shipright at Chris's request on 31 October 2026.
It does not import Shipright's two-agent count, social publishing rules or deployment
authority. The [existing local design](../../docs/architecture.md) defines product components.
The existing domain-check PoC explicitly uses a finite sequence of steps and no
planner/multiple cooperating agents. Preserve that choice until an agreed product
change supersedes it. Describe it honestly as a workflow; this import does not itself
claim or implement autonomous execution. Domain lookup remains read-only.

For future work explicitly requested as agentic, specify the model's objective,
available tools, decisions and stopping/waiting behaviour. Keep runtime mechanics
and deterministic validation separate. Do not add a coordinator or extra agent as a
substitute for giving an existing agent the tools its agreed role needs. A fixed
workflow remains valid where deliberately chosen; do not call it autonomous merely
because one step uses an LLM. A bounded manually started agent can still be agentic.

## Evidence required before claiming delivery

- Identify the objective, registered tools and actual prompt for each agent.
- Review where item selection and next-action decisions happen in code.
- Demonstrate more than one available item: show the agent discovering/selecting work,
  using tools, observing results and continuing or choosing to wait.
- Demonstrate the relevant product rules without replacing model-owned decisions.
- Test persistence, validation and applicable product rules with fake clients. Scripted fake-model
  calls prove tool mechanics, not that a live model makes the intended decisions.
- Record observed model-selected tool calls and resulting state changes in an
  authorised live proof before claiming live autonomy. State runtime prerequisites,
  how to stop it, and any unobserved parts. An SDK import or saved plan alone is not proof.

Keep evidence concise and free of credentials or hidden reasoning. A short actionable
plan, tool names, selected IDs, outcomes and timestamps are enough. Do not add a tracing
platform, framework or extra agent merely to produce evidence.

## How future work uses this charter

Read it before changing agent tools, prompts, selection, orchestration or lifecycle.
Specifications must say what the model decides, what tools enforce and what the runtime
does. PR review checks that division against the implementation and the evidence above.

This charter is guidance for future agentic changes, not authority to rewrite the
current product workflow. Existing local approval, prompt, testing, review and release
rules remain in force. A copy of this document does not grant credentials, spending,
deployment or external-action approval. Record an explicit agreed design change before
altering the local architecture. Keep delivery status in the repository's own records.
