---
name: Post-merge hook configuration
description: The post-merge script is tracked separately from the ignored platform configuration.
---

The post-merge hook should be a tracked, idempotent script while its path and timeout are configured through Replit's post-merge settings. In this repository, `.replit` is ignored, so do not force-add it just to persist the platform setting.

**Why:** The platform can run the configured hook even when `.replit` is not part of Git, and force-adding the file would change the repository's existing configuration boundary.

**How to apply:** Use the post-merge configuration functions to set the script path and timeout, keep the script fast and non-interactive, and use an explicit commit identity if the checkout has no default Git author configured.