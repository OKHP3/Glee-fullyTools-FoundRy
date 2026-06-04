---
name: Glee-fully FoundRy Structure
description: Key decisions about what this repo is, what it is not, and how it is organized.
---

## What This Repo Is

Private workbench (NOT a web app). Do not configure web server workflows or deployment targets.
The `web-templates/` folder holds webpage template source assets for child repos only.

## Why

The repo was imported with a webpage template folder (`webpage-build`) that was loaded in error.
A web server workflow was set up on import — this is wrong and was removed.
`replit.md` documents this preference explicitly.

## Structure (after reorganization)

Root: README.md, AGENTS.md, CHANGELOG.md, LICENSE.md, manifest.yaml, replit.md, .gitignore

Key folders and their role:
- `canon/` — The 9 canonical dataLedger files (authoritative source of truth)
- `governance/` — Project directives + operator's cathedral layout
- `docs/` — Human-readable overviews (narrative, technical)
- `prompts/` — Builder PromptChain v2.0 + scaffolds
- `vernacular/` — Voice/tone reference library
- `templates/` — FrankenTemplate GPT instruction variants (23 files, letter-versioned)
- `evaluation/` — GPT PulseBook rubrics (use v1.7 as current)
- `inventory/` — Entity catalog (companion to canon/dataLedger_registry_v3.md)
- `web-templates/` — Webpage template assets for child repos only
- `snapshots/` — Dated historical state captures (2025-09-08, 2025-09-14)

## Canon Rule

All 9 dataLedger files must live in `canon/` at repo root.
Governance directive: `GleeCoreDirective.v3.0.1.locked`
Four ledger stubs created (narrative, ideation, archive, processing) — populate as ecosystem grows.

## How to Apply

Any future AI agent or import should check replit.md first for workbench context.
AGENTS.md is the comprehensive navigation guide — read it before making any changes.
