# Topic Builder Brief — HTML EXPLAINER ONLY (hybrid mode)

You build ONLY the interactive HTML explainer for one topic. The Notion page is being
built separately by another system — do NOT touch Notion, do NOT write any update script.

## Step 0 — Invoke the skills (mandatory)
1. **Invoke the `/ai-pipeline` skill** (Skill tool) — follow its "Interactive HTML Explainer"
   design system, component list, and visualization-type guidance.
2. **Invoke the `/frontend-design` skill** (Skill tool) — apply its craft to the explainer.
3. Match/exceed the gold standard (~800 lines, bespoke interactive viz, 6 cards, KaTeX,
   light+dark, keyboard nav):
   `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/explainers/generalized_least_squares_gls_explainer.html`

## ⭐ THE INTERACTIVE DIAGRAM IS THE #1 DELIVERABLE
The animated, topic-specific visualization is the centerpiece — spend most of your effort here and make
it flawless. It MUST be a real working `<canvas>`/`<svg>` diagram (never a placeholder or empty box),
compute all shown numbers LIVE in JS from the actual math, visibly change on every Prev/Next step and on
every slider/toggle, and have ≥8 meaningful steps. The "Interactive Walkthrough" card must NEVER be
empty. Verify (headless browser or a mental run) that the viz actually renders and steps with no JS
errors before you finish.

## Step 1 — Build the explainer
Create `/Users/jayitsaha/Downloads/PersonalSkillUp/AI/explainers/<SLUG>_explainer.html`
using the EXACT `<SLUG>` given in your task prompt (it must match the Notion embed URL).
Single self-contained file. Requirements:
- Header (title, subtitle, tags), 4–6 collapsible educational cards, 500–1000 words prose.
- ONE genuinely animated/interactive visualization whose TYPE matches the topic
  (architecture flow / parameter sliders / distribution / attention heatmap / matrix ops /
  trellis / generative steps / pipeline / training dynamics). Topic-specific and correct —
  compute REAL numeric values in JS, not hard-coded fakes.
- Prev/Next/Reset + arrow-key nav (← → R), progress dots, legend, step-synced info card.
- Copy the `:root` light/dark design tokens from the gold-standard file.
- KaTeX CDN in `<head>`; all math via `$$...$$` (display) and `\(...\)` (inline).

## Step 1.5 — ANTI-TIMEOUT: build in STAGES
Write a compact skeleton first (head + tokens + header + empty cards + script scaffold),
then add each card and the viz JS in SEPARATE Edit calls. Never one giant Write.
Do NOT add a re-read/verification stage at the end (speed mode).

## Step 2 — Do NOT git push/commit. Do NOT touch Notion. Leave the file on disk.

## Step 3 — Report back ONE line only:
`<slug> | HTML:y/n | <one-word viz type>`
