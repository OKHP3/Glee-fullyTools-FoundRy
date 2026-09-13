# evaluation/ — GPT PulseBook Evaluation Framework

> A structured quality-assurance system for assessing Glee-fully GPTs before and after
> canonization. The PulseBook framework produces a comprehensive evaluation document
> (a "Pulsebook") for each GPT — covering identity, tone, function coverage, canon
> compliance, and deployment readiness.

---

## Purpose

The `evaluation/` folder contains the **GPT PulseBook Evaluation** rubric — a
specialized prompt/template that activates a structured review session for any GPT
in the ecosystem. Think of it as a pre-flight checklist and quality inspection rolled
into one: before a GPT is marked PME-ready and deployed, it passes through a PulseBook
review to confirm it meets the canonical standard.

The PulseBook rubric is also used as a diagnostic tool when a GPT shows signs of tone
drift, instruction decay, or behavioral inconsistency post-deployment.

---

## Files

| File | Version | Status | Notes |
|------|---------|--------|-------|
| [`gpt-pulsebook-evaluation-v1-7.md`](gpt-pulsebook-evaluation-v1-7.md) | v1.7 | **Current — use this** | Full Canvas-mode output, cleanroom directive, complete v1.7 template |
| [`gpt-pulsebook-evaluation-v1-6.md`](gpt-pulsebook-evaluation-v1-6.md) | v1.6 | Superseded | Expanded criteria over v1.4 |
| [`gpt-pulsebook-evaluation-v1-4.md`](gpt-pulsebook-evaluation-v1-4.md) | v1.4 | Legacy | Original rubric baseline |

---

## What a PulseBook Captures

Each PulseBook evaluation output is a structured Markdown document (generated in
ChatGPT Canvas mode) that covers:

| Section | What It Captures |
|---------|-----------------|
| **Identity Header** | GPT name, role, ecosystem, version, visibility, model |
| **Ownership Record** | Creator, contact, SLA tier, risk level, tags |
| **Tone & Persona Audit** | Overlay assignment, tone compliance score, drift events |
| **Function Coverage** | Every declared Function and Function-ette — present and complete? |
| **Canon Compliance** | CanonSeal status, !CLAUSE ID presence, ledger routing confirmed |
| **Instruction Quality** | Structure, ordering, completeness per canonical block spec |
| **Conversation Starters** | All 12 starters reviewed for tone and scope alignment |
| **PME Readiness** | Final go/no-go for deployment: Persona, Metadata, Export checks |
| **Open Gaps** | Clearly-marked assumption fields and operator-input stubs |

---

## When to Run a PulseBook Evaluation

| Trigger | Action |
|---------|--------|
| New GPT reaching end of PromptChain (PROMPT05) | Run v1.7 before marking PME-ready |
| Existing GPT updated with new instructions | Run v1.7 to confirm compliance |
| GPT flagged for tone drift or behavioral inconsistency | Run v1.7 as diagnostic |
| Formal registry entry being created or updated | Run v1.7 to populate metadata fields |
| Child repo release preparation | Run v1.7 for each new Tool-ette |

---

## How to Use the Evaluation Files

These files are **prompt payloads** — paste `gpt-pulsebook-evaluation-v1-7.md`
into a ChatGPT session with the GPT's existing instructions attached as a knowledge
file or pasted inline. The session will:

1. Activate **Cleanroom Mode** (no heritage bleed from other GPTs)
2. Guide the operator to provide GPT content
3. Populate all fields from the provided content
4. Fill gaps with clearly-marked assumptions
5. Output a complete Pulsebook v1.7 in Canvas mode

---

## Output Governance

After a PulseBook is completed:

- **Evaluation result** → log summary in `canon/dataledger-registry-v3.md` on the entity's record
- **Tone violations found** → log as `!DRIFT_EVENT` in `canon/dataledger-persona-v3.md`
- **Open gaps** → promote incomplete stubs to `canon/dataledger-ideation-v3.md` for resolution
- **PME-ready confirmed** → entity is eligible for deployment in ChatGPT Builder

---

## Version History

| Version | Key Changes |
|---------|------------|
| v1.7 | Canvas mode enforcement, cleanroom directive, full schema template with ownership record |
| v1.6 | Expanded compliance criteria, tone audit section added |
| v1.4 | Original rubric — baseline identity, function, and PME readiness checks |

---

## Relationship to Other Folders

```
evaluation/    <-- validates entities against --> canon/ (registry, persona, parameters)
evaluation/    <-- triggered at end of       --> prompts/ (PROMPT05 Fusion Checkpoint)
evaluation/    <-- produces input for        --> canon/dataledger-registry-v3.md
evaluation/    <-- used to populate          --> inventory/ (entity descriptions)
```
