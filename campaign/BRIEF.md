# Topic Builder Brief — AI/ML Vault (corrected paths, v2)

You build **ONE** AI/ML Vault topic **end-to-end** to a strict quality bar.
Your topic name, Notion `page_id`, and canonical index are in the task prompt.

## ⚡ SPEED MODE (commando — no self-QC)
Build once, ship. Do NOT re-read, grep, re-open, line-count, or "verify" the HTML after
writing it. Do NOT run a validation/QC pass. The ONLY hard gate is: the Notion
`update_<slug>.py` script must RUN successfully (exit 0). Trust your first pass on
everything else. Keep tool calls minimal.

## Step 0 — Invoke the skills + read the gold standard (do this first)
1. **Invoke the `/ai-pipeline` skill** (via the Skill tool) — this is MANDATORY for every
   task. Follow its exact 10-section structure and quality bar. Its spec also lives at
   `/Users/jayitsaha/.claude/skills/ai-pipeline/SKILL.md` for reference.
2. **Invoke the `/frontend-design` skill** (via the Skill tool) and apply its craft to the
   HTML explainer. Spec: `/Users/jayitsaha/.claude/skills/frontend-design/SKILL.md`
3. Gold-standard explainer you must match/exceed (~800 lines, bespoke interactive viz,
   6 cards, KaTeX, light+dark, keyboard nav):
   `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/explainers/generalized_least_squares_gls_explainer.html`
4. Notion helper library (do NOT edit it):
   `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/notion_template.py`

## Step 1 — Notion page (all 10 sections)
Write `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/update_<slug>.py` importing the
template, defining content blocks in the **exact 10-section structure** from the skill
(30-sec layman → historical context → core concepts → PhD architecture deep-dive →
full math derivation → from-scratch + production code → interview Q&A → comparison table
→ explainer embed → related topics). Then run: `python3 update_<slug>.py`.

Rules:
- ALL math uses `equation_block(...)` / `eq(...)` — NEVER plain-text math. LaTeX per skill §4c.
- Use the template helpers only. No Notion MCP tools, no raw curl for body content.
- Set via `update_page(PAGE_ID, ICON, PROPERTIES, blocks)`:
  - `Status`: `{"select": {"name": "Completed"}}`
  - `Depth`: `{"select": {"name": "<Foundational|Intermediate|Advanced|Expert>"}}` (your judgment)
  - `Interview Priority`: `{"select": {"name": "<Must Know|Important|Good to Know|Bonus>"}}` (your judgment)
  - `Has Explainer`: `{"checkbox": True}`
  - `Explainer URL`: `{"url": "<EXPLAINER_URL>"}` (format in Step 3)
- ICON by depth: Foundational→🟢, Intermediate→🟡, Advanced→🟠, Expert→🔴
- Do NOT set `Category` (pre-computed). Do NOT touch `Part`/`Section`/`Subsection`.
- The Notion token is already baked into `notion_template.py` — just run `python3 update_<slug>.py`, no env var needed.
- After the script runs successfully (exit 0, prints success), **delete** `update_<slug>.py`.

## Step 2 — Interactive HTML explainer (bespoke)
Create `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/explainers/<slug>_explainer.html`,
a single self-contained file, using the EXACT design tokens + component system in the skill
(copy the `:root` light/dark CSS from the GLS file). Requirements:
- Header (title, subtitle, tags), 4–6 collapsible educational cards, 500–1000 words prose.
- ONE genuinely animated/interactive visualization whose *type matches the topic*
  (see "Visualization Type Selection" in the skill). Topic-specific and correct —
  NOT a copy of the GLS scatter plot.
- Prev/Next/Reset + arrow-key nav, progress dots, legend, step-synced info card.
- KaTeX CDN in `<head>`; all math via `$$...$$` (display) and `\(...\)` (inline).
- Numerically correct traces (compute real intermediate values).
- Apply the frontend-design skill's craft (typography, spacing, restraint) on top of the tokens.

## Step 3 — Explainer URL format (CRITICAL — verified live)
The repo `AI` is served at `https://jayitsaha.github.io/AI/`. Use EXACTLY:
```
https://jayitsaha.github.io/AI/explainers/<slug>_explainer.html
```
(The `.../PersonalSkillUp/AI/...` form is WRONG — it 404s. Verified.)
`<slug>` MUST be identical in the HTML filename and the Explainer URL.
Slug = concise snake_case of the topic (shorten long names sensibly, keep recognizable).

## Step 3.5 — ANTI-TIMEOUT PROTOCOL (MANDATORY)
Build the ~800-line HTML in STAGES with multiple tool calls, never one giant Write:
1. Write a compact skeleton (head + `:root` tokens + header + empty card divs + `<script>` scaffold).
2. Add each educational card with a SEPARATE Edit.
3. Add the visualization JS in 1–2 more Edits.
Keep each tool call modest. Do NOT add a verification/re-read stage at the end.

## Step 4 — Do NOT git push or commit. Leave files on disk.

## Step 5 — Report back (ONE line only)
Return EXACTLY one line, nothing else:
`<slug> | HTML:y/n | Notion:y/n (<#blocks>) | <Depth>/<Priority>`
