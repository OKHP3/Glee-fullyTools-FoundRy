# Backup recovery rehearsal

`scripts/verify-foundry-backup.py` is a safe, standard-library rehearsal of the
documented full-folder backup path. It creates two synthetic projects, creates a
real revision history entry, closes the loopback service and SQLite connection,
copies the complete temporary data folder, restores it into a separate temporary
folder, then reads back every project and history entry.

Run it from the repository root:

```bash
python3 scripts/verify-foundry-backup.py
```

Expected output is a compact JSON result such as:

```json
{"history_entries": 3, "projects": 2, "status": "passed"}
```

The rehearsal never opens the default `.foundry-data/` directory. All source,
backup and restore folders are temporary and are removed when the process exits.
It uses loopback on an ephemeral port and does not require package installation,
credentials, network access or a running application instance.

The focused tests also remove one restored history row and assert that the
verifier fails. This guards against a rehearsal that checks only project rows
while silently losing revision history:

```bash
python3 -m unittest app.tests.test_backup_rehearsal -v
```

This is a recovery rehearsal, not a scheduled backup, a database migration, or
a substitute for an owner-approved private backup destination. For an actual
backup, stop the service first and copy the entire private `.foundry-data/`
folder as described in the application guide.
