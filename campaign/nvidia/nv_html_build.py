#!/usr/bin/env python3
"""Build HTML explainers with an NVIDIA-hosted heavy model (reuses gemini build_html prompt)."""
import sys, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed
HERE=os.path.dirname(os.path.abspath(__file__)); AI=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(AI,"campaign","gemini")); sys.path.insert(0, HERE)
from nvidia_client import NvidiaClient
import build_html as gh

MODEL = sys.argv[1] if len(sys.argv)>1 else "deepseek-ai/deepseek-v4-pro"
TSV   = sys.argv[2] if len(sys.argv)>2 else "/tmp/nvtest.tsv"
WORKERS = int(sys.argv[3]) if len(sys.argv)>3 else 4

class NVAdapter:
    """Expose .generate(model, system, user,...) over NvidiaClient.chat_long."""
    def __init__(self): self.c=NvidiaClient()
    def generate(self, model, system, user, max_tokens=48000, temperature=0.6):
        msgs=[{"role":"system","content":system},{"role":"user","content":user}]
        txt=self.c.chat_long(model, msgs, max_tokens=max_tokens, temperature=temperature)
        return txt, "stop"

def work(client, idx, slug, topic):
    try:
        path,n,dt,fin = gh.build(MODEL, slug, topic, topic, max_tokens=48000, client=client)
        return f"{slug} | {n//1024}KB | {dt}s"
    except Exception as e:
        return f"{slug} | FAIL {type(e).__name__}: {str(e)[:70]}"

def main():
    rows=[l.rstrip("\n").split("\t") for l in open(TSV) if l.strip()]
    client=NVAdapter()
    print(f"model={MODEL} | {len(rows)} to build | {WORKERS} workers", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs=[ex.submit(work, client, r[0], r[1], r[2]) for r in rows]
        for f in as_completed(futs): print("  "+f.result(), flush=True)

if __name__=="__main__": main()
