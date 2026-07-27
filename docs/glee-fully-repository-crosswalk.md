# Glee-fully Child Repository Crosswalk

> **Operational inventory snapshot:** 2026-07-26  
> **Scope rule:** every accessible child or supporting GitHub repository and adjacent local clone whose name contains `glee-fully`, excluding the primary website and this FoundRy.

This is a non-canonical discovery and coordination aid. The canonical entity record remains the data ledger in `canon/`; this document records the current GitHub and local-checkout pairing used to interrogate and coordinate the Glee-fully child ecosystem.

## Coverage

| Measure | Observed result |
|---|---:|
| GitHub repositories in scope | 51 |
| Adjacent local Git clones in scope | 51 |
| Exact repository-to-clone matches | 51 |
| GitHub repositories with administrative connector permission | 51 |
| Private repositories | 50 |
| Public repositories | 1 |
| Local working trees with uncommitted changes | 0 |
| Local default working branch | `main` |

The excluded repositories are `OKHP3/Glee-fullyTools` (the public GitHub Pages website) and `OKHP3/Glee-fullyTools-FoundRy` (this FoundRy workbench).

## Interaction boundary

The connected GitHub account can read repository data and supports write-capable operations, including branches, files, commits, pull requests, issues, labels, and comments. Remote changes must still have an explicit target and instruction.

The current environment can inspect all adjacent local clones and their Git state. Its write sandbox is limited to this FoundRy checkout, so editing a sibling clone requires explicit filesystem authorization before any local mutation.

## Crosswalk

| Repository | Ecosystem role | GitHub repository | Local clone | Visibility | Local state |
|---|---|---|---|---|---|
| `glee-fully-chai-chasers` | Ecosystem support | [OKHP3/glee-fully-chai-chasers](https://github.com/OKHP3/glee-fully-chai-chasers) | `../glee-fully-chai-chasers` | public | `main` / clean |
| `glee-fully-gpt00-personalizable-tools` | Toolbox / Tool | [OKHP3/glee-fully-gpt00-personalizable-tools](https://github.com/OKHP3/glee-fully-gpt00-personalizable-tools) | `../glee-fully-gpt00-personalizable-tools` | private | `main` / clean |
| `glee-fully-gpt01-discovered-careers` | Toolbox / Tool | [OKHP3/glee-fully-gpt01-discovered-careers](https://github.com/OKHP3/glee-fully-gpt01-discovered-careers) | `../glee-fully-gpt01-discovered-careers` | private | `main` / clean |
| `glee-fully-gpt01a-resume-builder` | Tool-ette | [OKHP3/glee-fully-gpt01a-resume-builder](https://github.com/OKHP3/glee-fully-gpt01a-resume-builder) | `../glee-fully-gpt01a-resume-builder` | private | `main` / clean |
| `glee-fully-gpt01b-resume-customizer` | Tool-ette | [OKHP3/glee-fully-gpt01b-resume-customizer](https://github.com/OKHP3/glee-fully-gpt01b-resume-customizer) | `../glee-fully-gpt01b-resume-customizer` | private | `main` / clean |
| `glee-fully-gpt01c-career-fitness` | Tool-ette | [OKHP3/glee-fully-gpt01c-career-fitness](https://github.com/OKHP3/glee-fully-gpt01c-career-fitness) | `../glee-fully-gpt01c-career-fitness` | private | `main` / clean |
| `glee-fully-gpt01d-letter-composer` | Tool-ette | [OKHP3/glee-fully-gpt01d-letter-composer](https://github.com/OKHP3/glee-fully-gpt01d-letter-composer) | `../glee-fully-gpt01d-letter-composer` | private | `main` / clean |
| `glee-fully-gpt01e-blinkin-tuner` | Tool-ette | [OKHP3/glee-fully-gpt01e-blinkin-tuner](https://github.com/OKHP3/glee-fully-gpt01e-blinkin-tuner) | `../glee-fully-gpt01e-blinkin-tuner` | private | `main` / clean |
| `glee-fully-gpt01f-career-seeker` | Tool-ette | [OKHP3/glee-fully-gpt01f-career-seeker](https://github.com/OKHP3/glee-fully-gpt01f-career-seeker) | `../glee-fully-gpt01f-career-seeker` | private | `main` / clean |
| `glee-fully-gpt02-treasured-finds` | Toolbox / Tool | [OKHP3/glee-fully-gpt02-treasured-finds](https://github.com/OKHP3/glee-fully-gpt02-treasured-finds) | `../glee-fully-gpt02-treasured-finds` | private | `main` / clean |
| `glee-fully-gpt02a-personal-librarian` | Tool-ette | [OKHP3/glee-fully-gpt02a-personal-librarian](https://github.com/OKHP3/glee-fully-gpt02a-personal-librarian) | `../glee-fully-gpt02a-personal-librarian` | private | `main` / clean |
| `glee-fully-gpt02b-decor-detective` | Tool-ette | [OKHP3/glee-fully-gpt02b-decor-detective](https://github.com/OKHP3/glee-fully-gpt02b-decor-detective) | `../glee-fully-gpt02b-decor-detective` | private | `main` / clean |
| `glee-fully-gpt02c-present-hoarder` | Tool-ette | [OKHP3/glee-fully-gpt02c-present-hoarder](https://github.com/OKHP3/glee-fully-gpt02c-present-hoarder) | `../glee-fully-gpt02c-present-hoarder` | private | `main` / clean |
| `glee-fully-gpt02d-scentinal-journal` | Tool-ette | [OKHP3/glee-fully-gpt02d-scentinal-journal](https://github.com/OKHP3/glee-fully-gpt02d-scentinal-journal) | `../glee-fully-gpt02d-scentinal-journal` | private | `main` / clean |
| `glee-fully-gpt02e-spirited-journal` | Tool-ette | [OKHP3/glee-fully-gpt02e-spirited-journal](https://github.com/OKHP3/glee-fully-gpt02e-spirited-journal) | `../glee-fully-gpt02e-spirited-journal` | private | `main` / clean |
| `glee-fully-gpt02f-supply-haus` | Tool-ette | [OKHP3/glee-fully-gpt02f-supply-haus](https://github.com/OKHP3/glee-fully-gpt02f-supply-haus) | `../glee-fully-gpt02f-supply-haus` | private | `main` / clean |
| `glee-fully-gpt02g-bag-nabbit` | Tool-ette | [OKHP3/glee-fully-gpt02g-bag-nabbit](https://github.com/OKHP3/glee-fully-gpt02g-bag-nabbit) | `../glee-fully-gpt02g-bag-nabbit` | private | `main` / clean |
| `glee-fully-gpt03-tasty-tracker` | Toolbox / Tool | [OKHP3/glee-fully-gpt03-tasty-tracker](https://github.com/OKHP3/glee-fully-gpt03-tasty-tracker) | `../glee-fully-gpt03-tasty-tracker` | private | `main` / clean |
| `glee-fully-gpt03a-flavor-meister` | Tool-ette | [OKHP3/glee-fully-gpt03a-flavor-meister](https://github.com/OKHP3/glee-fully-gpt03a-flavor-meister) | `../glee-fully-gpt03a-flavor-meister` | private | `main` / clean |
| `glee-fully-gpt03b-menu-conductor` | Tool-ette | [OKHP3/glee-fully-gpt03b-menu-conductor](https://github.com/OKHP3/glee-fully-gpt03b-menu-conductor) | `../glee-fully-gpt03b-menu-conductor` | private | `main` / clean |
| `glee-fully-gpt03c-wishful-tastes` | Tool-ette | [OKHP3/glee-fully-gpt03c-wishful-tastes](https://github.com/OKHP3/glee-fully-gpt03c-wishful-tastes) | `../glee-fully-gpt03c-wishful-tastes` | private | `main` / clean |
| `glee-fully-gpt03d-pantry-shopper` | Tool-ette | [OKHP3/glee-fully-gpt03d-pantry-shopper](https://github.com/OKHP3/glee-fully-gpt03d-pantry-shopper) | `../glee-fully-gpt03d-pantry-shopper` | private | `main` / clean |
| `glee-fully-gpt03e-palatably-profiled` | Tool-ette | [OKHP3/glee-fully-gpt03e-palatably-profiled](https://github.com/OKHP3/glee-fully-gpt03e-palatably-profiled) | `../glee-fully-gpt03e-palatably-profiled` | private | `main` / clean |
| `glee-fully-gpt04-travelers-guide` | Toolbox / Tool | [OKHP3/glee-fully-gpt04-travelers-guide](https://github.com/OKHP3/glee-fully-gpt04-travelers-guide) | `../glee-fully-gpt04-travelers-guide` | private | `main` / clean |
| `glee-fully-gpt04a-journey-diary` | Tool-ette | [OKHP3/glee-fully-gpt04a-journey-diary](https://github.com/OKHP3/glee-fully-gpt04a-journey-diary) | `../glee-fully-gpt04a-journey-diary` | private | `main` / clean |
| `glee-fully-gpt04b-itinerary-hacker` | Tool-ette | [OKHP3/glee-fully-gpt04b-itinerary-hacker](https://github.com/OKHP3/glee-fully-gpt04b-itinerary-hacker) | `../glee-fully-gpt04b-itinerary-hacker` | private | `main` / clean |
| `glee-fully-gpt04c-detour-discoverer` | Tool-ette | [OKHP3/glee-fully-gpt04c-detour-discoverer](https://github.com/OKHP3/glee-fully-gpt04c-detour-discoverer) | `../glee-fully-gpt04c-detour-discoverer` | private | `main` / clean |
| `glee-fully-gpt04d-dreamland-journeys` | Tool-ette | [OKHP3/glee-fully-gpt04d-dreamland-journeys](https://github.com/OKHP3/glee-fully-gpt04d-dreamland-journeys) | `../glee-fully-gpt04d-dreamland-journeys` | private | `main` / clean |
| `glee-fully-gpt04e-memento-log` | Tool-ette | [OKHP3/glee-fully-gpt04e-memento-log](https://github.com/OKHP3/glee-fully-gpt04e-memento-log) | `../glee-fully-gpt04e-memento-log` | private | `main` / clean |
| `glee-fully-gpt05-organized-life` | Toolbox / Tool | [OKHP3/glee-fully-gpt05-organized-life](https://github.com/OKHP3/glee-fully-gpt05-organized-life) | `../glee-fully-gpt05-organized-life` | private | `main` / clean |
| `glee-fully-gpt05a-task-maestro` | Tool-ette | [OKHP3/glee-fully-gpt05a-task-maestro](https://github.com/OKHP3/glee-fully-gpt05a-task-maestro) | `../glee-fully-gpt05a-task-maestro` | private | `main` / clean |
| `glee-fully-gpt05b-thrifty-spender` | Tool-ette | [OKHP3/glee-fully-gpt05b-thrifty-spender](https://github.com/OKHP3/glee-fully-gpt05b-thrifty-spender) | `../glee-fully-gpt05b-thrifty-spender` | private | `main` / clean |
| `glee-fully-gpt05c-giftlist-helper` | Tool-ette | [OKHP3/glee-fully-gpt05c-giftlist-helper](https://github.com/OKHP3/glee-fully-gpt05c-giftlist-helper) | `../glee-fully-gpt05c-giftlist-helper` | private | `main` / clean |
| `glee-fully-gpt05d-scheduling-wizard` | Tool-ette | [OKHP3/glee-fully-gpt05d-scheduling-wizard](https://github.com/OKHP3/glee-fully-gpt05d-scheduling-wizard) | `../glee-fully-gpt05d-scheduling-wizard` | private | `main` / clean |
| `glee-fully-gpt05e-lifestyle-wallboard` | Tool-ette | [OKHP3/glee-fully-gpt05e-lifestyle-wallboard](https://github.com/OKHP3/glee-fully-gpt05e-lifestyle-wallboard) | `../glee-fully-gpt05e-lifestyle-wallboard` | private | `main` / clean |
| `glee-fully-gpt05f-neighborly-bazaar` | Tool-ette | [OKHP3/glee-fully-gpt05f-neighborly-bazaar](https://github.com/OKHP3/glee-fully-gpt05f-neighborly-bazaar) | `../glee-fully-gpt05f-neighborly-bazaar` | private | `main` / clean |
| `glee-fully-gpt06-healthy-bee-ing` | Toolbox / Tool | [OKHP3/glee-fully-gpt06-healthy-bee-ing](https://github.com/OKHP3/glee-fully-gpt06-healthy-bee-ing) | `../glee-fully-gpt06-healthy-bee-ing` | private | `main` / clean |
| `glee-fully-gpt06a-care-check` | Tool-ette | [OKHP3/glee-fully-gpt06a-care-check](https://github.com/OKHP3/glee-fully-gpt06a-care-check) | `../glee-fully-gpt06a-care-check` | private | `main` / clean |
| `glee-fully-gpt06b-calm-keep` | Tool-ette | [OKHP3/glee-fully-gpt06b-calm-keep](https://github.com/OKHP3/glee-fully-gpt06b-calm-keep) | `../glee-fully-gpt06b-calm-keep` | private | `main` / clean |
| `glee-fully-gpt06c-snappy-count` | Tool-ette | [OKHP3/glee-fully-gpt06c-snappy-count](https://github.com/OKHP3/glee-fully-gpt06c-snappy-count) | `../glee-fully-gpt06c-snappy-count` | private | `main` / clean |
| `glee-fully-gpt06d-medi-minder` | Tool-ette | [OKHP3/glee-fully-gpt06d-medi-minder](https://github.com/OKHP3/glee-fully-gpt06d-medi-minder) | `../glee-fully-gpt06d-medi-minder` | private | `main` / clean |
| `glee-fully-gpt06e-moody-log` | Tool-ette | [OKHP3/glee-fully-gpt06e-moody-log](https://github.com/OKHP3/glee-fully-gpt06e-moody-log) | `../glee-fully-gpt06e-moody-log` | private | `main` / clean |
| `glee-fully-gpt06f-maven-wise` | Tool-ette | [OKHP3/glee-fully-gpt06f-maven-wise](https://github.com/OKHP3/glee-fully-gpt06f-maven-wise) | `../glee-fully-gpt06f-maven-wise` | private | `main` / clean |
| `glee-fully-gpt07-identity-known` | Toolbox / Tool | [OKHP3/glee-fully-gpt07-identity-known](https://github.com/OKHP3/glee-fully-gpt07-identity-known) | `../glee-fully-gpt07-identity-known` | private | `main` / clean |
| `glee-fully-gpt07a-critter-spotter` | Tool-ette | [OKHP3/glee-fully-gpt07a-critter-spotter](https://github.com/OKHP3/glee-fully-gpt07a-critter-spotter) | `../glee-fully-gpt07a-critter-spotter` | private | `main` / clean |
| `glee-fully-gpt07b-roost-wrangler` | Tool-ette | [OKHP3/glee-fully-gpt07b-roost-wrangler](https://github.com/OKHP3/glee-fully-gpt07b-roost-wrangler) | `../glee-fully-gpt07b-roost-wrangler` | private | `main` / clean |
| `glee-fully-gpt07c-sight-seeker` | Tool-ette | [OKHP3/glee-fully-gpt07c-sight-seeker](https://github.com/OKHP3/glee-fully-gpt07c-sight-seeker) | `../glee-fully-gpt07c-sight-seeker` | private | `main` / clean |
| `glee-fully-gpt07d-snap-decoder` | Tool-ette | [OKHP3/glee-fully-gpt07d-snap-decoder](https://github.com/OKHP3/glee-fully-gpt07d-snap-decoder) | `../glee-fully-gpt07d-snap-decoder` | private | `main` / clean |
| `glee-fully-gpt07e-motif-muse` | Tool-ette | [OKHP3/glee-fully-gpt07e-motif-muse](https://github.com/OKHP3/glee-fully-gpt07e-motif-muse) | `../glee-fully-gpt07e-motif-muse` | private | `main` / clean |
| `glee-fully-gpt07f-maker-matcher` | Tool-ette | [OKHP3/glee-fully-gpt07f-maker-matcher](https://github.com/OKHP3/glee-fully-gpt07f-maker-matcher) | `../glee-fully-gpt07f-maker-matcher` | private | `main` / clean |
| `glee-fully-gpt07g-self-fixer` | Tool-ette | [OKHP3/glee-fully-gpt07g-self-fixer](https://github.com/OKHP3/glee-fully-gpt07g-self-fixer) | `../glee-fully-gpt07g-self-fixer` | private | `main` / clean |

## Recommended operating pattern

1. Start with a read-only cross-repository audit: manifests, branch state, recent commits, governance files, and known drift.
2. Record findings in a dedicated non-canonical report, linking back to the relevant canonical ledger where applicable.
3. For a change that spans repositories, prepare a per-repository plan and apply changes in isolated commits or pull requests.
4. Treat each child repository's own `AGENTS.md` and governance documents as controlling for changes made inside that repository.
