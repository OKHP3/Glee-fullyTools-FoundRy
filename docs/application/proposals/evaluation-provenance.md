# Proposal: evaluation provenance contract

Status: proposal only. This document does not change the application schema,
readiness checks, canon, or evaluation rubric.

## Purpose

Attach each evaluation observation to the exact specification revision that was
tested, the environment in which it was tested, the observer and observation
time, and inspectable supporting artifacts. This makes a result easier to
reproduce and easier to invalidate without turning a user-entered report into
independent verification.

## Record shape

An evaluation record keeps the existing acceptance-case meaning and adds a
provenance envelope. The names below are proposed field names.

```yaml
evaluation_id: eval-20260907-001
project_id: project-synthetic-001
spec_revision: 4
spec_fingerprint: sha256:<hash-of-exported-specification>
case_id: acceptance-add-record
result: pass                    # not-run | pass | fail | stale
observation:
  summary: "A record appeared once with the submitted label."
  observed_at: "2026-09-07T19:20:00-05:00"
  observer:
    kind: user                   # user | independent-reviewer | automated-check
    identifier: "operator-local-01"
    basis: "direct interaction"
  environment:
    host: "local-loopback"
    service_revision: "<git-sha>"
    runtime: "Python 3.14.5; Chromium <version>"
    data_scope: synthetic
artifacts:
  - kind: exported-json
    path_or_locator: "qa/evidence/eval-20260907-001.json"
    sha256: "<artifact-hash>"
    retention: private
claim_basis: observed             # observed | user-claimed | imported
notes: "No personal data used."
```

Required for a `pass` or `fail`: `spec_revision`, a stable specification
fingerprint, `case_id`, `result`, an observation summary, an ISO 8601 time, an
observer kind, an environment description, and at least one artifact or an
explicit `artifact_status: none`. A hash is preferred for files, but a
private locator may be used when retaining the file would expose sensitive
content. `not-run` needs no observation. `stale` must identify the invalidating
event or revision.

`spec_fingerprint` covers the tested specification, including the acceptance
contract and attached Skillz reference revisions. It is not a hash of the
whole database or of a private environment. The environment should identify
the service and relevant runtime versions at the level needed to repeat the
test, without recording credentials, tokens, personal data, or machine paths.

## Evidence tiers

`claim_basis` describes what the record establishes:

| Value | Meaning | Permitted wording |
|---|---|---|
| `user-claimed` | An operator reports that the result occurred, without an independently inspectable check | “The operator reports…” |
| `observed` | A named observer directly performed the case and retained an artifact or reproducible observation | “Observed by…” |
| `automated-check` | A bounded check ran against the pinned revision and its output is retained | “The check reported…” |
| `imported` | The record came from elsewhere and has not been re-established here | “Imported report; not independently verified” |

An observer's assertion is not automatically independent. Independence means
the observer, execution path, or check is separate from the authoring claim,
with enough information for a reviewer to assess that separation. A user may
record a direct observation, but the application must not silently upgrade it
to an independent review. For example, `claim_basis: user-claimed` is still a
user report even when its observer is named; it becomes `observed` only when
the direct observation and its supporting basis are actually recorded.

## Invalidation and reset rules

1. A material change to the specification, acceptance case, constraints,
   attached reference revision, or execution contract marks linked records
   `stale`. It does not rewrite the historical observation.
2. A re-test creates a new `evaluation_id` linked to the new
   `spec_revision`; it does not edit an old result in place.
3. Import creates a new project identity and resets imported results to
   `not-run`, even when the source record says `pass`. Preserve the source
   locator and original claim as history, not as current evidence.
4. A missing, changed, unreadable, or unverifiable artifact downgrades the
   record to `stale` or `user-claimed`, as appropriate. A timestamp alone is
   not evidence that a test ran.
5. If the environment materially differs, retain the observation but mark its
   applicability to the current revision or environment as `stale` until
   re-tested.

These rules support the existing principle that saved specification changes
invalidate earlier evidence. They do not create a new readiness threshold or
certify a project.

## Privacy and synthetic data

Use synthetic inputs and temporary, loopback-only services for examples and
development checks. Do not put names, addresses, account identifiers,
conversation contents, credentials, access tokens, private URLs, or full
machine paths in a committed record. Prefer a redacted summary plus a hash of
a privately retained artifact. If an artifact cannot be safely retained, say
so explicitly and record only the minimum observation needed for review.

Synthetic data is evidence of the tested synthetic scenario only. It is not
evidence of real-user safety, production behavior, external GPT behavior, or
publication readiness.

## Valid record

```yaml
evaluation_id: eval-synthetic-001
project_id: project-synthetic-001
spec_revision: 4
spec_fingerprint: sha256:abc123
case_id: acceptance-add-record
result: pass
observation:
  summary: "Submitted 'Chai notes' appeared exactly once in the local list."
  observed_at: "2026-09-07T19:20:00-05:00"
  observer:
    kind: automated-check
    identifier: "qa-check-01"
    basis: "bounded browser assertion"
  environment:
    host: local-loopback
    service_revision: 32b8915
    runtime: "Python 3.14.5; Chromium"
    data_scope: synthetic
artifacts:
  - kind: test-output
    path_or_locator: "private QA result eval-synthetic-001"
    sha256: sha256:def456
    retention: private
claim_basis: automated-check
```

## Invalid records

```yaml
# Invalid: pass has no tested specification revision or observation.
result: pass
actual: "It worked"
```

```yaml
# Invalid: this is a user claim presented as independent verification.
spec_revision: 4
result: pass
observation:
  summary: "The owner says the external GPT worked."
  observer: {kind: independent-reviewer, identifier: owner}
claim_basis: automated-check
```

```yaml
# Invalid: private data and an unbounded machine path are included.
spec_revision: 4
result: pass
observation:
  summary: "Alex Example's account 8842 passed."
  environment: {path: "<machine-specific-private-path>/private-export.json"}
```

## Stale-evidence cases

| Situation | Record treatment | Safe summary |
|---|---|---|
| Instructions changed after revision 4 passed | Mark revision-4 record `stale`; create a revision-5 run | “Prior result no longer applies to the changed specification.” |
| Imported JSON says pass | New project has `not-run`; retain source claim as imported history | “Imported report; new project requires a fresh run.” |
| Artifact hash no longer matches | Keep history, mark artifact and result `stale` pending review | “Supporting artifact changed or cannot be verified.” |
| Same spec, different runtime or attached reference revision | Keep old observation scoped to its environment; re-test current target | “Observed in the earlier environment only.” |
| Synthetic fixture passes | Keep `claim_basis` and `data_scope: synthetic` | “Passes the synthetic case; real-data behavior is unknown.” |

## Adoption boundary

This proposal is a documentation contract for a future richer evidence record.
Until implemented, the application remains accurately described by its current
working-record fields: expected result, actual result, status, and saved project
revision. Existing readiness output must continue to mean review-ready working
record only, not independently verified behavior, PME approval, deployment, or
publication readiness.
