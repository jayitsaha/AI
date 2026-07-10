#!/usr/bin/env python3
"""Gemini-based QC of interactive HTML explainers: read each file's HTML+JS and
judge whether the Prev/Next walkthrough is authentic & functional. Outputs faulty list."""
import os, sys, re, json, glob, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE=os.path.dirname(os.path.abspath(__file__)); AI=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from gemini_client import GeminiClient

EXPL=os.path.join(AI,"AI","explainers")   # the served/tracked folder
MODEL=["gemini-2.5-flash"]
OUT=os.path.join(HERE,"qc_faulty.tsv")
SYS=("You are a strict front-end QA auditor. You statically analyze a self-contained interactive "
     "HTML explainer and decide if its step-by-step Prev/Next walkthrough is AUTHENTIC and would "
     "actually work for a user clicking the buttons. Be rigorous: trace the actual code.")
PROMPT=("""Audit this interactive HTML explainer's walkthrough by reading its HTML + JavaScript. A user must be able to click Prev/Next (or arrow keys) and advance through real, changing steps.

Mark FAULTY if ANY of these hold (trace the real code, cite the exact problem):
1. The steps/slides data is empty (e.g. `const steps = []`) or has fewer than 6 real entries, or is placeholder ("Step 1"/"TODO"/lorem).
2. Prev/Next controls are missing from the DOM.
3. The Next/Prev handler calls a function that is UNDEFINED or out of scope (e.g. onclick="go(1)" but `go` is never defined, a typo'd name, or defined inside a scope the inline handler can't see) — dead buttons.
4. A fatal JS error would throw on load or on click: undefined variable/function, syntax error, or `document.getElementById(...)` returning null then `.style`/`.innerHTML` access (null DOM ref).
5. Clicking Next is a no-op: it does not change a current-step index and re-render the info card/canvas.

Mark OK only if a user clicking Next genuinely advances through >=6 real, changing steps with no crash.

Respond with ONLY this JSON, nothing else:
{"faulty": true|false, "category": "empty-steps|too-few-steps|dead-nav|undefined-ref|syntax-error|null-dom|placeholder|missing-controls|ok", "reason": "<=140 chars citing the specific code"}

HTML:
""")

def verdict(client, path):
    try: html=open(path,errors="ignore").read()
    except Exception as e: return {"faulty":True,"category":"unreadable","reason":str(e)[:80]}
    html=html[:120000]
    try:
        txt,_=client.generate(MODEL, SYS, PROMPT+html, max_tokens=200, temperature=0, tries=4)
    except Exception as e:
        return {"faulty":None,"category":"qc-error","reason":str(e)[:80]}
    m=re.search(r'\{.*\}', txt, re.S)
    if not m: return {"faulty":None,"category":"parse-error","reason":txt[:80]}
    try: return json.loads(m.group(0))
    except Exception: return {"faulty":None,"category":"parse-error","reason":m.group(0)[:80]}

def main():
    client=GeminiClient()
    files=sorted(glob.glob(os.path.join(EXPL,"*.html")))
    print(f"{len(client.keys)} keys | {len(files)} html files to QC via gemini-2.5-flash", flush=True)
    lock=threading.Lock(); done=[0]; faulty=[]; errs=[]
    def work(p):
        v=verdict(client, p); name=os.path.basename(p)
        with lock:
            done[0]+=1; d=done[0]
        if v.get("faulty") is True: faulty.append((name,v.get("category","?"),v.get("reason","")))
        elif v.get("faulty") is None: errs.append((name,v.get("reason","")))
        if d%50==0: print(f"  ...{d}/{len(files)} checked | faulty so far={len(faulty)}", flush=True)
        return name
    with ThreadPoolExecutor(max_workers=12) as ex:
        for f in as_completed([ex.submit(work,p) for p in files]): f.result()
    faulty.sort()
    with open(OUT,"w") as fo:
        for n,c,r in faulty: fo.write(f"{n}\t{c}\t{r}\n")
    print(f"\n=== GEMINI QC COMPLETE: {len(files)} files | FAULTY={len(faulty)} | qc-errors={len(errs)} ===", flush=True)
    for n,c,r in faulty: print(f"FAULTY\t{n}\t[{c}] {r}", flush=True)
    if errs: print(f"\n({len(errs)} files could not be checked: {', '.join(n for n,_ in errs[:10])}...)", flush=True)

if __name__=="__main__": main()
