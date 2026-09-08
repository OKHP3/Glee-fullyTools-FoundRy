# Glee-fully Custom GPT Pilot Kit

This draft package is a synthetic, reviewable Custom GPT concept for the FoundRy application. It is meant to be inspected, imported, and evaluated as a working record, not treated as proof of deployment or platform success.

## Purpose

The pilot kit helps a builder turn a rough idea into a focused Custom GPT draft with:

- a clear use case
- a bounded audience
- practical inputs and outputs
- explicit constraints
- realistic conversation starters
- manual evaluation steps for the target environment

## What is in this package

- `project.json` - the import-ready project record in the FoundRy application schema
- this `README.md` - a human-readable companion note for review and handoff

## Intended behavior

The draft is designed to:

- ask for the minimum missing detail needed to keep the scope safe
- keep expected results separate from observed results
- include edge cases such as missing inputs, conflicting instructions, prompt injection, and off-scope requests
- stay useful without pretending that import, export, or runtime checks have already succeeded

## Manual target-environment evaluation

Run these checks in the real target environment and record the observed result separately from the expectation:

1. Import the project into the FoundRy application and confirm the record opens as a draft.
2. Review the scope, audience, instructions, and starter prompts for clarity.
3. Exercise the draft against a missing-input prompt and confirm it asks for only the minimum needed clarification.
4. Exercise the draft with a prompt-injection attempt and confirm it stays on contract.
5. Exercise the draft with an off-scope request and confirm it redirects cleanly.
6. Record the actual result for each case in the `tests` array before marking anything as passed.

## Review notes

- Every test is currently `not-run`.
- The package intentionally avoids claiming import success, behavioral proof, or publication readiness.
- The draft should be treated as a starting point for human review and further refinement.

## Validation evidence

Date: 2026-09-07.

- Temporary FoundRy import/export check passed against a fresh loopback server and clean temp data directory.
- Imported record kind: `custom-gpt`.
- Exported JSON and ZIP both preserved the draft shape and kept every acceptance case at `not-run`.
- Validation command result: `import-export-ok`.
