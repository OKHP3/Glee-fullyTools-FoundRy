---
name: Glee-fully child repo standard
description: Canonical folder/file structure for all 50 Glee-fully child repos, tier differences, fill order, and 1.0 gate.
---

# Glee-fully Child Repo Standard

## Structure (Tool-ette — 9 dirs, 17 files)

```
AGENTS.md                    ← AI agent navigation guide
README.md                    ← Entity overview
CHANGELOG.md                 ← Version history
LICENSE.md                   ← Proprietary license
manifest.yaml                ← Repo metadata + Glee-fully fields

gpt/
  instructions.md            ← Active GPT instruction payload (most important file)
  description.md             ← 300-char GPT Builder description
  starters.md                ← 4 conversation starters
  knowledge/.gitkeep         ← Knowledge files (toolette only)

pulsebook/
  pulsebook-v1-7.md          ← PulseBook evaluation (gates 1.0)

docs/
  overview.md                ← Plain-language summary
  functions.md               ← All functions documented

canon/
  registry-entry.md          ← !CLAUSE declaration

origin/
  chatgpt-exports/.gitkeep   ← Read-only migration source
  notion-exports/.gitkeep    ← Read-only migration source

assets/
  glee-fully-brand.json      ← Shared brand/tone/persona payload
  icon.png                   ← Add manually

archive/.gitkeep
```

Tool and Toolbox tiers: same structure minus gpt/knowledge/.

## Fill Order (after scaffold)

1. gpt/instructions.md — most important, paste + refine instruction payload
2. gpt/description.md — 300 chars max
3. gpt/starters.md — 4 starters
4. docs/overview.md
5. docs/functions.md
6. canon/registry-entry.md — fill !CLAUSE block
7. pulsebook/pulsebook-v1-7.md — run evaluation
8. manifest.yaml — set lifecycle_status: active, pme_ready: true

## 1.0 Gate

A repo is NOT 1.0 until:
- gpt/instructions.md finalized and deployed to ChatGPT Builder
- gpt/description.md populated
- gpt/starters.md has 4 starters
- pulsebook filled and passes
- canon/registry-entry.md has valid !PME_READY !CLAUSE block
- manifest.yaml: lifecycle_status: active, pme_ready: true

## Tone Defaults by Tier

- toolbox → BledsGLEE
- tool → GleeRich
- toolette → GleeLite
- Exceptions: Tool 01 (Discovered Careers) uses ForgeDialect.A1
