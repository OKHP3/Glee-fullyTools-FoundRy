# Technology Inventory and Version Policy

> Review date: 2026-09-08

This repository combines the canonical documentation workbench with an owner-local
loopback application under `app/`. The application uses Python's standard library,
SQLite, and vanilla browser JavaScript/CSS. The separate `web-templates/` folder
remains source material for child repositories.

## Technologies found

| Technology | In-place use | In-place version | Latest stable checked | Update posture |
|---|---|---:|---:|---|
| Python | `app/server.py`, application tests, and maintenance scripts use the Python standard library. | Application requires Python `3.11+`; app CI pins `3.11`; audit CI selects `3.x` | `3.14.6` | Keep the application floor at 3.11 until compatibility is deliberately raised; CI follows the latest stable line for the audit. |
| SQLite | Durable owner-local working records through Python's `sqlite3` module. | Bundled with the selected Python interpreter; no separate version pin | Python 3.14.6 ships SQLite 3.50.4 | Track through the Python runtime; do not add a separate database service. |
| JavaScript | Vanilla browser behavior in `app/static/app.js` and `web-templates/assets/js/app.js`. | Unpinned language/runtime; browser supplied | ECMAScript 2026, ECMA-262 17th edition | Track the browser platform. No Node/npm toolchain is used to build the app. |
| HTML | Static page template in `web-templates/index.html`. | HTML Living Standard, no repository pin | Living standard | Validate in the consuming child repository when a page is deployed. |
| CSS | Hand-authored stylesheets in `web-templates/theme.css` and `web-templates/assets/css/theme.css`. | No framework or version pin | CSS Snapshot 2025 | Continue using standards-based CSS. Tailwind and PostCSS are not present. |
| Mermaid | CDN ES module loaded by `web-templates/index.html`. | `11.17.2` | `11.17.2` | Review the pinned release when Mermaid publishes a newer version. |
| Google Fonts | Remote font stylesheet for Fredoka, Open Sans, Poppins, and DM Sans. | No semantic package version | Service-managed | Check URL availability; font families and weights are the meaningful contract. |
| Ko-fi widget | Remote script loaded by the HTML template. | No public version pin | Service-managed | Check URL availability; update only when Ko-fi changes the integration contract. |
| YAML | `manifest.yaml` and YAML-shaped fenced content in governed Markdown. | PyYAML declared in `requirements.txt` for manifest validation | YAML 1.2.2 | Keep canonical files Markdown/YAML compatible. |
| JSON Schema | `schemas/manifest.schema.yaml` validates the current root manifest. | jsonschema declared in `requirements.txt` | Draft 2020-12 | Keep the schema aligned with the current manifest shape. |
| Markdown | Canon, governance, prompts, inventory, and documentation. | No renderer pin | CommonMark has no single runtime release | Render in the consuming platform. |
| Git | Repository version control. | Not pinned by this repository | `2.55.0` | Developer-machine tooling; document only, do not install or upgrade from CI. |
| GitHub Actions | Application checks and scheduled technology auditing. | `actions/checkout@v7`, `actions/setup-python@v7` | `v7` / `v7` | Dependabot monitors action references monthly. |

## Explicitly absent

The repository has no `package.json`, lockfile, `pyproject.toml`, `tsconfig.json`,
Vite configuration, Tailwind configuration, React source, or Node/npm runtime
declaration. `requirements.txt` is present for manifest-validation tooling, but
the owner-local application itself uses the Python standard library and does not
require package installation. GitHub Actions workflows are present for application
checks and technology auditing; no hosted deployment workflow is configured.
References to Vite, TypeScript and Tailwind in planning documents describe
possible architectures, not technologies used by the current solution.
## Update plan

1. Keep this inventory as the human-readable baseline.
2. Run `scripts/audit-technology-versions.py` monthly and on demand. It reads live
   Mermaid npm metadata and confirms that CI selects the current stable Python 3
   line, then fails when the Mermaid CDN major is behind the latest stable major.
3. Review the failed workflow before changing Mermaid. A major update can change
   diagram parsing or rendering behavior, so the script reports the exact file and
   URL that need review rather than silently rewriting canonical template assets.
4. Let Dependabot propose updates to the GitHub Actions used by the audit workflow.
5. If this workbench later becomes a real frontend or Python package, add a lockfile
   and a runtime declaration first. Then extend Dependabot and CI to test upgrades
   before merging them.

## Sources checked

- [Python downloads](https://www.python.org/downloads/)
- [Mermaid package versions](https://www.npmjs.com/package/mermaid)
- [ECMA-262 standard](https://ecma-international.org/publications-and-standards/standards/ecma-262/)
- [W3C CSS Snapshot 2025](https://www.w3.org/TR/css-2025/)
- [Git documentation](https://git-scm.com/docs/git)
