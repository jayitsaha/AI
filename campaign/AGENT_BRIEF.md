# Topic Builder Brief — AI/ML Vault Campaign

You are producing **ONE** AI/ML Vault topic **end-to-end** to a strict quality bar.
Your topic name, Notion `page_id`, and classification metadata are given in the task prompt.


## Step 0 — Read the spec + the gold standard (MANDATORY, do this first)

1. Read the full pipeline spec: `/Users/j0s0yz3/.wibey/skills/ai-pipeline/SKILL.md`
2. Read the gold-standard example you must match:
   `/Users/j0s0yz3/Documents/PersonalSkillUp/AI/explainers/generalized_least_squares_gls_explainer.html`
3. Skim the Notion helper library (do NOT edit it):
   `/Users/j0s0yz3/Documents/PersonalSkillUp/AI/notion_template.py`

The GLS file is the **minimum quality bar**: ~800 lines, a *bespoke* topic-specific
interactive canvas/SVG visualization (NOT a generic template), 6 collapsible cards,
KaTeX math, a step-synced code trace, light+dark themes, keyboard nav. Match this depth.

## Step 1 — Notion page (all 10 sections)

Write `/Users/j0s0yz3/Documents/PersonalSkillUp/AI/update_<slug>.py` that imports the
template and defines the content blocks, following the **exact 10-section structure** in
the skill (30-sec version → historical context → core concepts → PhD architecture deep-dive
→ full math derivation → from-scratch + production code → interview Q&A → comparison table
→ explainer embed → related topics). Then run it: `python3 update_<slug>.py`.

Rules:
- ALL math uses `equation_block(...)` / `eq(...)` — NEVER plain-text math. LaTeX conventions per skill §4c.
- Use the template helpers only. Do NOT use Notion MCP tools or raw curl for body content.
- Set these properties via `update_page(PAGE_ID, ICON, PROPERTIES, blocks)`:
  - `Status`: `{"select": {"name": "Completed"}}`
  - `Depth`: `{"select": {"name": "<Foundational|Intermediate|Advanced|Expert>"}}`  (your judgment)
  - `Interview Priority`: `{"select": {"name": "<Must Know|Important|Good to Know|Bonus>"}}` (your judgment)
  - `Has Explainer`: `{"checkbox": True}`
  - `Explainer URL`: `{"url": "<EXPLAINER_URL>"}` (see Step 3 for exact format)
- ICON by depth: Foundational→🟢, Intermediate→🟡, Advanced→🟠, Expert→🔴
- Do NOT set `Category` (pre-computed). Do NOT touch `Part`/`Section`/`Subsection`.
- After the script runs successfully, **delete** `update_<slug>.py`.

## Step 2 — Interactive HTML explainer (bespoke)

Create `/Users/j0s0yz3/Documents/PersonalSkillUp/AI/explainers/<slug>_explainer.html`,
a single self-contained file, using the EXACT design tokens + component system in the skill
(copy the `:root` light/dark CSS from the GLS file). Requirements:
- Header (title, subtitle, tags), 4–6 collapsible educational cards, 500–1000 words prose.
- ONE genuinely animated/interactive visualization whose *type matches the topic*
  (see "Visualization Type Selection" in the skill — architecture flow / parameter sliders /
  distribution / attention heatmap / matrix ops / generative steps / pipeline / training dynamics).
  It must be topic-specific and correct — NOT a copy of the GLS scatter plot.
- Prev/Next/Reset + arrow-key nav, progress dots, legend, step-synced info card.
- KaTeX CDN in `<head>`; all math via `$$...$$` (display) and `\(...\)` (inline).
- Numerically correct traces (compute real intermediate values).

## Step 3 — Explainer URL format (CRITICAL — match the live GLS page)

The repo is `PersonalSkillUp`, served at `https://jayitsaha.github.io/PersonalSkillUp/`.
Use EXACTLY this format (the skill's shorter form is outdated — the working GLS page uses this):

```
https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/<slug>_explainer.html
```

The `<slug>` MUST be identical in the HTML filename and the Explainer URL.
Slug = concise snake_case of the topic (shorten very long names sensibly, keep it recognizable).

## Step 4 — Do NOT git push. Do NOT git commit.

The user pushes manually. Leave files on disk.

## Step 5 — Report back (your final message)

Return ONLY:
- `slug`
- `<slug>_explainer.html` created (yes/no)
- Notion update ran successfully (yes/no) + Depth + Interview Priority you assigned
- Any errors or judgment calls the reviewer should double-check (especially math correctness)
