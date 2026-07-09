#!/usr/bin/env python3
"""Full wave builder using GEMINI for BOTH the Notion page and the HTML explainer.
Off the Claude budget AND off the (currently flaky) NVIDIA endpoint.

  python3 campaign/fastqueue.py --limit 20
  python3 campaign/gemini/build_topic_gemini.py --concurrency 2
"""
import argparse, os, sys, time, traceback, json
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(AI, "campaign", "nvidia"))

from gemini_client import GeminiClient
import prompts, blocks_spec
import build_html as gh                       # example-fed HTML builder
from build_topic import push_page, slugify, URL_FMT, ICON, read_queue, LOGS
import notion_template as NT

NOTION_MODEL_DEFAULT = "gemini-2.5-flash"
HTML_MODEL_DEFAULT = "gemini-2.5-flash"


def build_notion(gc, model, page_id, topic, context, url):
    txt, fin = gc.generate(model, prompts.SYSTEM_NOTION,
                           prompts.notion_user_prompt(topic, context, url),
                           max_tokens=16000, temperature=0.3)
    meta, blocks = blocks_spec.blocks_from_dsl(txt)
    depth = meta.get("depth", "Intermediate")
    if depth not in ICON:
        depth = "Intermediate"
    priority = meta.get("priority", "Important")
    if len(blocks) < 30:
        raise ValueError(f"only {len(blocks)} blocks (finish={fin})")
    props = {
        "Status": {"select": {"name": "Completed"}},
        "Depth": {"select": {"name": depth}},
        "Interview Priority": {"select": {"name": priority}},
        "Has Explainer": {"checkbox": True},
        "Explainer URL": {"url": url},
    }
    sent = push_page(page_id, ICON[depth], props, blocks)
    if sent < 30:
        raise ValueError(f"only {sent}/{len(blocks)} blocks accepted")
    return sent, depth, priority


def do_topic(gc, nmodel, hmodel, page_id, topic, context, notion_only, html_only):
    slug = slugify(topic)
    url = URL_FMT.format(slug=slug)
    rec = {"topic": topic, "slug": slug, "html": False, "notion": 0}
    try:
        if not notion_only:
            gh.build(hmodel, slug, topic, context, max_tokens=48000)
            rec["html"] = True
        nb = depth = prio = None
        if not html_only:
            nb, depth, prio = build_notion(gc, nmodel, page_id, topic, context, url)
            rec["notion"] = nb
        htag = "y" if rec["html"] else ("skip" if notion_only else "n")
        ntag = f"y ({nb})" if nb else ("skip" if html_only else "n")
        line = f"{slug} | HTML:{htag} | Notion:{ntag} | {depth or ''}/{prio or ''}"
    except Exception as e:
        line = (f"{slug} | HTML:{'y' if rec['html'] else 'n'} | "
                f"Notion:{'y('+str(rec['notion'])+')' if rec['notion'] else 'n'} | "
                f"ERROR: {type(e).__name__}: {e}")
        rec["error"] = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
    os.makedirs(LOGS, exist_ok=True)
    json.dump(rec, open(os.path.join(LOGS, f"{slug}.json"), "w"), indent=2)
    return line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notion-model", default=NOTION_MODEL_DEFAULT)
    ap.add_argument("--html-model", default=HTML_MODEL_DEFAULT)
    ap.add_argument("--concurrency", type=int, default=2)  # respect Gemini free-tier RPM
    ap.add_argument("--notion-only", action="store_true")
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()

    items = read_queue()
    if not items:
        print("No topics. Run: python3 campaign/fastqueue.py --limit N"); return
    gc = GeminiClient()
    print(f"Gemini notion={a.notion_model} html={a.html_model} | {len(items)} topics | conc {a.concurrency}")
    t0 = time.time(); results = []

    def work(pid, topic_raw):
        topic, ctx = (topic_raw.split("||", 1) + [""])[:2] if "||" in topic_raw else (topic_raw, topic_raw)
        return do_topic(gc, a.notion_model, a.html_model, pid, topic.strip(), ctx.strip(),
                        a.notion_only, a.html_only)

    with ThreadPoolExecutor(max_workers=max(1, a.concurrency)) as ex:
        futs = {ex.submit(work, p, t): t for p, t in items}
        for f in as_completed(futs):
            line = f.result(); results.append(line); print("  " + line, flush=True)

    ok = sum(1 for r in results if "ERROR" not in r)
    print(f"\n{ok}/{len(items)} built in {int(time.time()-t0)}s")
    print("Reconcile: python3 campaign/fastqueue.py --reconcile")


if __name__ == "__main__":
    main()
