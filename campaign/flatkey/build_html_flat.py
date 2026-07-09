#!/usr/bin/env python3
"""Parallel HTML explainer builder via flatkey.ai (round-robin keys, streaming).
Interactive-diagram-first. Builds every missing/broken explainer up to a target index.

  python3 campaign/flatkey/build_html_flat.py [target] [workers] [model]
"""
import sys, os, re, time, json, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(AI, "campaign", "nvidia")); sys.path.insert(0, AI)
from flatkey_client import FlatkeyClient
import prompts

TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 1318
WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 else 12
MODEL = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-flash"
EXPL = os.path.join(AI, "explainers")
LOGDIR = os.path.join(HERE, "logs"); os.makedirs(LOGDIR, exist_ok=True)
FAILED = os.path.join(HERE, "failed.tsv")
MIN_KB = 30
# one strong example keeps input cost low while nailing the house style
GOLD = open(os.path.join(EXPL, "generalized_least_squares_gls_explainer.html")).read()
SYSTEM = ("You are a senior front-end engineer and ML educator. You output ONE complete, "
          "self-contained interactive HTML explainer starting at <!DOCTYPE html>. "
          "Output ONLY raw HTML — no markdown fences, no commentary, no <think> text.")


def slugify(t):
    s = t.split(":")[0].split("(")[0].strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:48] or "topic"


def fine(p):
    try: h = open(p, errors="ignore").read()
    except Exception: return False
    if len(h) < 30000: return False
    if "<!doctype" not in h.lower() or "</html>" not in h.lower(): return False
    scr = re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", h, re.S)
    if max((len(s) for s in scr), default=0) < 4000: return False
    if re.search(r"(?:const|let|var)\s+(?:steps|STEPS)\s*=\s*\[\s*\]", h): return False
    return True


def strip_html(t):
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S).strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t); t = re.sub(r"\n?```\s*$", "", t)
    i = t.lower().find("<!doctype")
    return t[i:] if i >= 0 else t.strip()


def build_todo():
    d = json.load(open(os.path.join(AI, "topic_page_ids.json")))
    topics = list(d.keys())
    floor = int(open(os.path.join(AI, "campaign", "floor.txt")).read().strip())
    todo, seen = [], set()
    for i in range(floor, TARGET):   # index order (ScaNN → §33) — redoes the Gemini-bad early parts first
        t = topics[i]; s = slugify(t)
        if s in seen: continue
        seen.add(s); p = os.path.join(EXPL, f"{s}_explainer.html")
        if not (os.path.exists(p) and fine(p)):
            todo.append((s, t))
    todo.reverse()   # tail-first, so flatkey diverges from the front-first internal Sonnet waves
    return todo


def build_one(client, slug, topic):
    user = (f"Match the exact house style (design tokens, collapsible cards, KaTeX, "
            f"step-synced interactive visualization, controls) of this reference explainer:\n\n"
            f"{GOLD}\n\n========================================\n"
            f"NOW BUILD A NEW ONE for the topic below — same quality/style but a DIFFERENT, "
            f"topic-appropriate visualization. The INTERACTIVE DIAGRAM is the single most "
            f"important deliverable: it must be a real working canvas/svg viz with >=8 steps, "
            f"live-computed numbers, and a walkthrough that is NEVER empty.\n\n"
            f"{prompts.html_user_prompt(topic, slug, topic)}")
    txt = client.chat(MODEL, [{"role": "system", "content": SYSTEM},
                              {"role": "user", "content": user}],
                      max_tokens=32000, temperature=0.5)
    html = strip_html(txt)
    if "<!doctype" not in html.lower():
        raise ValueError(f"no doctype ({len(html)} chars)")
    if len(html) // 1024 < MIN_KB:
        raise ValueError(f"thin {len(html)//1024}KB")
    open(os.path.join(EXPL, f"{slug}_explainer.html"), "w").write(html)
    return len(html) // 1024


def funded_keys(keys):
    """Probe each key with a tiny request; keep only those with credit (skip 403 insufficient_quota)."""
    import urllib.request, urllib.error, ssl
    from flatkey_client import UA, _ctx
    def ok(k):
        p = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": "hi"}],
                        "max_tokens": 5, "stream": True}).encode()
        req = urllib.request.Request("https://console.flatkey.ai/v1/chat/completions", data=p,
            headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json",
                     "User-Agent": UA, "Accept": "text/event-stream"}, method="POST")
        try:
            urllib.request.urlopen(req, timeout=30, context=_ctx).read(200); return True
        except urllib.error.HTTPError as e:
            return e.code not in (402, 403)   # out of credit / blocked -> drop
        except Exception:
            return True   # transient -> keep
    with ThreadPoolExecutor(max_workers=len(keys)) as ex:
        flags = list(ex.map(ok, keys))
    return [k for k, f in zip(keys, flags) if f]


def main():
    client = FlatkeyClient()
    good = funded_keys(client.keys)
    if good:
        client.keys = good
    workers = min(WORKERS, max(1, len(client.keys)))
    todo = build_todo()
    print(f"{len(client.keys)} funded keys | {workers} workers | model={MODEL} | {len(todo)} to build", flush=True)
    done = [0]; lock = threading.Lock(); fails = []
    t0 = time.time()

    def work(item):
        slug, topic = item
        try:
            kb = build_one(client, slug, topic)
            with lock:
                done[0] += 1; d = done[0]
            return f"[{d}/{len(todo)}] {slug} | {kb}KB"
        except Exception as e:
            fails.append(item)
            return f"{slug} | FAIL {str(e)[:60]}"

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(work, it) for it in todo]):
            print("  " + fut.result(), flush=True)
    if fails:
        open(FAILED, "w").writelines("\t".join(x) + "\n" for x in fails)
    print(f"\nDONE {len(todo)-len(fails)}/{len(todo)} in {int(time.time()-t0)}s | failed={len(fails)}", flush=True)


if __name__ == "__main__":
    main()
