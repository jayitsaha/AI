# Hybrid workflow — NVIDIA (Notion) + Sonnet (HTML) + Opus (orchestration)

Per the token-split decision: heavy Notion prose → NVIDIA; interactive HTML → Sonnet;
orchestration → Opus. Roughly halves Claude usage while keeping HTML quality high.

## Per wave (Opus drives)
1. Pull the wave:            python3 campaign/fastqueue.py --limit 20
2. Get canonical slugs:      python3 campaign/nvidia/build_topic.py --print-slugs
3. In PARALLEL:
   a. NVIDIA builds Notion pages (background):
        python3 campaign/nvidia/build_topic.py --model <M> --notion-only --concurrency 3
   b. Opus spawns one Sonnet subagent per topic to build ONLY the HTML, following
      campaign/BRIEF_HTML.md, using the EXACT slug from step 2 (so the embed URL matches).
4. When both finish:         python3 campaign/fastqueue.py --reconcile   # then repeat

## Slug agreement (critical)
Both engines must use the same slug so the Notion embed points at Sonnet's HTML file.
`--print-slugs` is the source of truth; pass those exact slugs to the Sonnet workers.
Verified working: NVIDIA embed URL == Sonnet HTML filename.

## Model for the Notion side
Tested on nvidia/llama-3.3-nemotron-super-49b-v1.5 (57-59 blocks, 9+ equations/page).
Swap --model for deepseek-ai/deepseek-v4-pro or nvidia/llama-3.1-nemotron-ultra-253b-v1
for higher quality. Always --reconcile after (Notion Status = ground truth).

## Revert to pure Claude
Stop using the NVIDIA step; have Sonnet/Claude build BOTH page+HTML via campaign/BRIEF.md.
Nothing to undo — shared queue + shared Notion DB.
