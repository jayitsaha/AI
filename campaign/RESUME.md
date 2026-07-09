# AI Vault Campaign — Resume Pointer

PAUSED after Wave 3 (2026-07-08). 60 topics built this run (Waves 1-3).

## State (ground truth = Notion Status property)
- Notion Completed: 605 topics
- Queue cursor: 647 (canonical index in topic_page_ids.json)
- Floor: 583 (ScaNN — pinned start; earlier gaps 303-582 intentionally skipped)
- Target end: Part IX §33 (~index 1318) => ~730 topics remaining at pause

## How to resume
1. `python3 campaign/fastqueue.py --reconcile`   # sync truth from Notion
2. `python3 campaign/fastqueue.py --limit 20`     # pull next wave into campaign/next.txt
3. Spawn Sonnet workers (one per line) using campaign/BRIEF.md
4. On completion, reconcile + repeat.

## Gotchas already fixed (don't rediscover)
- Notion token was broken: fastqueue.py had a dead token (401); notion_template.py
  read empty NOTION_API_TOKEN. Both now fall back to the working token in-file.
- Correct explainer URL: https://jayitsaha.github.io/AI/explainers/<slug>_explainer.html
  (the .../PersonalSkillUp/AI/... form 404s). Baked into campaign/BRIEF.md.
- Each worker costs ~85-170k output tokens (full page + ~800-line HTML). ~730 left ≈ ~80M.
- Session-limit crash mid-wave leaves pages Completed but HTML missing (Notion built first).
  Detect via: Notion Status=Completed AND explainers/<slug>_explainer.html missing/<15KB.
