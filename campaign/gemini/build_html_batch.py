#!/usr/bin/env python3
"""Build HTML for a todo list via Gemini (skips ones already built; continues past failures)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import build_html as bh

TODO = os.path.join(AI, "campaign", "gemini", "html_todo.tsv")
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-2.5-flash"

for line in open(TODO):
    p = line.rstrip("\n").split("\t")
    if len(p) < 3:
        continue
    pid, topic, slug = p[0], p[1], p[2]
    out = os.path.join(AI, "explainers", f"{slug}_explainer.html")
    if os.path.exists(out) and os.path.getsize(out) > 15000:
        print(f"{slug} | skip (exists)", flush=True); continue
    try:
        _, n, dt, fin = bh.build(MODEL, slug, topic, topic, max_tokens=48000)
        print(f"{slug} | {n//1024}KB {dt}s {fin}", flush=True)
    except Exception as e:
        print(f"{slug} | FAIL {str(e)[:70]}", flush=True)
