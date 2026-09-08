# Proposal: restorable project revisions

Status: proposed, not implemented
Task: F15
Scope: the owner-local FoundRy application under `app/`

## Source boundary

The current application stores one complete project JSON document in the
`projects` table:

```sql
projects(id TEXT PRIMARY KEY, revision INTEGER NOT NULL, data TEXT NOT NULL)
```

It stores only revision metadata in `history`:

```sql
history(project_id TEXT NOT NULL, revision INTEGER NOT NULL, at TEXT NOT NULL,
        action TEXT NOT NULL, summary TEXT NOT NULL,
        PRIMARY KEY(project_id, revision))
```

`Store.create` writes revision 1 to both tables. `Store.update` checks the
caller's current revision, increments it, replaces the current JSON, and adds a
metadata row. Material specification, attached-skill, or acceptance-contract
changes clear recorded test evidence. Archive and restore are currently status
changes made through the same update path. The existing history endpoint cannot
reconstruct an earlier project because no earlier JSON is stored.

This proposal designs the smallest viable extension. It does not implement a
database migration, endpoint, UI change, backup command, or runtime behavior.

## Decisions

### 1. Store one immutable snapshot per committed revision

Add a table owned by the same SQLite database:

```sql
project_revisions(
  project_id TEXT NOT NULL,
  revision INTEGER NOT NULL,
  captured_at TEXT NOT NULL,
  action TEXT NOT NULL,
  schema_version INTEGER NOT NULL,
  data TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  PRIMARY KEY(project_id, revision),
  FOREIGN KEY(project_id) REFERENCES projects(id)
)
```

`data` is the complete validated project JSON at that revision, including its
project ID, revision, status, timestamps, components, acceptance cases and
attached skill IDs. `sha256` is the SHA-256 digest of the exact UTF-8 JSON
bytes stored in `data`, using one deterministic serializer. The digest is an
integrity check, not a security boundary or a substitute for access control.

Every successful create and update writes exactly one snapshot. The existing
`history` row remains the compact activity index and remains useful for the
existing history view. The snapshot row is the source for restore. Do not store
only field diffs: a full document makes restore deterministic, keeps the first
implementation small, and preserves fields that are not currently displayed.

The application continues to treat `projects` as the current-state read model.
The snapshot table is append-only. No update or delete operation is part of this
contract. SQLite foreign-key enforcement should be enabled before relying on the
foreign key, and project deletion is outside this proposal.

### 2. Restore always creates a new revision on the same project

Proposed operation:

```text
POST /api/projects/{projectId}/restore
{
  "sourceRevision": 3,
  "currentRevision": 7
}
```

The server must require the caller's current revision, as PUT does today. It
must read and digest-check the source snapshot before changing anything. It
then copies the source document into the current project under revision 8,
retaining the current project ID and original `createdAt`, and setting a new
`updatedAt`. The saved document's `revision` becomes 8. The source revision 3
remains unchanged and available for another restore.

The restore response is the complete current project at revision 8. A history
row records `action = "restored"` and identifies the source revision. The new
revision also receives a snapshot. There is no in-place replacement, revision
reuse, branch, merge, or deletion of the intervening revisions.

A restore is not an import. Import creates a new identity and resets evidence;
restore keeps the identity and its project lineage.

### 3. Restored evaluation evidence is invalidated

Restore must clear every restored test case's `actual` value and set its
`status` to `not-run`, even when the selected snapshot appears identical to the
current document. The restored specification is now being treated as a new
revision, and the old observation does not prove this newly committed revision
in a particular environment. The pre-restore evidence remains readable only
inside its immutable source snapshot.

The restore summary should state that evaluation evidence was reset. Readiness
must therefore fail until the owner records fresh observed evidence. This keeps
the existing rule that a passing result requires actual evidence and avoids a
silent claim that old testing transferred across a restore.

The snapshot captured for the new revision contains the cleared evidence, not
the source snapshot's stale pass results.

### 4. Archive is a reversible lifecycle status, not content deletion

Archive remains a normal status-only update that creates the next revision and
snapshot. It does not remove any snapshot or project. Restoring an archived
project through the existing archive control changes its status to `draft` and
creates a new revision. Because this is only a lifecycle transition, it follows
the current behavior and does not invalidate evidence.

The version-restore operation is different: it always invalidates evidence and
sets the resulting status to `draft`, including when the source snapshot was
archived. This makes the safe active-library outcome explicit. If an owner later
needs to inspect the archived state, the source snapshot remains available; a
restore is not a way to hide an archive.

Archive is not a retention policy. Purging snapshots, compacting history,
deleting projects, and recovering a deleted database require a separate
retention and backup decision.

### 5. The write is one atomic transaction

For create, update, archive, and version restore, the current row, snapshot row,
and history row must be committed together. A transaction must roll back all
three writes if validation, digest verification, serialization, a uniqueness
constraint, or SQLite write fails. The client must continue to see the prior
current project and revision after a failed restore.

For restore specifically, the order is:

1. Validate the request shape and current-revision precondition.
2. Read the source snapshot and verify its digest, project ID, schema version,
   JSON shape, and source revision.
3. Construct the new project document, clear evidence, set status to `draft`,
   and assign `currentRevision + 1`.
4. Insert the new snapshot and history row and update `projects` in one
   transaction.
5. Return the committed project only after the transaction succeeds.

If another writer advances the project first, return the existing 409 conflict
shape and make no write. If the source revision is absent or corrupt, return a
non-success error identifying that the source is unavailable or invalid and
make no write. Do not silently fall back to the current row.

## Compatibility and old data

Existing databases have current project rows and history metadata but no
historical JSON. They cannot honestly offer restoration of revisions that
predate snapshot capture.

The later migration should be explicit and separately reviewed:

- Create the snapshot table without changing existing project data.
- Validate each current `projects.data` document against the current schema.
- Insert one snapshot for each current project at its current revision with an
  action such as `migration-baseline` and a recorded capture timestamp.
- Mark or expose that snapshot as a migration baseline, so the UI does not imply
  that revisions 1 through N have become recoverable.
- Leave existing `history` rows intact. Do not manufacture old JSON from their
  summaries.
- Abort the migration transaction for a project if its current JSON or digest
  cannot be validated, and report the project for manual recovery.

An old project with current revision 7 would therefore have a known snapshot for
revision 7 after migration, but not for revisions 1 through 6. A project JSON
export made before this feature remains a portable import, not a full database
backup and not proof of its activity history.

Schema-version handling must be conservative. A future snapshot schema that the
running application cannot validate is unavailable for restore, while the
project remains editable or archivable under the rules already documented for
the current schema. Do not reinterpret unknown fields or silently downgrade a
snapshot.

## Proposed read contract

The existing history response can grow an availability indicator without making
old rows look restorable:

```json
{
  "revision": 3,
  "at": "2026-09-07T12:00:00+00:00",
  "action": "updated",
  "summary": "Project updated",
  "restorable": true
}
```

For a pre-feature metadata row, `restorable` is `false`. For a missing or
digest-invalid snapshot, it is also `false`, with a non-sensitive diagnostic
available to the owner. A separate endpoint could return a validated snapshot
preview later, but this proposal does not require exposing full historical
content in the existing list view.

The restore request should reject `sourceRevision` values that are not marked
restorable. A client must not infer availability from a contiguous revision
number sequence.

## Acceptance scenarios

These are design acceptance scenarios for a future implementation. They are not
claims that the current application passes them.

1. **Create captures a baseline.** Create a synthetic project. Its current
   revision is 1, its history contains revision 1, and one matching immutable
   snapshot exists. The stored digest matches the canonical JSON bytes.

2. **Update preserves the prior document.** Save a material change from r1 to
   r2. The current row is r2, both snapshots exist, and r1 still contains the
   original name, instructions and evidence.

3. **Restore is append-only.** Restore r1 while the current revision is r2.
   The response and current row are r3 with the r1 content, the project ID and
   original creation timestamp preserved, and r1 and r2 remain unchanged.

4. **Restore invalidates evidence.** Restore a snapshot containing a passing
   case. The new r3 case has blank `actual` and `not-run` status; readiness does
   not pass until fresh evidence is recorded.

5. **Archive remains recoverable.** Archive a project, restart the service, and
   confirm the project remains in the archive view. Restore it through the
   lifecycle control and confirm a new draft revision exists without deleting
   the archived snapshot.

6. **Stale restore conflicts.** Two clients read r4. Client A advances to r5.
   Client B requests restore with `currentRevision: 4`; the server returns 409,
   leaves r5 current, and adds no snapshot or history row.

7. **Bad source is a no-op.** Request a nonexistent, schema-invalid, or
   digest-invalid source revision. The server returns an error and the current
   row, snapshot count and history remain unchanged.

8. **Write failure rolls back.** Force a synthetic SQLite failure after the
   proposed current-row, snapshot, or history write. After reopening the
   database, either all records for the new revision exist consistently or none
   do. No partial current state is observable.

9. **Pre-feature history is honest.** Load an old fixture containing projects
   and history but no snapshot table. The migration creates only a clearly
   labelled current baseline; old metadata revisions are shown as not
   restorable, and no historical content is invented.

10. **Unavailable future schema is bounded.** Present a snapshot with an
    unsupported schema version. The server refuses restore without changing the
    project and reports the source as unavailable rather than attempting a
    lossy downgrade.

## Limitations and non-decisions

- This is not a backup or disaster-recovery design. A damaged or deleted SQLite
  file still needs a separate private backup and recovery procedure.
- Immutable in the application database does not protect against an owner with
  direct filesystem or SQLite write access. File permissions and loopback scope
  remain the current local safety boundary.
- Snapshots do not make canon changes, Skillz source changes, external GPT
  deployment, or target-environment evaluation reversible.
- A restored project keeps its identity but receives a new revision. Consumers
  must use the revision as the content version and must not key external work on
  revision alone without the project ID.
- Retention limits, snapshot compression, encryption, cross-device sync,
  conflict merging, branching, deletion, and public or multiuser hosting are
  intentionally unspecified.
- No current runtime or test result demonstrates this proposal. Implementation
  requires a separate migration and engine task, followed by focused SQLite
  failure and recovery checks.

## Next action

Owner review the decisions about always-reset-on-restore evidence and archived
source status. If accepted, implement the schema and transaction contract in a
separate engine change with a migration plan and synthetic fixture tests.
