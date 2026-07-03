#!/usr/bin/env python3
"""
Fast local queue: advances a cursor over the canonical topic_page_ids.json order,
so pulling the next wave is INSTANT (no Notion round-trip).

- First run (or --reconcile): does ONE Notion query to find which canonical indices
  are already Completed, sets the cursor to the first not-Completed index, and records
  the set of completed indices so already-done "islands" (GLS/WLS) are skipped.
- Subsequent runs: pure local reads. Outputs next N as "page_id | topic" to
  campaign/next.txt and advances the cursor, skipping any indices already Completed.

Usage:
    python3 campaign/fastqueue.py --reconcile      # sync cursor + completed set from Notion
    python3 campaign/fastqueue.py --limit 8        # next 8 (instant), advance cursor
    python3 campaign/fastqueue.py --peek 8         # next 8 without advancing
"""
import json, os, sys, argparse, urllib.request, ssl, time

AI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CDIR = os.path.dirname(os.path.abspath(__file__))
CURSOR = os.path.join(CDIR, "cursor.txt")
DONE = os.path.join(CDIR, "completed_idx.json")
NEXT = os.path.join(CDIR, "next.txt")
FLOOR = os.path.join(CDIR, "floor.txt")  # never advance cursor below this canonical index
IDS = os.path.join(AI, "topic_page_ids.json")


def get_floor():
    try:
        return int(open(FLOOR).read().strip())
    except Exception:
        return 0

TOKEN = "NOTION_TOKEN_REDACTED"
DB = "33c93418-809c-81f7-a93d-df0ac011aa09"
_ctx = ssl.create_default_context(); _ctx.check_hostname = False; _ctx.verify_mode = ssl.CERT_NONE


def _urlopen_retry(req, tries=8):
    """Notion intermittently returns transient 401/429/5xx; retry with backoff."""
    for k in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60, context=_ctx) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (401, 429, 500, 502, 503, 504) and k < tries - 1:
                time.sleep(min(60, 2 * (2 ** k)))
                continue
            raise


def load_order():
    d = json.load(open(IDS))
    topics = list(d.keys())
    return topics, d  # ordered topic names, {topic: page_id}


def reconcile():
    """Query Notion once; record completed canonical indices; set cursor."""
    topics, ids = load_order()
    idx_of = {t: i for i, t in enumerate(topics)}
    H = {"Authorization": f"Bearer {TOKEN}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
    completed = set()
    payload = {"page_size": 100, "filter": {"property": "Status", "select": {"equals": "Completed"}}}
    while True:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(f"https://api.notion.com/v1/databases/{DB}/query", data=data, headers=H, method="POST")
        res = _urlopen_retry(req)
        for p in res.get("results", []):
            arr = p["properties"].get("Topic", {}).get("title", [])
            name = arr[0]["text"]["content"] if arr else None
            if name in idx_of:
                completed.add(idx_of[name])
        if not res.get("has_more"):
            break
        payload["start_cursor"] = res["next_cursor"]
    json.dump(sorted(completed), open(DONE, "w"))
    # cursor = first index at/after the floor that is not completed
    cur = get_floor()
    while cur in completed:
        cur += 1
    open(CURSOR, "w").write(str(cur))
    print(f"reconciled: {len(completed)} completed, floor={get_floor()}, cursor={cur}")
    return completed, cur


def get_completed():
    if os.path.exists(DONE):
        return set(json.load(open(DONE)))
    return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--peek", type=int, default=0)
    ap.add_argument("--reconcile", action="store_true")
    args = ap.parse_args()

    if args.reconcile or not os.path.exists(CURSOR):
        reconcile()
        if not (args.limit or args.peek):
            return

    topics, ids = load_order()
    completed = get_completed()
    cur = int(open(CURSOR).read().strip())
    n = args.limit or args.peek or 8

    batch, i = [], cur
    while len(batch) < n and i < len(topics):
        if i not in completed:
            t = topics[i]
            batch.append((i, ids[t], t))
        i += 1

    lines = [f"{pid} | {t}" for (_, pid, t) in batch]
    open(NEXT, "w").write("\n".join(lines))
    print("\n".join(lines))

    if args.limit:  # advance cursor past this batch (do NOT mark completed —
        # failures must stay visible; reconcile from Notion truth handles gaps)
        open(CURSOR, "w").write(str(i))


if __name__ == "__main__":
    main()
