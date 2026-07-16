#!/usr/bin/env python3
"""
NVIDIA harness — build AI-vault topics with an NVIDIA-hosted model instead of Claude.

Deterministic pipeline (the LLM only generates content; our code does the rest):
  1. HTML explainer  : one chat_long() call -> explainers/<slug>_explainer.html
  2. Notion page     : one chat() call -> JSON block spec -> notion_template.update_page()

It consumes the SAME queue as the Claude path (campaign/next.txt), writes to the SAME
explainers/ dir and the SAME Notion DB. So reverting to pure Claude needs nothing undone
— just resume spawning Claude subagents from campaign/next.txt.

USAGE
  # list models your keys can call
  python3 campaign/nvidia/build_topic.py --list

  # build the current queue wave (campaign/next.txt) with a chosen model
  python3 campaign/fastqueue.py --limit 20
  python3 campaign/nvidia/build_topic.py --model deepseek-ai/deepseek-v4-pro --concurrency 3

  # single-topic pilot
  python3 campaign/nvidia/build_topic.py --model nvidia/nemotron-3-super-120b-a12b \
      --pageid 33c93418-... --topic "Stochastic depth" --context "layer dropout in ResNets"
"""
import argparse, json, os, re, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, AI)

from nvidia_client import NvidiaClient
from blocks_spec import blocks_from_spec, blocks_from_dsl
import prompts
import notion_template as NT

EXPLAINERS = os.path.join(AI, "explainers")
LOGS = os.path.join(HERE, "logs")
NEXT = os.path.join(AI, "campaign", "next.txt")
URL_FMT = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/{slug}_explainer.html"
ICON = {"Foundational": "🟢", "Intermediate": "🟡", "Advanced": "🟠", "Expert": "🔴"}


def slugify(topic):
    s = topic.split(":")[0].split("(")[0].strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:48] or "topic"


def strip_fences(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)  # reasoning models
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def extract_json(text):
    """Pull the first balanced {...} object out of a model response."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    i = text.find("{")
    if i < 0:
        raise ValueError("no JSON object found")
    depth, in_str, esc = 0, False, False
    for j in range(i, len(text)):
        c = text[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[i:j + 1])
    raise ValueError("unbalanced JSON")


def build_html(client, model, topic, slug, context, max_tokens):
    msgs = [
        {"role": "system", "content": prompts.SYSTEM_HTML},
        {"role": "user", "content": prompts.html_user_prompt(topic, slug, context)},
    ]
    html = client.chat_long(model, msgs, max_tokens=max_tokens, temperature=0.4,
                            stop_marker="</html>")
    html = strip_fences(html)
    if "<!doctype" not in html.lower():
        raise ValueError("HTML output missing doctype")
    path = os.path.join(EXPLAINERS, f"{slug}_explainer.html")
    with open(path, "w") as f:
        f.write(html)
    return path, len(html)


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


def push_page(page_id, icon, props, blocks):
    """Resilient push: set props, clear, then append in batches — and if a batch is
    rejected (one malformed block from the LLM), retry that batch block-by-block so a
    single bad block can't wipe the whole page. Returns count of blocks accepted."""
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
            for blk in chunk:  # fall back per-block, skipping the offender
                try:
                    NT.api("PATCH", url, {"children": [blk]}, retries=1)
                    sent += 1
                except Exception:
                    pass
        time.sleep(0.35)
    return sent


def do_topic(client, model, page_id, topic, context, html_mt, notion_mt,
             dry=False, notion_only=False, slug=None):
    slug = slug or slugify(topic)
    url = URL_FMT.format(slug=slug)
    rec = {"topic": topic, "slug": slug, "html": False, "notion": 0}
    try:
        if dry:
            tail = "Notion only" if notion_only else "HTML + Notion"
            return f"{slug} | DRY-RUN (would build {tail}) | url={url}"
        if not notion_only:
            build_html(client, model, topic, slug, context, html_mt)
            rec["html"] = True
        nb, depth, prio = build_notion(client, model, page_id, topic, context, url, notion_mt)
        rec["notion"] = nb
        htag = "HTML:skip" if notion_only else "HTML:y"
        line = f"{slug} | {htag} | Notion:y ({nb}) | {depth}/{prio}"
    except Exception as e:
        line = (f"{slug} | HTML:{'y' if rec['html'] else ('skip' if notion_only else 'n')} | "
                f"Notion:{'y('+str(rec['notion'])+')' if rec['notion'] else 'n'} | "
                f"ERROR: {type(e).__name__}: {e}")
        rec["error"] = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
    os.makedirs(LOGS, exist_ok=True)
    with open(os.path.join(LOGS, f"{slug}.json"), "w") as f:
        json.dump(rec, f, indent=2)
    return line


def read_queue():
    items = []
    if os.path.exists(NEXT):
        for line in open(NEXT):
            line = line.strip()
            if "|" in line:
                pid, topic = line.split("|", 1)
                items.append((pid.strip(), topic.strip()))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="nvidia/nemotron-3-super-120b-a12b")
    ap.add_argument("--list", action="store_true", help="list available models and exit")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--html-max-tokens", type=int, default=16384)
    ap.add_argument("--notion-max-tokens", type=int, default=16384)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--notion-only", action="store_true",
                    help="hybrid mode: build only the Notion page; Sonnet builds the HTML")
    ap.add_argument("--print-slugs", action="store_true",
                    help="print 'pageid<TAB>topic<TAB>slug' for the queue and exit "
                         "(so the Sonnet HTML workers use matching filenames)")
    # single-topic mode
    ap.add_argument("--pageid")
    ap.add_argument("--topic")
    ap.add_argument("--slug")
    ap.add_argument("--context", default="")
    args = ap.parse_args()

    if args.print_slugs:
        for pid, topic in read_queue():
            print(f"{pid}\t{topic}\t{slugify(topic)}")
        return

    client = NvidiaClient()
    if args.list:
        data = client.list_models()
        for m in sorted(x["id"] for x in data.get("data", [])):
            print(m)
        return

    if args.pageid and args.topic:
        items = [(args.pageid, args.topic if not args.context
                  else f"{args.topic} || {args.context}")]
    else:
        items = read_queue()
    if not items:
        print("No topics. Run: python3 campaign/fastqueue.py --limit N")
        return

    print(f"Model: {args.model} | topics: {len(items)} | concurrency: {args.concurrency}")
    t0 = time.time()
    results = []

    def work(pid, topic_raw):
        topic, context = (topic_raw.split("||", 1) + [""])[:2] if "||" in topic_raw \
            else (topic_raw, topic_raw)
        return do_topic(client, args.model, pid, topic.strip(), context.strip(),
                        args.html_max_tokens, args.notion_max_tokens,
                        dry=args.dry_run, notion_only=args.notion_only,
                        slug=args.slug if args.pageid else None)

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        futs = {ex.submit(work, pid, t): t for pid, t in items}
        for fut in as_completed(futs):
            line = fut.result()
            results.append(line)
            print("  " + line)

    dt = int(time.time() - t0)
    ok = sum(1 for r in results if "Notion:y" in r and "ERROR" not in r)
    print(f"\n{ok}/{len(items)} Notion pages built in {dt}s. Logs: campaign/nvidia/logs/")
    print("Reconcile truth: python3 campaign/fastqueue.py --reconcile")


if __name__ == "__main__":
    main()
