# Pilot Agent Skill Draft

This package is a bounded, reviewable draft for a portable Agent Skill.
It is designed to be imported, inspected, revised, and exported again without
pretending that any behavioral result has been proven.

## Purpose

Create a first-pass skill that is narrow enough to trigger predictably and
small enough to review quickly.

## What it should do

- State exactly when the skill applies.
- List the minimum inputs needed before writing.
- Describe a short, repeatable method.
- Include clear acceptance checks.
- End with a handoff that names the artifact and next validation step.

## What it should not do

- It should not claim publication readiness.
- It should not claim tested runtime behavior unless that evidence was actually run.
- It should not expand into a general-purpose instruction set.
- It should not depend on hidden tools or external services.

## Suggested validation

1. Import `project.json` into the FoundRy application.
2. Export the project as `SKILL.md` and inspect the generated frontmatter.
3. Check that the draft still names a bounded trigger, inputs, method, checks, and handoff.
4. Confirm the acceptance cases are specific, observable, and still marked `not-run`.

## Reviewer notes

The draft is intentionally synthetic. Its value is in showing the importer-friendly
shape of a useful Agent Skill spec, not in claiming real evaluation evidence.
