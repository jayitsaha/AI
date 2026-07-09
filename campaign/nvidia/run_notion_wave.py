#!/usr/bin/env python3
"""
NVIDIA Notion page builder — pushes pages from campaign/next.txt in parallel.
Low concurrency (3-5) to avoid starving Gemini's sockets.

Run from repo root:
  cd ~/Downloads/PersonalSkillUp/AI
  python3 campaign/nvidia/run_notion_wave.py

Options:
  python3 campaign/nvidia/run_notion_wave.py --model deepseek-ai/deepseek-r1 --concurrency 3 --limit 50
  python3 campaign/nvidia/run_notion_wave.py --notion-only --concurrency 5
"""
import argparse, json, os, re, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, AI)

from nvidia_client import NvidiaClient
from blocks_spec import blocks_from_dsl
import prompts
import notion_template as NT

# Ensure Notion token is set
if not NT.TOKEN:
    NT.TOKEN = os.environ.get("NOTION_API_TOKEN", "")
    NT.HEADERS["Authorization"] = f"Bearer {NT.TOKEN}"

EXPLAINERS_DIR = os.path.join(AI, "explainers")
LOGS = os.path.join(HERE, "logs")
NEXT = os.path.join(AI, "campaign", "next.txt")
URL_FMT = "https://jayitsaha.github.io/AI/explainers/{slug}_explainer.html"
ICON = {"Foundational": "🟢", "Intermediate": "🟡", "Advanced": "🟠", "Expert": "🔴"}


def slugify(t):
    s = t.split(":")[0].split("(")[0].strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:48] or "topic"


def push_page(page_id, icon, props, blocks):
    """Resilient push with per-block fallback on batch failure."""
    base = "https://api.notion.com/v1"
    NT.api("PATCH", f"{base}/pages/{page_id}",
           {"icon": {"type": "emoji", "emoji": icon}, "properties": props})
    NT.clear_page(page_id)
    url = f"{base}/blocks/{page_id}/children"
    sent = 0
    B = 40
    for i in range(0, len(blocks), B):
        chunk = blocks[i:i + B]
        try:
            NT.api("PATCH", url, {"children": chunk}, retries=2)
            sent += len(chunk)
        except Exception:
            for blk in chunk:
                try:
                    NT.api("PATCH", url, {"children": [blk]}, retries=1)
                    sent += 1
                except Exception:
                    pass
        time.sleep(0.35)
    return sent


def build_notion(client, model, page_id, topic, context, url, max_tokens):
    msgs = [
        {"role": "system", "content": prompts.SYSTEM_NOTION},
        {"role": "user", "content": prompts.notion_user_prompt(topic, context, url)},
    ]
    raw = client.chat_long(model, msgs, max_tokens=max_tokens, temperature=0.3,
                           max_rounds=4)
    meta, blocks = blocks_from_dsl(raw)
    depth = meta.get("depth", "Intermediate")
    if depth not in ICON:
        depth = "Intermediate"
    priority = meta.get("priority", "Important")
    if len(blocks) < 30:
        raise ValueError(f"only {len(blocks)} blocks parsed from DSL")
    props = {
        "Status": {"select": {"name": "Completed"}},
        "Depth": {"select": {"name": depth}},
        "Interview Priority": {"select": {"name": priority}},
        "Has Explainer": {"checkbox": True},
        "Explainer URL": {"url": url},
    }
    sent = push_page(page_id, ICON[depth], props, blocks)
    if sent < 30:
        raise ValueError(f"only {sent}/{len(blocks)} blocks accepted by Notion")
    return sent, depth, priority


def do_topic(client, model, page_id, topic, max_tokens):
    slug = slugify(topic)
    url = URL_FMT.format(slug=slug)
    try:
        nb, depth, prio = build_notion(client, model, page_id, topic, topic, url, max_tokens)
        line = f"{slug} | Notion:y ({nb} blocks) | {depth}/{prio}"
    except Exception as e:
        line = f"{slug} | Notion:n | ERROR: {type(e).__name__}: {str(e)[:80]}"
        # Log error
        os.makedirs(LOGS, exist_ok=True)
        with open(os.path.join(LOGS, f"{slug}.err"), "w") as f:
            f.write(traceback.format_exc())
    return line


def read_queue(limit=None):
    items = []
    if os.path.exists(NEXT):
        for line in open(NEXT):
            line = line.strip()
            if "|" in line:
                pid, topic = line.split("|", 1)
                items.append((pid.strip(), topic.strip()))
    if limit:
        items = items[:limit]
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-ai/deepseek-r1",
                    help="NVIDIA-hosted model for Notion content generation")
    ap.add_argument("--concurrency", type=int, default=3,
                    help="Parallel workers (keep low: 3-5 to avoid socket contention)")
    ap.add_argument("--max-tokens", type=int, default=16384)
    ap.add_argument("--limit", type=int, default=None,
                    help="Process only first N topics from queue")
    ap.add_argument("--list", action="store_true", help="List available models")
    args = ap.parse_args()

    client = NvidiaClient()
    if args.list:
        data = client.list_models()
        for m in sorted(x["id"] for x in data.get("data", [])):
            print(m)
        return

    items = read_queue(args.limit)
    if not items:
        print("No topics in campaign/next.txt")
        return

    print(f"{'='*60}")
    print(f"NVIDIA Notion Page Builder")
    print(f"{'='*60}")
    print(f"Model: {args.model}")
    print(f"Keys: {len(client.keys)} | Concurrency: {args.concurrency}")
    print(f"Topics: {len(items)}")
    print(f"{'='*60}\n")

    t0 = time.time()
    ok_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(do_topic, client, args.model, pid, topic, args.max_tokens): topic
                for pid, topic in items}
        for fut in as_completed(futs):
            line = fut.result()
            if "Notion:y" in line:
                ok_count += 1
            else:
                fail_count += 1
            print(f"  [{ok_count+fail_count}/{len(items)}] {line}", flush=True)

    dt = int(time.time() - t0)
    print(f"\n{'='*60}")
    print(f"DONE: {ok_count}/{len(items)} pages built in {dt}s ({dt//60}m)")
    print(f"Failed: {fail_count} (check campaign/nvidia/logs/*.err)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
