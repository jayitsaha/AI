# Deferred-HTML workflow (bank Notion pages now, build HTML later)

Strategy: NVIDIA builds Notion pages now (off Claude budget); Sonnet HTML explainers are
DEFERRED to save Claude usage, built later in a batch when the limit is fresh.

## Tracker
`campaign/pending_html.tsv` — one row per topic whose Notion page is built but HTML is NOT:
    <page_id>\t<topic>\t<slug>
Written by `campaign/nvidia/run_notion_waves.sh` (deduped by slug).

NOTE: notion-only pages have `Has Explainer=True` + an Explainer URL that 404s until the
HTML is built and pushed. That's expected — the URL is reserved.

## Bank more Notion pages (off Claude budget)
    bash campaign/nvidia/run_notion_waves.sh <K>     # K waves of 20, appends to pending_html.tsv

## Build the deferred HTML later (Sonnet — costs Claude tokens)
When the limit is fresh, Opus builds HTML for the pending topics:
1. Read `campaign/pending_html.tsv`.
2. For each slug WITHOUT an existing `explainers/<slug>_explainer.html`, spawn a Sonnet
   subagent following `campaign/BRIEF_HTML.md` with the EXACT slug (matches the Notion embed).
   Do ~20 at a time (watch for API instability; rebuild any that fail).
3. After a slug's HTML exists (≥15KB), remove its row from pending_html.tsv:
       python3 - <<'PY'
       import os
       keep=[l for l in open("campaign/pending_html.tsv")
             if not os.path.exists(f"explainers/{l.split(chr(9))[2].strip()}_explainer.html")]
       open("campaign/pending_html.tsv","w").writelines(keep)
       PY
4. Repeat until pending_html.tsv is empty.

## Status check any time
    echo "pending HTML: $(wc -l < campaign/pending_html.tsv)"
    # how many pending already have HTML on disk (ready to prune):
