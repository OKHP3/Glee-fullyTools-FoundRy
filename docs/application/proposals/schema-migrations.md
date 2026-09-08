# SQLite schema migration proposal

Status: **PROPOSAL**. This document specifies a future implementation contract. It does not change the application, migrate owner data, or claim that a migration runner exists.

## Decision boundary

The current application is an owner-local Python service using one ignored SQLite file, `.foundry-data/foundry.sqlite3`. The proposal covers that file only. It does not migrate canonical ledgers, exported packages, child repositories, Replit data, or any hosted service.

The database schema version is separate from the project JSON field `schemaVersion`. The former describes SQLite tables and migration state. The latter describes the portable project payload accepted by the API. A database migration must not silently rewrite a project payload or upgrade its JSON contract.

## Evidence and assumptions

| Claim | Tier | Evidence | Consequence if false | Next check |
|---|---|---|---|---|
| The current database has `projects` and `history` tables, with `data` stored as JSON text. | CONFIRMED | `app/server.py`, `Store.__init__`, lines 157-166 at base `32b8915` | The proposed legacy detector could miss an actual table or column. | Inspect a representative owner-created database before implementation. |
| The current database has no database-level version marker. | CONFIRMED | `app/server.py` creates tables but does not set or read `PRAGMA user_version`. | A first migration must distinguish the unmarked current shape from an unknown legacy shape. | Add a synthetic unmarked fixture to the migration test. |
| The current project payload version is `1`. | CONFIRMED | `app/server.py`, `Store.create`, import validation, and API contract | A database migration could be incorrectly coupled to project import compatibility. | Keep payload-version tests separate from database migration tests. |
| Immutable snapshots and richer recovery are future maturation work, not current behavior. | CONFIRMED | `docs/application/current-state-and-maturation.md`, “Recommended order of maturation”, stage 3 | A migration design could imply that historical project bodies are already restorable. | Revisit the v2 design after snapshot requirements are accepted. |
| F15 can provide implementation context, but no separate F15 migration artifact is present on `origin/main`. | UNKNOWN | F15 branch name exists locally, but it is at the same base and contains no migration proposal path. | A later F15 change may refine names or lifecycle assumptions. | Coordinator should reconcile this proposal with F15’s accepted output before implementation. |

The design below therefore treats the current table shape as observed and every migration policy as proposed.

## Version contract

Use SQLite `PRAGMA user_version` for the database version. The proposed versions are:

| Version | Meaning | Support |
|---:|---|---|
| `0` | Unmarked legacy database. This includes the current first-release shape when `user_version` is still zero. | Detect and migrate only after exact shape and data checks. |
| `1` | Current first-release shape: `projects(id, revision, data)` and `history(project_id, revision, at, action, summary)`, with the existing primary keys and no additional required tables. | Supported target. |
| `2+` | A newer database format whose migration code is not available in this release. | Refuse to open for writes. Preserve the file and request a compatible application. |

Only `0 -> 1` is specified and supported by this proposal. There is no invented `1 -> 2` transform. A future v2 must first document its data contract, backfill rule, downgrade policy, and recovery tests. The likely roadmap driver is restorable immutable project snapshots, but that is not a v2 schema decision yet.

## Startup and legacy detection

Migration should run before the store is exposed to request handlers and before any application write:

1. Resolve the configured data directory and database path. Keep the existing private-directory and file-mode boundary.
2. If no database exists, create the current tables in one transaction and set `user_version = 1`. This is initialization, not legacy migration.
3. If a database exists, open it with a bounded busy timeout and read `PRAGMA user_version`, `PRAGMA integrity_check`, and the table metadata from `sqlite_master` and `PRAGMA table_info`.
4. For `user_version = 1`, verify the exact required table and column contract, then run read-only row checks. A mismatched v1 file is an error, not an opportunity to guess.
5. For `user_version = 0`, accept it as legacy only when both required tables and all required columns match the observed current shape. Verify every project row has valid JSON, an object payload, matching `id` and `revision` types, and `schemaVersion = 1`; verify each history row has valid required values and references an existing project.
6. For `user_version > 1`, fail closed with an “unsupported database version” error. Do not run `CREATE TABLE`, `UPDATE`, `VACUUM`, or any repair operation.
7. For a missing table, extra incompatible column contract, malformed JSON, duplicate logical identity, failed integrity check, or impossible revision/history relationship, fail closed and leave the file untouched.

The detector must not infer a version from filenames, timestamps, row count, or a project payload alone. `user_version = 0` plus an unrecognized shape is unknown, not automatically current.

## Transaction and backup protocol

The migration runner should be a small standard-library operation called while the service is still starting:

1. Acquire the process migration lock. Refuse a second migration in the same data directory rather than allowing two writers to inspect and copy the same file.
2. Create a consistent private backup before the first write. Prefer SQLite’s backup API to copy the open database into a temporary backup path in a private backup directory. Flush and close the temporary file, verify it can be opened read-only, and atomically rename it to a recovery name such as `foundry.sqlite3.pre-migration-v0-to-v1.<UTC>.sqlite3`. Do not place backups in a tracked repository path.
3. Run `PRAGMA integrity_check` and the legacy shape/data checks against the live database. A failed preflight stops before `BEGIN IMMEDIATE`.
4. Start `BEGIN IMMEDIATE`. For `0 -> 1`, the data transformation is intentionally minimal: make no project or history row changes, set `PRAGMA user_version = 1`, and commit. If the current schema needs table creation for an unmarked fixture, create only the exact current tables inside this same transaction and then set the marker.
5. Before commit, re-read the required metadata, row counts, JSON records, and `PRAGMA integrity_check`. Any mismatch raises an error and rolls back.
6. After commit, reopen or re-read the database, confirm `user_version = 1`, and confirm the preflight row counts and identity sets are unchanged. Only then allow request handling.

SQLite DDL and `PRAGMA user_version` must remain inside the same transaction. No `executescript` call should be used if it can introduce an implicit commit that defeats this boundary.

## Failure and recovery behavior

- Backup creation or backup verification failure: abort startup before migration. Keep the original database unchanged and report the recovery path that was attempted.
- Preflight failure: abort startup without a write. Do not “repair” malformed owner data automatically.
- Lock or busy timeout: abort startup with a retryable message. Do not delete lock files or override another process.
- Migration exception before commit: issue `ROLLBACK`, close the connection, retain the original and backup, and abort startup.
- Post-commit verification failure: stop using the database, retain the backup and migrated file for inspection, and require explicit restore from the verified backup. Do not attempt a second automatic migration.
- Unsupported future version: read-only refusal. Do not downgrade, clear `user_version`, or drop unknown tables.
- Backup restore: stop the service, preserve the failed database under a new diagnostic name, copy the verified backup into the original path, restore private file permissions, and rerun startup checks. This is an explicit recovery operation, not an automatic response to ordinary validation errors.

The user-facing error should say that working data was not changed when that is true, name the database version or failed preflight, and point to the private backup or diagnostic file without exposing authored project contents.

## Supported test matrix

These are proposed synthetic tests for the future migration runner. They must use temporary directories and databases, never `.foundry-data` with owner records.

| Case | Fixture and action | Required result |
|---|---|---|
| Fresh initialization | Empty temporary directory; start the store. | Exact current tables exist, `user_version = 1`, and the service opens. |
| Legacy current shape | Create v0 database with the two observed tables, two valid projects, and history rows; migrate. | `0 -> 1` succeeds; project JSON, IDs, revisions, history rows, and row counts are byte-for-byte or semantically preserved; marker is 1. |
| Idempotent restart | Reopen the migrated fixture and invoke startup again. | No new backup migration, no row changes, and no duplicate history. |
| Payload distinction | Include a valid project `schemaVersion = 1`; run database migration. | Payload remains version 1. Database version is checked independently. |
| Missing table | Remove `history` from an otherwise unmarked fixture. | Startup fails before write; database remains unmarked and unchanged. |
| Bad payload | Put invalid JSON or a non-object JSON value in `projects.data`. | Startup fails closed; no partial conversion or silently discarded row. |
| Inconsistent history | Add a history row for a missing project or duplicate primary-key identity. | Preflight fails; no marker update. |
| Integrity failure | Corrupt a temporary SQLite fixture or make `integrity_check` fail. | Startup fails before migration and preserves the source file. |
| Future version | Set `user_version = 2` and add an unknown table/column. | Startup refuses writes and does not alter or drop the unknown shape. |
| Injected migration error | Force an error after `BEGIN IMMEDIATE` and before commit. | Rollback occurs; source content, marker, and row counts match the pre-migration snapshot; verified backup remains. |
| Backup failure | Deny the temporary backup destination or inject backup failure. | No migration transaction begins and the source database is unchanged. |
| Busy writer | Hold a write lock from a second temporary connection beyond the bounded timeout. | Migration exits with a retryable failure and does not bypass the lock. |
| Recovery | Restore the verified pre-migration backup after a simulated post-commit verification failure. | Original v0 fixture opens again, with the diagnostic copy retained. |

No test should use `expectedFailure`, skip an unavailable migration runtime, or weaken assertions to make a failed experiment pass. A test that cannot run should be reported as NOT RUN with its reason.

## Implementation guardrails

- Keep the migration code separate from request handlers and project validation.
- Use parameterized SQL and explicit allowlists for table and column names.
- Keep the existing loopback-only service boundary. A schema migration does not authorize hosting, cross-FoundRy synchronization, or database sharing.
- Never modify canon, exports, or application data as part of a schema migration.
- Log version, phase, outcome, backup path and row counts only. Do not log project JSON, authored text, or private identifiers beyond what is needed to diagnose a failure.
- Add implementation and migration tests only when the migration runner is authorized and assigned. This proposal itself adds no runtime or test changes.

## Acceptance boundary and next action

This proposal is complete as a design artifact, not as an implementation. It establishes one supported transition, explicit future-version refusal, a backup-before-write requirement, transactional behavior, and recovery test cases.

Next action: coordinator reconciles this proposal with the accepted F15 output and owner-approved stage-3 scope, then assigns a separate implementation change if the migration runner is wanted.
