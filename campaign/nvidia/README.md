# NVIDIA Harness — alternate topic builder

Builds AI-vault topics (Notion page + interactive HTML explainer) using an
**NVIDIA-hosted model** (build.nvidia.com) instead of Claude subagents.

It is **purely additive**. It consumes the same queue (`campaign/next.txt`), writes to
the same `explainers/` folder and the same Notion database as the Claude path.
Nothing in the Claude pipeline was changed. See "Revert to pure Claude" below.

## Design (why it's built this way)

The model does ONLY content generation. All the fragile/mechanical parts run in our
deterministic Python — this is where open models fail, so we don't let them do it:

- **HTML**: one `chat_long()` call → `explainers/<slug>_explainer.html`.
- **Notion**: one `chat_long()` call → a **line-based DSL** (NOT JSON — JSON mangles LaTeX
  backslashes) → parsed by us → pushed via the proven `notion_template.py`.
- **Robustness baked in**: emoji sanitized to a single valid emoji; code language mapped
  to Notion's allowed set; page push is **per-block resilient** (a malformed block skips
  itself instead of nuking the page).

## Setup

Keys live in `campaign/nvidia/.env` (gitignored — never committed). Pure stdlib, nothing to install.

## Usage

```bash
cd ~/Downloads/PersonalSkillUp/AI

# 1. see which models your keys can call
python3 campaign/nvidia/build_topic.py --list

# 2. pull a wave into the shared queue (same command the Claude path uses)
python3 campaign/fastqueue.py --limit 20

# 3. build that wave with an NVIDIA model
python3 campaign/nvidia/build_topic.py --model deepseek-ai/deepseek-v4-pro --concurrency 3

# 4. sync truth from Notion, then repeat from step 2
python3 campaign/fastqueue.py --reconcile
```

Single-topic pilot:
```bash
python3 campaign/nvidia/build_topic.py \
  --model nvidia/llama-3.3-nemotron-super-49b-v1.5 \
  --pageid <uuid> --topic "Orthogonal initialization" \
  --context "init weights as orthogonal matrices; preserves norms; helps deep/RNN training"
```

### Models worth trying (from your catalog, strongest first)
- `deepseek-ai/deepseek-v4-pro` — likely best overall quality/math
- `nvidia/llama-3.1-nemotron-ultra-253b-v1` — NVIDIA's flagship reasoning tune
- `nvidia/nemotron-3-ultra-550b-a55b` — newest large Nemotron
- `moonshotai/kimi-k2.6` — strong at code (good for the HTML)
- `openai/gpt-oss-120b` — solid open reasoning
- `nvidia/llama-3.3-nemotron-super-49b-v1.5` — the tested default (faster, cheaper, decent)

Tip: pilot 3-5 topics on 2-3 models, eyeball the pages/explainers, then commit to one.

### Flags
- `--concurrency N` — parallel topics (default 3; one per API key is a good match)
- `--html-max-tokens`, `--notion-max-tokens` — raise if outputs truncate (default 16384)
- `--dry-run` — plan only, no API calls to generate content
- Per-topic logs (incl. errors) land in `campaign/nvidia/logs/<slug>.json`

## Known quality caveats (measured, not theoretical)

- HTML tends to be **smaller/simpler** than Claude's (~15-25KB vs ~40KB) — less elaborate viz.
- Occasional single blocks get skipped by the resilient push (logged) — page still lands.
- Throughput ~5-8 min/topic on the 49B (HTML gen dominates).
- **Always `--reconcile` after a run**: Notion Status is ground truth; a topic only counts
  as done if its page actually populated. Re-running a topic is idempotent.

## Revert to pure Claude (instant, nothing to undo)

This harness only *reads* `campaign/next.txt` and writes pages/HTML. To go back to the
Claude pipeline, just resume spawning Claude subagents from the same queue:

```bash
python3 campaign/fastqueue.py --reconcile
python3 campaign/fastqueue.py --limit 20
# then Claude builds each line in campaign/next.txt via campaign/BRIEF.md
```

Or just tell Claude "go back to pure Claude" — it will pick up from the reconciled cursor.
Nothing NVIDIA-specific touches the shared state, so there is no cleanup step.
