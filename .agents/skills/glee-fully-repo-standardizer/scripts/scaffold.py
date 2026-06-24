#!/usr/bin/env python3
"""
glee-fully-repo-standardizer — Scaffold generator for Glee-fully child repos.

Spawns the canonical folder/file structure for any Glee-fully entity
(Toolbox, Tool, or Tool-ette). Run from the root of the target child repo.

Usage:
    python3 scaffold.py --tier toolette --name "Resume Builder" --id 01a \\
        --parent "Discovered Careers" \\
        --parent-url "https://chatgpt.com/g/g-..." \\
        --chatgpt-url "https://chatgpt.com/g/g-..."

Options:
    --tier          toolbox | tool | toolette  (auto-detected if manifest exists)
    --name          Display name of this entity
    --id            Entity ID (e.g., 00, 01, 01a)
    --parent        Parent entity display name
    --parent-url    Parent entity ChatGPT URL
    --chatgpt-url   This entity's ChatGPT URL
    --tone          Tone overlay ID (auto-assigned by tier if omitted)
    --dry-run       Show what would be created without writing files
    --audit         Show missing files/folders in existing repo, do not write
    --overwrite     Overwrite existing files (default: skip existing)
    --quiet         Suppress output except errors and final summary
    --json          Output machine-readable JSON summary to stdout
"""

from __future__ import annotations

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_VERSION = "1.0.0"

TIER_DEFAULTS = {
    "toolbox":  {"tone": "BledsGLEE",      "emoji": "🧰", "tree": "🌳", "role": "Toolbox (Trunk)"},
    "tool":     {"tone": "GleeRich",        "emoji": "🪚", "tree": "🌵", "role": "Tool (Branch)"},
    "toolette": {"tone": "GleeLite",        "emoji": "🔩", "tree": "🌿", "role": "Tool-ette (Twig)"},
}

TONE_INSTRUCTIONS = {
    "BledsGLEE": (
        "TONE: BLEED-GLEE\n"
        "Mode: Maximalist joy, humor, metaphor. Every sentence pulses with enthusiasm.\n"
        "- Use Freak'n, OMG, Facts on facts when something clicks\n"
        "- Ask 'Do you love me?' or 'But are you really sure?' playfully in key flows\n"
        "- Embrace cozy honesty with lines like 'Let me think about it...'\n"
        "- Infuse Schitt's Creek, Friends, Practical Magic, Stevie Nicks references where joyful\n"
        "- Use fun sarcasm with love, but never cruelty\n"
        "Always bleed Glee."
    ),
    "GleeRich": (
        "TONE: GLEE-RICH\n"
        "Mode: Warm, balanced, efficient — structured personality.\n"
        "- Use Literally, Freak'n, or OMG that's adorable\n"
        "- Keep a 'let me think about it...' pacing when introducing options\n"
        "- Ask gently cheeky check-ins: 'Do you love this?' or 'But are you really sure?'\n"
        "Channel cozy clarity. Like a barista BFF who organizes your life with rainbow folders."
    ),
    "GleeLite": (
        "TONE: GLEE-LITE\n"
        "Mode: Light, playful, snappy. Freshly caffeinated and ready to sparkle.\n"
        "- Use Freak'n, Facts on facts, or OMG for emphasis\n"
        "- Ask 'Do you love this?' in playful completions\n"
        "- Channel Phoebe Buffay meets Stevie Nicks — whimsical and prepared\n"
        "Keep it snappy, sweet, and personal."
    ),
    "ForgeDialect.A1": (
        "TONE: FORGE-DIALECT.A1\n"
        "Mode: Precise, technical, directive. Retains warmth but privileges clarity.\n"
        "- Confident and specific in all responses\n"
        "- Warm but structured — Monica Geller energy: organized, capable, a little competitive\n"
        "- Pop culture references are subtle and professional-context appropriate\n"
        "Polished. Punched up. Ready to slay."
    ),
    "Watchkeeper.Core": (
        "TONE: WATCHKEEPER.CORE\n"
        "Mode: Compliance-focused, rule-aware, slightly formal.\n"
        "- Accuracy and rule-adherence matter most here\n"
        "- Still carries Glee-fully warmth but dials back the glitter for clarity\n"
        "- The trusted advisor who keeps you out of trouble"
    ),
}

TOOLBOX_URL = "https://chatgpt.com/g/g-68578aaa54588191b70c6aa8aa9bf228-glee-fully-personalizable-tools"


def detect_tier_from_repo_name(repo_name: str) -> str | None:
    """Guess tier from the repo directory name."""
    name = repo_name.lower()
    if re.search(r"gpt00", name):
        return "toolbox"
    if re.search(r"gpt0[1-7]-", name):
        return "tool"
    if re.search(r"gpt0[1-7][a-z]-", name):
        return "toolette"
    return None


def load_existing_manifest(root: Path) -> dict:
    """Read manifest.yaml if it exists and extract known fields."""
    manifest_path = root / "manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        content = manifest_path.read_text(encoding="utf-8")
        result = {}
        for line in content.splitlines():
            line = line.strip()
            for key, field in [
                ("display_name:", "name"),
                ("chatgpt_url:", "chatgpt_url"),
                ("type:", "type"),
                ("tone_overlay:", "tone"),
            ]:
                if line.startswith(key):
                    val = line.split(":", 1)[1].strip().strip('"').strip("'")
                    if val:
                        result[field] = val
        return result
    except Exception:
        return {}


def get_brand_json_path() -> Path:
    """Find the glee-fully-brand.json asset relative to this script."""
    script_dir = Path(__file__).parent
    brand_path = script_dir.parent / "assets" / "glee-fully-brand.json"
    return brand_path


def load_brand_json() -> dict:
    brand_path = get_brand_json_path()
    if brand_path.exists():
        try:
            return json.loads(brand_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def make_brand_json_for_repo(args, brand: dict) -> str:
    """Copy the canonical brand JSON (already has everything needed)."""
    return json.dumps(brand, indent=2, ensure_ascii=False)


def tier_label(tier: str) -> str:
    return TIER_DEFAULTS.get(tier, {}).get("role", tier)


def tier_emoji(tier: str) -> str:
    return TIER_DEFAULTS.get(tier, {}).get("emoji", "")


def tier_tree_emoji(tier: str) -> str:
    return TIER_DEFAULTS.get(tier, {}).get("tree", "")


def default_tone(tier: str) -> str:
    return TIER_DEFAULTS.get(tier, {}).get("tone", "GleeLite")


def tone_instructions(tone: str) -> str:
    return TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["GleeLite"])


def now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def placeholder(text: str) -> str:
    return f"[TODO: {text}]"


# ---------------------------------------------------------------------------
# Template builders
# ---------------------------------------------------------------------------

def build_agents_md(args) -> str:
    t = args.tier
    name = args.name
    entity_id = args.id or placeholder("entity ID e.g. 01a")
    parent = args.parent or placeholder("parent entity name")
    parent_url = args.parent_url or placeholder("parent ChatGPT URL")
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    tone = args.tone

    parent_section = ""
    if t == "toolette":
        parent_section = (
            f"  └─ [{parent}]({parent_url})  ← Parent Tool (Branch)\n"
            f"       └─ **{name}**  ◀ THIS REPO (Tool-ette)\n"
        )
    elif t == "tool":
        parent_section = (
            f"  └─ **{name}**  ◀ THIS REPO (Tool / Branch)\n"
            f"       └─ [Tool-ettes listed in inventory]\n"
        )
    else:
        parent_section = f"  └─ **{name}**  ◀ THIS REPO (Toolbox / Trunk)\n"

    return f"""# AGENTS.md — {name}

> **For AI agents, assistants, and LLM tools navigating this repository.**
> Read this file first. It tells you what this repo is, what it contains,
> what you are and are not allowed to do here, and where to find everything.

---

## What This Repository Is

This is the governed source repository for **{name}** — a
{tier_label(t)} within the Glee-fully Personalizable Tools™ ecosystem.

**ChatGPT Link:** {chatgpt_url}

This is NOT a web application. Do not configure web server workflows,
deployment targets, or live-site infrastructure for this repository.

---

## Authority Chain

```
OKHP3/OverKill-Hill  (root governance)
  └─ OKHP3/Glee-fullyTools-FoundRy  (FoundRy — source of all governance)
{parent_section}```

Parent FoundRy governance applies here. When in conflict, defer to the root.

---

## Entity Identity

| Field | Value |
|-------|-------|
| **Entity ID** | {entity_id} |
| **Tier** | {tier_label(t)} |
| **Tone Overlay** | {tone} |
| **Parent** | {parent} |
| **Parent URL** | {parent_url} |
| **Toolbox** | [Glee-fully Personalizable Tools]({TOOLBOX_URL}) |
| **ChatGPT** | {chatgpt_url} |

---

## Directory Map

| Path | Contents |
|------|----------|
| `gpt/instructions.md` | Active GPT instruction payload — the core deliverable |
| `gpt/description.md` | 300-char GPT Builder description |
| `gpt/starters.md` | 4 conversation starters |
| `gpt/knowledge/` | Knowledge files attached to the GPT |
| `pulsebook/` | PulseBook evaluation — required before 1.0 |
| `docs/` | Human-readable documentation |
| `canon/registry-entry.md` | !CLAUSE declaration for this entity |
| `origin/` | Read-only source migration content (ChatGPT exports, Notion) |
| `assets/glee-fully-brand.json` | Canonical brand/tone/persona payload |
| `archive/` | Retired or superseded content |

---

## Governance Rules You Must Follow

### 1. Expansion-Only Discipline
Never delete, simplify, or reduce existing content in any canonical file.
All edits add detail, specificity, or capability. Existing clauses are never removed.

### 2. CanonSeal Integrity
If a file has a `::CanonSeal[...]::` tag, it is locked for growth only.
Do not remove or alter the tag. Any edit must preserve all prior content.

### 3. Canon Authority Hierarchy
```
OKHP3/Glee-fullyTools-FoundRy/canon/ > governance/ > GPT-local logic
```

### 4. No Prompt-Local Memory
Runtime state must not be stored in GPT-local logic or prompt context.
All continuity uses `canon/dataledger_hydration_v3.md` in the FoundRy.

### 5. Tone Default
This entity uses **{tone}**. Threads without an explicit overlay default to
`GleeTone.A1` (uplifting, whimsical, clear). Log deviations with `!DRIFT_EVENT`.

### 6. origin/ Is Read-Only
Files in `origin/chatgpt-exports/` and `origin/notion-exports/` are source
migration content. Never edit them — copy content out to `gpt/` or `docs/`
for refinement.

### 7. 1.0 Gate
This repo is not 1.0 until:
- `gpt/instructions.md` is finalized and deployed
- `pulsebook/pulsebook-v1-7.md` is filled and passes
- `manifest.yaml` has `pme_ready: true`

---

## Brand Rules (All Generated Content)

| Rule | Detail |
|------|--------|
| **No em dashes** | Do not use em dashes in any generated content |
| **Preserve punchy lines** | Standalone short lines must not be consolidated into paragraphs |
| **ROY principle** | Verbosity must earn its space — clarity over comprehensiveness |
| **Tone default** | {tone} unless explicitly overridden |

---

## Quick Reference

| I need to... | Go to |
|-------------|-------|
| See the active GPT instructions | `gpt/instructions.md` |
| Find this entity's canonical ID | `canon/registry-entry.md` |
| Check what tone rules apply | `assets/glee-fully-brand.json` or `docs/overview.md` |
| Add migrated ChatGPT content | `origin/chatgpt-exports/` |
| Add migrated Notion content | `origin/notion-exports/` |
| Evaluate quality before 1.0 | `pulsebook/pulsebook-v1-7.md` |
| Understand the full ecosystem | [Glee-fullyTools-FoundRy README](https://github.com/OKHP3/Glee-fullyTools-FoundRy) |
"""


def build_readme(args) -> str:
    t = args.tier
    name = args.name
    entity_id = args.id or placeholder("entity ID")
    parent = args.parent or placeholder("parent entity name")
    parent_url = args.parent_url or placeholder("parent ChatGPT URL")
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    tone = args.tone
    e = tier_emoji(t)
    tree = tier_tree_emoji(t)

    parent_chain = f"- **Toolbox:** [Glee-fully Personalizable Tools]({TOOLBOX_URL})\n"
    if t == "toolette":
        parent_chain += f"- **Tool (Branch):** [{parent}]({parent_url})\n"
        parent_chain += f"- **Tool-ette (Twig):** {name} ← you are here\n"
    elif t == "tool":
        parent_chain += f"- **Tool (Branch):** {name} ← you are here\n"
    else:
        parent_chain += f"- **Toolbox (Trunk):** {name} ← you are here\n"

    return f"""# {e} {name}

> {tier_label(t)} in the Glee-fully Personalizable Tools™ ecosystem.

[Open in ChatGPT →]({chatgpt_url})

---

## What This {tier_label(t).split(" ")[0]} Does

{placeholder("Plain-language description — what does this entity help users accomplish?")}

---

## Primary Functions

{placeholder("List the key functions/capabilities this entity delivers.")}

Example format:
- **Function Name** — what it does and why it matters
- **Function Name** — what it does and why it matters

---

## Parent Chain

{parent_chain}
---

## Tone

This entity uses the **{tone}** tone overlay.

{placeholder("One sentence describing the emotional character of this entity's voice.")}

---

## Entity Metadata

| Field | Value |
|-------|-------|
| Entity ID | {entity_id} |
| Tier | {tier_label(t)} |
| Tone Overlay | {tone} |
| Lifecycle Status | draft |
| PME Ready | false |
| ChatGPT URL | {chatgpt_url} |

---

## Repository Structure

```
gpt/instructions.md     ← Active GPT instruction payload
gpt/description.md      ← GPT Builder description (300 chars)
gpt/starters.md         ← Conversation starters
pulsebook/              ← Quality evaluation
docs/                   ← Documentation
canon/                  ← Canon compliance
origin/                 ← Migrated source content
assets/                 ← Brand payload + icon
```

---

> *The capability is durable. The platform wrapper is temporary.*
"""


def build_manifest(args) -> str:
    t = args.tier
    name = args.name
    entity_id = args.id or placeholder("entity ID")
    parent = args.parent or placeholder("parent entity name")
    parent_url = args.parent_url or placeholder("parent ChatGPT URL")
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    tone = args.tone
    repo_name = Path.cwd().name

    type_map = {"toolbox": "toolbox", "tool": "tool", "toolette": "toolette"}
    entity_type = type_map.get(t, "toolette")

    return f"""schema_version: "2.0"

repo:
  name: {repo_name}
  display_name: "{name}"
  type: {entity_type}
  lifecycle_status: draft
  visibility: private
  pme_ready: false
  chatgpt_url: "{chatgpt_url}"

brand:
  domain: gleefully
  display_name: "Glee-fully Personalizable Tools™"
  public_site: https://glee-fully.tools
  tone_overlay: {tone}
  tier: {t}

authority_chain:
  parent_foundry: OKHP3/Glee-fullyTools-FoundRy
  parent_toolbox: glee-fully-gpt00-personalizable-tools
  toolbox_url: "{TOOLBOX_URL}"
  parent_tool: "{parent}"
  parent_tool_url: "{parent_url}"

entity:
  id: "{entity_id}"
  name: "{name}"
  type: {entity_type}
  parent_name: "{parent}"
  parent_url: "{parent_url}"

governance:
  directive_version: "3.0.1"
  expansion_discipline: growth-only
  pme_ready: false
  canon_seal: ""

author: Jamie Hill
organization: OverKill Hill P³ (OKHP3)
contact: contact@glee-fully.tools
"""


def build_changelog() -> str:
    return f"""# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Planned
- Populate `gpt/instructions.md` with finalized instruction payload
- Fill `pulsebook/pulsebook-v1-7.md` evaluation
- Set `manifest.yaml` `pme_ready: true` when 1.0 is reached

---

## [0.1.0] — {now_str()}

### Added
- Initial repository scaffold via `glee-fully-repo-standardizer`
- Canonical folder structure: `gpt/`, `pulsebook/`, `docs/`, `canon/`, `origin/`, `assets/`, `archive/`
- `assets/glee-fully-brand.json` — shared brand/tone/persona payload
"""


def build_license() -> str:
    return """# License

Copyright © 2024–2026 Jamie Hill / OverKill Hill P³ (OKHP3)
All rights reserved.

This repository and all its contents are proprietary.
No part of this repository may be reproduced, distributed, or used
in derivative works without explicit written permission from the author.

Contact: contact@glee-fully.tools
"""


def build_gpt_instructions(args) -> str:
    t = args.tier
    name = args.name
    tone = args.tone
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    parent = args.parent or placeholder("parent entity name")
    tone_block = tone_instructions(tone)

    if t == "toolbox":
        role_block = (
            f"You are the **heart of the Glee-fully Personalizable Tools suite** — "
            f"the Toolbox (Trunk). Your role is to **guide users** through the suite's "
            f"Tools and Tool-ettes, making it easy to find the right GPT for any task."
        )
        behavior = (
            "- Introduce the Glee-fully structure and the trunk-branch-twig-leaf metaphor\n"
            "- Link to all 7 Tools (Branches) and help users choose the right Tool-ette\n"
            "- Do NOT execute tasks directly — route users to the appropriate Tool or Tool-ette\n"
            "- Visit-aware dialog: greet first-timers differently than returning users"
        )
    elif t == "tool":
        role_block = (
            f"You are **{name}**, the {tier_label(t)} in the Glee-fully Personalizable "
            f"Tools suite. Your role is to route users to the correct Tool-ette for their "
            f"specific need within your category."
        )
        behavior = (
            f"- Introduce the Tool-ettes available in {name}\n"
            "- Help users identify which Tool-ette fits their current need\n"
            "- Do NOT perform the task yourself — route to the appropriate Tool-ette\n"
            "- You may do light logic if no subtool fits (edge cases only)"
        )
    else:
        role_block = (
            f"You are **{name}**, a {tier_label(t)} in the Glee-fully Personalizable "
            f"Tools suite. Your role is to execute a specific, focused task with joy "
            f"and precision.\n\n"
            f"Parent Tool: {parent}"
        )
        behavior = (
            f"- {placeholder('Primary capability 1 — what does this Tool-ette do first?')}\n"
            f"- {placeholder('Primary capability 2')}\n"
            f"- {placeholder('Primary capability 3')}\n"
            "- Do NOT route users to other GPTs — stay focused on your specific task\n"
            "- Export, summarize, or confirm outputs clearly at the end of each flow"
        )

    return f"""# GPT Instructions — {name}
# Tone Overlay: {tone}
# Tier: {tier_label(t)}
# ChatGPT: {chatgpt_url}
#
# IMPORTANT: This file becomes the instruction payload in ChatGPT Builder.
# Target: ~6,000–8,000 characters. Trim if needed.
# Do not include comment lines (starting with #) in the final Builder payload.
# ---------------------------------------------------------------------------

## Role and Identity

{role_block}

You are part of the **Glee-fully Personalizable Tools™** suite — designed to
sparkle, sort, and slay life's chaos. Inspired by Glee herself: a Pacific
Northwest original who color-codes everything and drinks chai like it's a love
language.

---

## Tone

{tone_block}

---

## Core Behavior

{behavior}

---

## Glee-isms (Use Throughout)

Use these phrases naturally at key moments — completions, check-ins, thinking:

- "Freak'n facts on facts."
- "OMG stop — this is so Glee-coded."
- "Hold up, doing a sparkle sort..."
- "Give me one sec — lighting a cinnamon candle and thinking this through..."
- "Do you love this? Wait. No. REALLY love it?"
- "Polished. Punched up. Ready to slay."
- "Literally the cutest."

Pop culture touchstones (use sparingly and naturally):
Schitt's Creek, Friends, Practical Magic, Stevie Nicks, Hocus Pocus, The Crow.

---

## {placeholder("Section: Primary Task Flow")}

{placeholder("Describe the step-by-step flow this GPT walks the user through.")}

Step 0 — Welcome and orient
Step 1 — Gather input
Step 2 — Process / generate
Step 3 — Review and refine
Step 4 — Export or confirm

---

## Output Behavior

- Responses should be warm, clear, and appropriately sized — not padded
- Use bullet points and headers for structured content
- At task completion, celebrate the output with a Glee-ism
- Ask a check-in question before finalizing: "Do you love this? REALLY love it?"

---

## Boundaries

- Stay focused on your specific task — do not attempt to cover other Tool-ettes' scope
- Do not store user data between sessions
- If a user asks for something outside your scope, route them to the Toolbox:
  {TOOLBOX_URL}

---

## Suite Context

This GPT is part of Glee-fully Personalizable Tools™.
Public site: https://glee-fully.tools
Ecosystem map: https://glee-fully.tools/ecosystem/

{placeholder("Add any additional context, knowledge file references, or special instructions.")}
"""


def build_gpt_description(args) -> str:
    name = args.name
    return f"""{name} — {placeholder("One punchy sentence describing what this GPT does. 300 characters MAX including this entity name. Count carefully.")}

[TODO: Remove this line and ensure total character count is under 300]
"""


def build_gpt_starters(args) -> str:
    name = args.name
    return f"""# Conversation Starters — {name}
# Add exactly 4 starters to GPT Builder.
# Each should be a natural user request that triggers the core flow.

1. {placeholder("Starter 1 — a common user request that opens the primary flow")}
2. {placeholder("Starter 2 — a second common entry point")}
3. {placeholder("Starter 3 — a task-specific prompt")}
4. {placeholder("Starter 4 — a discovery or help prompt")}
"""


def build_docs_overview(args) -> str:
    t = args.tier
    name = args.name
    tone = args.tone
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    parent = args.parent or placeholder("parent entity name")

    return f"""# Overview — {name}

> {tier_label(t)} in the Glee-fully Personalizable Tools™ ecosystem.
> Tone: {tone}

[Open in ChatGPT →]({chatgpt_url})

---

## What {name} Is

{placeholder("Plain-language description of this entity's purpose and who it's for.")}

{placeholder("Second paragraph — the emotional value proposition. Why does this feel good to use?")}

---

## Who Uses This

{placeholder("Describe the primary user and their context. Example: 'Job seekers preparing to apply for a specific role who already have a base resume.'")}

---

## What It Does

{placeholder("List the 3-7 key things this entity helps users accomplish.")}

---

## How It Works

{placeholder("Brief description of the interaction flow. What does a typical session look like?")}

1. User {placeholder("opens / starts with")}
2. {name} {placeholder("responds with / asks for")}
3. User {placeholder("provides")}
4. Output: {placeholder("what the user gets at the end")}

---

## Tone and Personality

This entity uses the **{tone}** tone overlay.

{placeholder("One paragraph describing how this entity sounds. What's its emotional character?")}

---

## Parent Chain

- Toolbox: [Glee-fully Personalizable Tools]({TOOLBOX_URL})
- Tool: [{parent}]({args.parent_url or placeholder("parent URL")})
- This entity: {name}

---

## Related Tool-ettes

{placeholder("List 1-3 sibling Tool-ettes that complement this one. Link to their ChatGPT URLs.")}
"""


def build_docs_functions(args) -> str:
    name = args.name
    return f"""# Functions — {name}

> All capabilities and sub-functions this entity provides.

---

## Primary Functions

{placeholder("List every function this entity delivers. Use the format below.")}

### {placeholder("Function Name")}

**Trigger:** {placeholder("What user action or input activates this function?")}
**Output:** {placeholder("What does the user get?")}
**Notes:** {placeholder("Any important caveats or edge cases.")}

---

### {placeholder("Function Name")}

**Trigger:** {placeholder("What user action or input activates this function?")}
**Output:** {placeholder("What does the user get?")}
**Notes:** {placeholder("Any important caveats or edge cases.")}

---

### {placeholder("Function Name")}

**Trigger:** {placeholder("What user action or input activates this function?")}
**Output:** {placeholder("What does the user get?")}
**Notes:** {placeholder("Any important caveats or edge cases.")}

---

## Easter Eggs and Alternate Commands

{placeholder("Optional: list any hidden triggers or playful alternate commands.")}

- Type "BLEED GLEE MODE" to activate maximum sparkle tone
- Type "calm mode" or "keep it pro" to dial back the Glee-isms
- Type "I need a Glee-spiration" for extra encouragement

---

## Out of Scope

{placeholder("List things users might try that this entity does NOT handle — and where to route them.")}
"""


def build_canon_registry_entry(args) -> str:
    t = args.tier
    name = args.name
    entity_id = args.id or placeholder("entity ID")
    chatgpt_url = args.chatgpt_url or placeholder("ChatGPT URL")
    tone = args.tone
    tier_map = {"toolbox": "Toolbox", "tool": "Tool", "toolette": "Toolette"}
    entity_type = tier_map.get(t, "Toolette")

    return f"""# Canon Registry Entry — {name}

> This file declares {name} in the Glee-fully canon system.
> It is the entity's !CLAUSE block for `canon/dataledger_registry_v3.md`.
> Copy the YAML block below into the FoundRy registry when this entity reaches 1.0.

---

## !CLAUSE Declaration

```yaml
!CLAUSE: !PME_READY
ID: {entity_type}.{name.replace(" ", "")}.1.0.0
Summary: {placeholder("One-line description of what this entity does")}
TargetPhase: Gleam
DeclaredBy: Glee-fully FoundRy
EntityID: "{entity_id}"
ChatGPTURL: "{chatgpt_url}"
ToneOverlay: {tone}
Tier: {t}
LifecycleStatus: draft
CanonSeal: ""
```

---

## Metadata

| Field | Value |
|-------|-------|
| Entity ID | {entity_id} |
| Entity Type | {entity_type} |
| Display Name | {name} |
| Tone Overlay | {tone} |
| ChatGPT URL | {chatgpt_url} |
| Lifecycle Status | draft |
| PME Ready | false |
| CanonSeal | {placeholder("Add ::CanonSeal[...]::: after PulseBook passes")} |

---

## Registration Checklist

Before copying this declaration to the FoundRy registry:

- [ ] `gpt/instructions.md` is finalized and deployed to ChatGPT Builder
- [ ] `gpt/description.md` is populated (300 chars max)
- [ ] `gpt/starters.md` has 4 starters
- [ ] `pulsebook/pulsebook-v1-7.md` is filled and passes all checks
- [ ] `manifest.yaml` has `lifecycle_status: active` and `pme_ready: true`
- [ ] CanonSeal tag has been assigned and added above
- [ ] Entry has been added to `canon/dataledger_registry_v3.md` in the FoundRy
"""


def build_pulsebook_stub(args) -> str:
    name = args.name
    return f"""# GPT Pulsebook — {name}

> **Version:** v1.7
> **Status:** DRAFT — fill this out at PROMPT05 before marking 1.0
>
> Reference: `OKHP3/Glee-fullyTools-FoundRy/evaluation/gpt-pulsebook-evaluation-v1-7.md`
> Run the full PulseBook evaluation prompt from that file against this GPT,
> then paste the output here.

---

pulsebook_schema: v1.7
pulse_id: {placeholder("unique identifier for this GPT")}
gpt_id: {placeholder("ChatGPT GPT ID from the URL")}
ecosystem: gleefully
entity_name: "{name}"
tier: {args.tier}
tone_overlay: {args.tone}
evaluation_date: {placeholder("YYYY-MM-DD")}
evaluator: {placeholder("your name or 'FoundRy Agent'")}
lifecycle_status: draft
pme_ready: false

---

## Evaluation Results

{placeholder("Paste the full PulseBook v1.7 output here after running the evaluation.")}

---

## Sign-Off

- [ ] Identity and scope verified
- [ ] Tone calibration verified
- [ ] Function coverage complete
- [ ] Instruction quality passes
- [ ] Canon compliance confirmed
- [ ] PME-ready status: APPROVED / REJECTED

**Reviewer:** {placeholder("name")}
**Date:** {placeholder("YYYY-MM-DD")}
"""


# ---------------------------------------------------------------------------
# File manifest by tier
# ---------------------------------------------------------------------------

def get_file_manifest(tier: str, args) -> list[tuple[str, str]]:
    """Returns list of (relative_path, content) tuples."""
    files = [
        ("AGENTS.md",                   build_agents_md(args)),
        ("README.md",                   build_readme(args)),
        ("CHANGELOG.md",                build_changelog()),
        ("LICENSE.md",                  build_license()),
        ("manifest.yaml",               build_manifest(args)),
        ("gpt/instructions.md",         build_gpt_instructions(args)),
        ("gpt/description.md",          build_gpt_description(args)),
        ("gpt/starters.md",             build_gpt_starters(args)),
        ("gpt/knowledge/.gitkeep",      ""),
        ("pulsebook/pulsebook-v1-7.md", build_pulsebook_stub(args)),
        ("docs/overview.md",            build_docs_overview(args)),
        ("docs/functions.md",           build_docs_functions(args)),
        ("canon/registry-entry.md",     build_canon_registry_entry(args)),
        ("origin/chatgpt-exports/.gitkeep", ""),
        ("origin/notion-exports/.gitkeep",  ""),
        ("archive/.gitkeep",            ""),
    ]

    brand_json = make_brand_json_for_repo(args, load_brand_json())
    files.append(("assets/glee-fully-brand.json", brand_json))

    if tier in ("tool", "toolbox"):
        files = [f for f in files if not f[0].startswith("gpt/knowledge")]

    return files


def get_dir_manifest(tier: str) -> list[str]:
    dirs = [
        "gpt",
        "pulsebook",
        "docs",
        "canon",
        "origin/chatgpt-exports",
        "origin/notion-exports",
        "assets",
        "archive",
    ]
    if tier not in ("tool", "toolbox"):
        dirs.append("gpt/knowledge")
    return dirs


# ---------------------------------------------------------------------------
# Audit mode
# ---------------------------------------------------------------------------

def run_audit(root: Path, tier: str | None) -> None:
    """Show which canonical files/folders are missing."""
    print(f"\nglee-fully-repo-standardizer v{SCRIPT_VERSION} [audit]")
    print(f"Root: {root}\n")

    if not tier:
        tier = detect_tier_from_repo_name(root.name) or "toolette"
        print(f"Tier auto-detected: {tier}\n")

    class FakeArgs:
        pass
    a = FakeArgs()
    a.tier = tier
    a.name = root.name
    a.id = ""
    a.parent = ""
    a.parent_url = ""
    a.chatgpt_url = ""
    a.tone = default_tone(tier)

    files = get_file_manifest(tier, a)
    dirs = get_dir_manifest(tier)

    missing_dirs = [d for d in dirs if not (root / d).is_dir()]
    missing_files = [f for f, _ in files if not (root / f).exists()]

    if not missing_dirs and not missing_files:
        print("All canonical folders and files are present.")
        return

    if missing_dirs:
        print("Missing folders:")
        for d in missing_dirs:
            print(f"  {d}/")
    if missing_files:
        print("\nMissing files:")
        for f in missing_files:
            print(f"  {f}")

    print(f"\nRun scaffold.py --tier {tier} --name ... to create missing structure.")


# ---------------------------------------------------------------------------
# Main scaffold
# ---------------------------------------------------------------------------

def run_scaffold(root: Path, args, dry_run: bool, overwrite: bool, quiet: bool, as_json: bool) -> None:
    created_dirs = []
    written_files = []
    skipped_files = []
    overwritten_files = []

    if not quiet and not as_json:
        print(f"\nglee-fully-repo-standardizer v{SCRIPT_VERSION} [{args.tier}] · {args.name}")
        print(f"Root: {root}")
        print(f"Tone: {args.tone}")
        print()

    dirs = get_dir_manifest(args.tier)
    for d in dirs:
        dir_path = root / d
        if not dir_path.exists():
            if not dry_run:
                dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(d)

    files = get_file_manifest(args.tier, args)
    for rel_path, content in files:
        full_path = root / rel_path
        if full_path.exists() and not overwrite:
            skipped_files.append(rel_path)
            continue
        if full_path.exists() and overwrite:
            overwritten_files.append(rel_path)
        if not dry_run:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
        written_files.append(rel_path)

    if dry_run:
        todo_files = [f for f, content in files if "[TODO" in content]
    else:
        todo_files = [f for f in written_files if (root / f).exists() and "[TODO" in (root / f).read_text(encoding="utf-8")]

    if as_json:
        result = {
            "version": SCRIPT_VERSION,
            "tier": args.tier,
            "name": args.name,
            "tone": args.tone,
            "dry_run": dry_run,
            "created_dirs": created_dirs,
            "written_files": written_files,
            "skipped_files": skipped_files,
            "overwritten_files": overwritten_files,
            "todo_files": todo_files,
        }
        print(json.dumps(result, indent=2))
        return

    if not quiet:
        if dry_run:
            print("DRY RUN — no files written\n")

        if created_dirs:
            print(f"Folders ({len(created_dirs)}):")
            for d in created_dirs:
                marker = "  (would create)" if dry_run else "  created"
                print(f"  {d}/{marker}")
            print()

        if written_files:
            print(f"Files written ({len(written_files)}):")
            for f in written_files:
                marker = "  (would write)" if dry_run else ("  overwritten" if f in overwritten_files else "  written")
                print(f"  {f}{marker}")
            print()

        if skipped_files:
            print(f"Files skipped — already exist ({len(skipped_files)}):")
            for f in skipped_files:
                print(f"  {f}")
            print()

    print(f"\n{'DRY RUN COMPLETE' if dry_run else 'SCAFFOLD COMPLETE'}")
    print(f"  Tier:       {tier_label(args.tier)}")
    print(f"  Entity:     {args.name}")
    print(f"  Tone:       {args.tone}")
    print(f"  Dirs:       {len(created_dirs)} created")
    print(f"  Files:      {len(written_files)} written, {len(skipped_files)} skipped")

    if todo_files:
        print(f"\n  {len(todo_files)} files need [TODO] items filled:")
        for f in todo_files[:8]:
            print(f"    {f}")
        if len(todo_files) > 8:
            print(f"    ... and {len(todo_files) - 8} more")

    print("\n  Recommended fill order:")
    print("    1. gpt/instructions.md  ← most important")
    print("    2. gpt/description.md")
    print("    3. gpt/starters.md")
    print("    4. docs/overview.md")
    print("    5. docs/functions.md")
    print("    6. canon/registry-entry.md")
    print("    7. pulsebook/pulsebook-v1-7.md  ← gates 1.0")
    print("    8. manifest.yaml  ← set pme_ready: true when done\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a canonical Glee-fully child repo structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--tier", choices=["toolbox", "tool", "toolette"],
                        help="Entity tier (auto-detected from manifest or repo name if omitted)")
    parser.add_argument("--name", help="Display name of this entity")
    parser.add_argument("--id", help="Entity ID (e.g., 01a)")
    parser.add_argument("--parent", help="Parent entity display name")
    parser.add_argument("--parent-url", dest="parent_url", default="", help="Parent ChatGPT URL")
    parser.add_argument("--chatgpt-url", dest="chatgpt_url", default="", help="This entity's ChatGPT URL")
    parser.add_argument("--tone", help="Tone overlay ID (default: tier default)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--audit", action="store_true", help="Show missing structure, do not write")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON output")

    args = parser.parse_args()
    root = Path.cwd()

    if args.audit:
        run_audit(root, args.tier)
        return

    existing = load_existing_manifest(root)

    if not args.tier:
        detected = detect_tier_from_repo_name(root.name)
        manifest_type = existing.get("type", "")
        type_map = {"toolbox": "toolbox", "tool": "tool", "toolette": "toolette"}
        args.tier = type_map.get(manifest_type) or detected or "toolette"
        if not args.quiet and not args.as_json:
            print(f"Tier auto-detected: {args.tier}")

    if not args.name:
        args.name = existing.get("name") or root.name.replace("-", " ").title()

    if not args.chatgpt_url:
        args.chatgpt_url = existing.get("chatgpt_url", "")

    if not args.tone:
        args.tone = existing.get("tone") or default_tone(args.tier)

    if not args.parent:
        args.parent = ""

    run_scaffold(root, args, dry_run=args.dry_run, overwrite=args.overwrite,
                 quiet=args.quiet, as_json=args.as_json)


if __name__ == "__main__":
    main()
