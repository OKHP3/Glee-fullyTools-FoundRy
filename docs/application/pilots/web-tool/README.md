# Incident Intake Log

This pilot brief describes how to adapt the exported web-tool starter into a small
incident intake record manager.

## What is already implemented in the starter

The exported baseline already provides:

- Local add, complete, reopen, and filter behavior
- Browser persistence for the record list
- A simple editable implementation that can be adapted to another record type
- A narrow loopback-only delivery model from the FoundRy application

Those behaviors are the generic starter. They are useful, but they are not the
full domain solution yet.

## What still needs domain customization

The incident intake workflow still needs:

- Domain labels for intake, triage, follow-up, and closure
- Record fields for incident title, reporter, category, date, summary, owner, and closure outcome
- Copy updates so the interface reads like an incident log instead of a generic task list
- Review guidance that captures observed evidence instead of assuming readiness
- A clear distinction between starter behavior and domain-specific behavior in exported notes

## Brief

Use the starter as the baseline implementation and adapt it to support a local
incident intake log for operations work.

The intended use is simple:

1. A reviewer records a new incident.
2. The record is moved through triage and follow-up.
3. The record is closed when the work is finished.
4. The list remains searchable through the starter's existing filters and persistence.

## Acceptance notes

Temporary import/export was verified through the FoundRy API against a loopback server.
The exported ZIP included `project.json`, `README.md`, `specification.md`, `evaluation.md`,
`skill-references.md`, `handoff.md`, `index.html`, `style.css`, and `app.js`, and the
imported fixture preserved its `not-run` acceptance status.

Acceptance observations remain not-run in this pilot brief.

That means:

- The adapted workflow should be checked in a browser before any readiness claim
- The starter should never be described as arbitrary application generation

## Adaptation checklist

- Replace generic record text with incident intake language
- Add the domain fields needed for each record
- Keep the existing add, complete, reopen, and filter behavior intact
- Confirm persistence still works after a reload
- Verify import/export round-trips with temporary data
- Record actual browser observations for every acceptance case
- Capture remaining gaps instead of filling them in with invented success

## Boundaries

- Keep the app local and loopback-bound
- Do not add hosted deployment steps here
- Do not claim production readiness
- Do not treat the generic starter as a finished domain implementation

## Status

This is a working brief for adaptation, not a completed implementation.
