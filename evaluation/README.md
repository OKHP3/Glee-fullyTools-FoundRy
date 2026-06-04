# evaluation/ — GPT PulseBook Evaluation Rubrics

This folder contains the GPT PulseBook Evaluation framework — a structured rubric
for assessing the quality, compliance, and completeness of Glee-fully GPTs before
and after canonization.

## Files

| File | Version | Notes |
|------|---------|-------|
| `gpt-pulsebook-evaluation-v1-4.md` | v1.4 | Early rubric |
| `gpt-pulsebook-evaluation-v1-6.md` | v1.6 | Expanded criteria |
| `gpt-pulsebook-evaluation-v1-7.md` | v1.7 | **Latest** — use this for all current evaluations |

## When to Use

Run a PulseBook evaluation:
- Before marking a new GPT as PME-ready
- After a significant instruction update
- When a GPT has been flagged for tone drift
- As part of the PROMPT05 Fusion Checkpoint in the PromptChain

## Governance

Evaluation results should be logged in `canon/dataledger_registry_v3.md`
against the entity's record, and any tone violations logged in
`canon/dataledger_persona_v3.md` via `!DRIFT_EVENT`.
