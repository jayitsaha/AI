#!/usr/bin/env python3
"""Parallel Gemini HTML builder with HARDENED interactive-walkthrough gate + retry.
Rejects any file whose interactive walkthrough is weak and rebuilds until it passes.
  python3 campaign/gemini/parallel_html.py [target_index] [workers]
"""
import sys, os, time, threading, json, re
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE = os.path.dirname(os.path.abspath(__file__)); AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, AI)
from gemini_client import GeminiClient
import build_html as gh

MODEL = ["gemini-2.5-flash"]          # proven-good interactive model only
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 1318
EXPL = os.path.join(AI, "AI", "explainers")
FAILED = os.path.join(HERE, "html_failed.tsv")
ATTEMPTS = 3                          # iterate until the walkthrough is top-notch


def slugify(t):
    s = t.split(":")[0].split("(")[0].strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_"); return re.sub(r"_+", "_", s)[:48] or "topic"


def fine_html(p):
    """HARD gate — file is good only if the interactive walkthrough is real & rich."""
    try: h = open(p, errors="ignore").read()
    except Exception: return False, "missing"
    hl = h.lower()
    if len(h) < 35000: return False, f"{len(h)//1024}KB<35"
    if "<!doctype" not in hl or "</html>" not in hl: return False, "no doctype/html"
    scr = re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", h, re.S)
    big = max(scr, key=len, default="")
    if len(big) < 6000: return False, f"script {len(big)}<6000"
    if re.search(r"(?:const|let|var)\s+(?:steps|STEPS)\s*=\s*\[\s*\]", h): return False, "empty steps[]"
    m = re.search(r"(?:const|let|var)\s+(?:steps|STEPS)\s*=\s*\[", h)
    nsteps, arrlen = 0, 0
    if m:
        i = m.end() - 1; depth = 0; j = i
        while j < len(h):
            c = h[j]
            if c == "[": depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0: break
            j += 1
        arr = h[i:j+1]; arrlen = len(arr); nsteps = len(re.findall(r"\{", arr))
    if nsteps < 8: return False, f"{nsteps}steps<8"
    if arrlen < 1200: return False, "thin steps"
    if ("getcontext" not in hl) and ("<svg" not in hl): return False, "no live canvas/svg"
    if "katex" not in hl: return False, "no katex"
    if not re.search(r"(next|prev|goto|arrowright)", hl): return False, "no nav"
    return True, "ok"


def build_todo():
    d = json.load(open(os.path.join(AI, "topic_page_ids.json"))); topics = list(d.keys())
    start = int(os.environ.get("START_IDX", open(os.path.join(AI, "campaign", "floor.txt")).read().strip()))
    todo, seen = [], set()
    for i in range(start, min(TARGET, len(topics))):
        t = topics[i]; slug = slugify(t)
        if slug in seen: continue
        seen.add(slug)
        if not os.path.exists(os.path.join(EXPL, f"{slug}_explainer.html")):   # MISSING only
            todo.append((d[t], t, slug))
    return todo


def main():
    client = GeminiClient()
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    todo = build_todo()
    print(f"{len(client.keys)} keys | {workers} workers | {len(todo)} to build | target<{TARGET}", flush=True)
    done = [0]; lock = threading.Lock(); fails = []

    def work(item):
        pid, topic, slug = item
        out = os.path.join(EXPL, f"{slug}_explainer.html")
        ok, _ = fine_html(out)
        if ok: return f"{slug} | skip(fine)"
        last = ""
        for a in range(ATTEMPTS):
            try:
                _, n, dt, fin = gh.build(MODEL, slug, topic, topic, max_tokens=48000, client=client)
            except Exception as e:
                last = f"build:{str(e)[:40]}"; continue
            ok, reason = fine_html(out)
            if ok:
                with lock:
                    done[0] += 1; d = done[0]
                return f"[{d}/{len(todo)}] {slug} | {n//1024}KB a{a+1}"
            last = reason
            try: os.remove(out)
            except Exception: pass
        fails.append((pid, topic, slug))
        return f"{slug} | FAIL {ATTEMPTS}x ({last})"

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(work, it) for it in todo]):
            print("  " + fut.result(), flush=True)
    if fails:
        open(FAILED, "w").writelines("\t".join(map(str, r)) + "\n" for r in fails)
    print(f"\nDONE {len(todo)-len(fails)}/{len(todo)} in {int(time.time()-t0)}s | failed={len(fails)}", flush=True)


if __name__ == "__main__":
    main()
