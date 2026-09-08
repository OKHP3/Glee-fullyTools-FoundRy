# Mentoring Patterns Packet v1.0

Status: proposal
Scope: reciprocal mentoring exchange between regional FoundRys
Source base: `origin/main` at `32b89159293bba2edc0c9b308b716ab20e234b5d`
Prepared on: 2026-09-07

## Purpose

This packet defines a small, versioned exchange format for sharing one useful mentoring pattern across FoundRys without implying shared runtime, shared data, or automatic adoption.

It is designed for low-cost review, clear privacy boundaries, and explicit conflict handling.

## Packet shape

```yaml
packet_version: "1.0"
packet_id: "mentoring-patterns-v1"
source_sha: "32b89159293bba2edc0c9b308b716ab20e234b5d"
origin_foundry: "Glee-fullyTools-FoundRy"
regional_scope:
  authoring_region: "Glee-fully"
  recipient_region: "AskJamie or OverKill"
pattern_name: "Reciprocal mentoring exchange contract"
summary: "A short contract for sharing a useful practice with source provenance, regional adaptation notes, and a feedback path."
compatibility:
  requires_shared_skillz: true
  requires_shared_runtime: false
  requires_shared_database: false
  requires_public_source_access: true
privacy:
  allowed_content:
    - "synthetic examples"
    - "public-source references"
    - "owner-approved pattern descriptions"
  disallowed_content:
    - "private records"
    - "credentials"
    - "working data from ignored local stores"
    - "cross-region secrets"
regional_overrides:
  preserve_tone: true
  preserve_governance: true
  localize_examples: true
  localize_contacts: true
feedback:
  route: "documented comment thread, follow-up note, or sibling review"
  response_goal: "improve the next revision without copying private project content"
adoption_evidence:
  acceptable:
    - "one regional use case reviewed with explicit diffs from the source pattern"
    - "one sibling review that names the local override decisions"
    - "one revision that incorporates feedback without changing the source SHA"
  not_claimed:
    - "auto-sync"
    - "deployment"
    - "shared persistence"
    - "cross-repo write access"
```

## Contract

1. Keep the source SHA visible in every revision so reviewers can trace the packet back to the exact baseline.
2. Preserve regional ownership. A region may adapt examples, contact points, and tone cues, but it may not inherit private data or hidden runtime state.
3. Keep compatibility language narrow. Use the packet only when the receiving region can review public-source material and shared Skillz references.
4. Treat adoption as evidence, not as a claim. A pattern is adopted only when a reviewer can point to the local override and the resulting change.
5. Route feedback back to the authoring region with a concrete revision request, not a broad endorsement.

## Conflict rules

- If the receiving region already has a stronger local rule, the local rule wins for that region.
- If the source pattern conflicts with private-record handling, privacy wins and the private content stays out of the packet.
- If two regions use the same pattern differently, record both variants instead of forcing a merge.
- If a reviewer cannot verify the source SHA, mark the packet as unverified and do not count it as adoption evidence.

## Privacy rules

- Use only synthetic examples or public-source references in the packet.
- Redact names, IDs, tokens, and private links unless the owner has explicitly approved publication.
- Do not copy working notes from local ignored data stores into the packet.
- If a pattern is useful but context-sensitive, describe the rule and the boundary, not the underlying private case.

## Glee-fully example

Pattern name: Reciprocal mentoring exchange contract

Glee-fully source note:
- Source SHA: `32b89159293bba2edc0c9b308b716ab20e234b5d`
- Pattern focus: define a small exchange packet that helps another FoundRy review a pattern without touching the owner-local app data

Synthetic regional override:
- Glee-fully keeps the warm, clear tone
- AskJamie may prefer a more direct service-style example
- OverKill may prefer a higher-level mentoring note with stronger baseline context

Example feedback note:
- "The packet is easy to review, but the compatibility field should call out whether the sibling has public-source access only."

Example adoption evidence:
- Glee-fully publishes the packet with the source SHA and privacy limits
- AskJamie reuses the shape, replaces the example, and records the local override
- A reviewer confirms the result is useful without treating it as a shared runtime contract

## Revision notes

- v1.0: first versioned packet for reciprocal mentoring exchange
- Future revisions should keep the packet small, keep the source SHA pinned, and document only the deltas that matter for review
