#!/usr/bin/env python3
"""Parallel Gemini HTML builder — one worker per key (thread-safe rotation).
Builds HTML for ALL remaining topics up to a target index that lack an HTML file.
Failures (after retries across all keys) are logged to campaign/gemini/html_failed.tsv
for a Sonnet fallback pass.

  python3 campaign/gemini/parallel_html.py [target_index] [workers]
"""
import sys, os, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, AI)
import json
from gemini_client import GeminiClient
import build_html as gh

# gemini-2.5-flash ONLY — the proven good model for interactive HTML (quota reset).
# NO *-lite models (they botch the interactive walkthrough).
MODEL = ["gemini-2.5-flash"]
MIN_KB = 30  # reject/redo anything smaller (thin/broken signature)
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 1318
EXPL = os.path.join(AI, "explainers")
FAILED = os.path.join(HERE, "html_failed.tsv")


def slugify(t):
    import re
    s = t.split(":")[0].split("(")[0].strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:48] or "topic"


def build_todo():
    d = json.load(open(os.path.join(AI, "topic_page_ids.json")))
    topics = list(d.keys())
    floor = int(open(os.path.join(AI, "campaign", "floor.txt")).read().strip())
    todo, seen = [], set()
    for i in range(floor, min(TARGET, len(topics))):
        t = topics[i]; slug = slugify(t)
        if slug in seen:
            continue
        seen.add(slug)
        if not os.path.exists(os.path.join(EXPL, f"{slug}_explainer.html")):
            todo.append((d[t], t, slug))
    return todo


def main():
    client = GeminiClient()          # shared, thread-safe key rotation
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else len(client.keys)
    todo = build_todo()
    print(f"{len(client.keys)} keys | {workers} workers | {len(todo)} HTML to build | target<{TARGET}", flush=True)
    done = [0]; lock = threading.Lock(); fails = []

    def work(item):
        pid, topic, slug = item
        out = os.path.join(EXPL, f"{slug}_explainer.html")
        if os.path.exists(out) and os.path.getsize(out) > 15000:
            return f"{slug} | skip"
        try:
            _, n, dt, fin = gh.build(MODEL, slug, topic, topic, max_tokens=48000, client=client)
            if n // 1024 < MIN_KB:                      # lite/weak output -> reject & requeue
                try: os.remove(out)
                except Exception: pass
                fails.append((pid, topic, slug))
                return f"{slug} | REJECT {n//1024}KB (too small)"
            with lock:
                done[0] += 1
                d = done[0]
            return f"[{d}/{len(todo)}] {slug} | {n//1024}KB {dt}s"
        except Exception as e:
            fails.append((pid, topic, slug))
            return f"{slug} | FAIL {str(e)[:50]}"

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(work, it) for it in todo]):
            print("  " + fut.result(), flush=True)

    if fails:
        with open(FAILED, "w") as f:
            f.writelines("\t".join(r) + "\n" for r in fails)
    print(f"\nDONE {len(todo)-len(fails)}/{len(todo)} built in {int(time.time()-t0)}s | "
          f"failed={len(fails)} (see html_failed.tsv for Sonnet fallback)", flush=True)


if __name__ == "__main__":
    main()
