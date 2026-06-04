# web-templates/ — Webpage Template Assets

> ⚠️ **These are template source files, NOT a deployable website.**
> Do not configure a web server workflow to serve this folder from this workbench.
> These assets are intended for use in child repositories that host Glee-fully
> public-facing pages (e.g. Tool-ette landing pages on glee-fully.tools).

## Contents

| File / Folder | Purpose |
|---------------|---------|
| `index.html` | Tool-ette page template — fill in `[TOOL-ETTE NAME]` placeholders |
| `theme.css` | Shared Glee-fully theme (root tokens, layout, nav, hero, cards, footer) |
| `assets/css/theme.css` | Same theme at the expected asset path for the served HTML |
| `assets/js/app.js` | Scroll-reveal, mobile nav, footer year, Ko-fi widget |
| `tool-and-tool-ette-page-updates.md` | Page update notes and change log |

## How to Use

1. Copy `index.html` and the `assets/` folder to the child repository's `web/` directory
2. Find and replace all `[TOOL-ETTE NAME]` and `[PARENT TOOL]` placeholders
3. Update the `href` on the ChatGPT launch button to the actual GPT URL
4. Update Open Graph and meta description tags
5. Add the Tool-ette's actual sections and content

## Template Variables to Replace

| Placeholder | Replace With |
|-------------|--------------|
| `[TOOL-ETTE NAME]` | The actual Tool-ette name |
| `Parent Tool Name` | The parent Tool (branch) name |
| `YOUR-GPT-ID-HERE` | The ChatGPT custom GPT ID |
| Meta description content | Tool-specific description |
| `og:url` | The published Tool-ette URL |

## Theme Overview

The CSS uses the Glee-fully brand system:
- **Fonts:** Fredoka (headings), Poppins (subheadings), Open Sans (body), DM Sans (accent)
- **Colors:** Rust-orange accent (`#c46a2c`), paper background (`#f6f2ee`)
- **Brand stripes:** Retro rainbow spectrum hero animation
- **Body class:** `glee-main` activates all Glee-fully brand overrides
